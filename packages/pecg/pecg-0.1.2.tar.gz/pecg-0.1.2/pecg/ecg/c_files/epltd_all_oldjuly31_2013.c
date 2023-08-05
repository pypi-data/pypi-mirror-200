/*****************************************************************************
FILE:  easytest.cpp
AUTHOR: Patrick S. Hamilton
REVISED:        5/13/2002 (PSH); 4/10/2003 (GBM)

Recised by Qiao Li to processing MIMICII database
called by mimic2_all.c (see mimic2_all.c for more information)
Last revised: 02/20/2007
  ___________________________________________________________________________

easytest.cpp: Use bdac to generate an annotation file.
Copyright (C) 2001 Patrick S. Hamilton
Copyright (C) 1999 George B. Moody

This file is free software; you can redistribute it and/or modify it under
the terms of the GNU Library General Public License as published by the Free
Software Foundation; either version 2 of the License, or (at your option) any
later version.

This software is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Library General Public License for more
details.

You should have received a copy of the GNU Library General Public License along
with this library; if not, write to the Free Software Foundation, Inc., 59
Temple Place - Suite 330, Boston, MA 02111-1307, USA.

You may contact the author by e-mail (pat@eplimited.edu) or postal mail
(Patrick Hamilton, E.P. Limited, 35 Medford St., Suite 204 Somerville,
MA 02143 USA).  For updates to this software, please visit our website
(http://www.eplimited.com).
  __________________________________________________________________________

Easytest.exe is a simple program to help test the performance of our
beat detection and classification software. Data is read from the
indicated ECG file, the channel 1 signal is fed to bdac.c, and the
resulting detections are saved in the annotation file <record>.ate.
<record>.ate may then be compared to <record>.atr to using bxb to
analyze the performance of the the beat detector and classifier detector.

Note that data in the MIT/BIH Arrythmia database file has been sampled
at 360 samples-per-second, but the beat detection and classification
software has been written for data sampled at 200 samples-per-second.
Date is converterted from 360 sps to 200 sps with the function NextSample.
Code for resampling was copied from George Moody's xform utility.  The beat
locations are then adjusted back to coincide with the original sample
rate of 360 samples/second so that the annotation files generated by
easytest can be compared to the "atruth" annotation files.

This file must be linked with object files produced from:
        wfdb software library (source available at www.physionet.org)
        analbeat.cpp
        match.cpp
        rythmchk.cpp
        classify.cpp
        bdac.cpp
        qrsfilt.cpp
        qrsdet.cpp
        postclass.cpp
        noisechk.cpp
  __________________________________________________________________________

  Revisions
        4/13/02:
                Added conditional define statements that allow MIT/BIH or AHA
                        records to be processed.
                Normalize input to 5 mV/LSB (200 A-to-D units/mV).

        4/10/03:
                Moved definitions of Record[] array, ECG_DB_PATH, and REC_COUNT
                        into "input.h"
*******************************************************************************/

#include <wfdb/wfdb.h>
#include <wfdb/ecgcodes.h>
#include <wfdb/ecgmap.h>
#include "string.h"
#include "stdio.h"
#include "stdlib.h"
#include "math.h"
#include "qrsdet.h"

#include "inputs.h"     /* list of records to analyze and definitions of
                           ECG_DB_PATH and REC_COUNT */

                                                 // External function prototypes.
  void ResetBDAC(void);
int BeatDetectAndClassify(int ecgSample, int *beatType, int *beatMatch);

// Local Prototypes.
int NextSample(int *vout, int nosig, int ifreq,
               int ofreq, int init);
int gcd(int x, int y);

// Global variables.

int ADCZero, ADCUnit;

double InputFileSampleFrequency;

WFDB_Sample *v;
WFDB_Siginfo *s;
FILE *fp;
char *pname; /* name by which this program was invoked */
long nsamp=-1L,nsamporig=-1L;
char *prog_name();

#ifdef __STDC__
#define MAINTYPE int
#else
#define MAINTYPE void
#endif

void myquit() {
  free(s);
  free(v);
  wfdbquit();
}

char *ecglead[20] = {"III", "II", "I", "AVR", "AVL", "AVF",  "V1", "V2", "V3", "V4", "V5", "V6", "V","MCL1", "MCL2", "MCL3", "MCL4", "MCL5", "MCL6", "MCL"};

void hpsort(unsigned long n, int ra[]) {
  unsigned long i, ir, j, l;
  int rra;

  if (n < 2) return;
  l = (n >> 1) + 1;
  ir = n;
  for (;;) {
    if (l > 1) {
      rra = ra[--l];
    } else {
      rra = ra[ir];
      ra[ir] = ra[1];
      if (--ir == 1) {
        ra[1] = rra;
        break;
      }
    }
    i = l;
    j = l + l;
    while (j <= ir) {
      if (j < ir && ra[j] < ra[j + 1]) j++;
      if (rra < ra[j]) {
        ra[i] = ra[j];
        i = j;
        j <<= 1;
      } else j = ir + 1;
    }
    ra[i] = rra;
  }
}

int findb(int *tempsort, int firstb, int n) {
  int i;

  for (i = 0; i < n; i++)
    if (tempsort[i] == firstb)
      return (i);
  return 0;
}

void insertsort(int ra[], int n, int old, int new) // delete old value, insert new value at proper position with order
{
  int pint, j, j2;

  pint = findb(ra, old, n);
  if (ra[pint] > new) {
    for (j = 0; j < pint; j++)
      if (ra[j] >= new) {
        for (j2 = pint; j2 > j; j2--)
          ra[j2] = ra[j2 - 1];
        ra[j] = new;
        break;
      }
    if (j == pint)
      ra[pint] = new;
  } else if (ra[pint] < new) {
    for (j = pint + 1; j < n; j++)
      if (ra[j] >= new) {
        for (j2 = pint; j2 < j - 1; j2++)
          ra[j2] = ra[j2 + 1];
        ra[j2] = new;
        break;
      }
    if (j == n) {
      for (j2 = pint; j2 < j - 1; j2++)
        ra[j2] = ra[j2 + 1];
      ra[j2] = new;
    }
  }
}

double mykurtosis(int *data, int n) {

  int i;
  double mean, mean4, std, std4;

  mean = 0;
  for (i = 0; i < n; i++) {
    mean += data[i];
  }
  mean /= n;
  std = 0;
  mean4 = 0;
  for (i = 0; i < n; i++) {
    std += ((data[i] - mean)*(data[i] - mean));
    mean4 += (pow((data[i] - mean), 4));
  }
  std4 = std*std;
  mean4 *= n;
  return (mean4 / std4);
}

MAINTYPE main(int argc, char *argv[]) {
  char *record;
  char fname[50];
  int i, ecg[20], delay, recNum;
  //    WFDB_Siginfo si[3] ;
  WFDB_Anninfo a[2];
  WFDB_Annotation annot;
  WFDB_Siginfo s[100];
  WFDB_Sample v[20];
  int leadi, leadj;
  int ecgbuf[40], sortbuf[40], ecgbufp;

  unsigned char byte;
  FILE *newAnn0, *newAnn1;
  long SampleCount = 0;
  int lTemp;
  double DetectionTime; // Changed to double for MIMIC II
  int beatType, beatMatch;
  char tempfname1[50], tempfname2[50], tempfname[100];
  int nsig, n, onsig;
  char *p;
  char tempname[10], tempname1[10];
  long next_minute, datalength, timecount;
  double tempk;
  int filtold, dataold, filt;
  int old;
  long from = 0L, to = 0L;
  // Set up path to database directory
  if (argc < 2) {
    fprintf(stderr, "Usage: %s -r record\n", argv[0]);
    exit(-1);
  }
  wfdbquiet();

  pname = (char *) prog_name(argv[0]);
  for (i = 1; i < argc; i++) {
    if (*argv[i] == '-') switch (*(argv[i] + 1)) {

      case 'r': /* input record name */
        if (++i >= argc) {
          (void) fprintf(stderr, "%s: record name must follow -r\n",
                         pname);
          exit(1);
        }
        record = argv[i];
        break;
      case 'f': /* starting time */
        if (++i >= argc) {
          (void) fprintf(stderr, "%s: time must follow -f\n", pname);
          exit(1);
        }
        from = i;
        break;
      case 't': /* end time */
        if (++i >= argc) {
          (void) fprintf(stderr, "%s: time must follow -t\n", pname);
          exit(1);
        }
        to = i;
        break;
      default:
        (void) fprintf(stderr, "%s: unrecognized option %s\n", pname,
                       argv[i]);
        exit(1);


      }
  }

  //    while (!feof(fp))
  for (i = 1; i <= 1; i++) {
    //          strcpy(tempfname,"mimic2db/");
    //          strcpy(tempfname,"mimicdb/");
    //          strcpy(tempfname,"noise/");
    //          strcat(tempfname,tempfname2);
    //          strcat(tempfname,"/");
    printf("Processing %s ... \n", record);


    // Open a 2 channel record

    nsig = isigopen(record, NULL, 0);
    InputFileSampleFrequency = sampfreq(record) ;

    /*      s = (WFDB_Siginfo *)calloc(sizeof(WFDB_Siginfo),nsig);
            v = (WFDB_Sample *)calloc(sizeof(WFDB_Sample),nsig);
            if (s == NULL || v == NULL ) {
            fprintf(stderr, "insufficient memory\n");
            myquit(tempfname2);
            continue;
            }
    */
    //          printf("record: %s nsig: %d\n",record,nsig);
    if (isigopen(record, s, nsig) < nsig) {
      printf("Couldn't open %s\n", record);
      myquit();
      continue;
    }

    if (from > 0L) {
      fprintf(stderr,"from: %s\n",argv[from]);
      from = strtim(argv[from]);
      if (from < (WFDB_Time) 0) from = -from;
      (void) isigsettime(from);
    }
    if (to > 0L) {
      fprintf(stderr,"to: %s\n",argv[to]);
      to = strtim(argv[to]);
      if (to < (WFDB_Time) 0) to = -to;
    }
    nsamp = (to > 0L) ? to - from : -1L;
    nsamporig=nsamp;
    fprintf(stderr,"Fs: %f\n",InputFileSampleFrequency);

/////////////////////////////////////////////////////////////////
// datalength should be scaled by SAMPLE_RATE; changed 18/05/2011
/////////////////////////////////////////////////////////////////

    datalength = strtim("e")*SAMPLE_RATE/InputFileSampleFrequency;

/////////////////////////////////////////////////////////////////
// spm should be scaled by SAMPLE_RATE; changed 18/05/2011
/////////////////////////////////////////////////////////////////

//    int minutes, spm = 60 * InputFileSampleFrequency, sp5s = 5 * InputFileSampleFrequency;
//    int buf5s[5 * (int)InputFileSampleFrequency], ibuf5s

    int minutes, spm = 60 * SAMPLE_RATE;

    int j;



    // Setup for output annotations
//    for (leadi = 0; leadi < nsig; leadi++)
//      for (j = 0; j < strlen(s[leadi].desc); j++)
//       if (s[leadi].desc[j] == ' ') {
//          s[leadi].desc[j] = '\0';
//          break;
//        }

    onsig = 0;
    for (leadi=0;leadi<nsig;leadi++)
	for (j=0;j<strlen(s[leadi].desc);j++)
	    s[leadi].desc[j]=toupper(s[leadi].desc[j]); // ensure all upper case

    for (leadi = 0; leadi < nsig; leadi++)
      for (leadj = 0; leadj < 20; leadj++)
        if (strcmp(s[leadi].desc, ecglead[leadj]) == 0) { // look for exact string match
          ADCZero = s[leadi].adczero;
          ADCUnit = s[leadi].gain;




//          sprintf(tempname, "%s%d", "epltd", onsig);
//          sprintf(tempname, "%s%d", "epltd", leadi);
// Alistair 01/07/2013: changed to output with lead name
	  sprintf(tempname, "%s%s", "epltd", ecglead[leadj]);
          onsig++;
          a[0].name = tempname;
          a[0].stat = WFDB_WRITE;

          printf("\nECG: %s, lead: %s, annot file: %s\n", record, ecglead[leadj], a[0].name);

          if (annopen(record, a, 1) < 0) {
            myquit();
            fprintf(stderr,"Couldn't open annotation file\n");
            continue;
          }

          // Initialize sampling frequency adjustment.

          NextSample(ecg, nsig, InputFileSampleFrequency, SAMPLE_RATE, 1);

          // Initialize beat detection and classification.

          ResetBDAC();

///////////////////////////////////////////////////////
// changed SampleCount = 0 to from: changed 18/05/2011
///////////////////////////////////////////////////////

          SampleCount = from*SAMPLE_RATE/InputFileSampleFrequency;
          next_minute = SampleCount+spm;
          minutes = 0;
//          ibuf5s = 0;
//          filtold = dataold = 0;
//          for (j = 0; j < 40; j++) {
//            ecgbuf[j] = 0;
//            sortbuf[j] = 0;
//          }
//          ecgbufp = 0;

          // Read data from MIT/BIH file until there is none left.

          while (NextSample(ecg, nsig, InputFileSampleFrequency, SAMPLE_RATE, 0) >= 0) {
            ++SampleCount;
            // Set baseline to 0 and resolution to 5 mV/lsb (200 units/mV)

            lTemp = ecg[leadi] - ADCZero;
            lTemp = lTemp*(200.0/ADCUnit);

            ecg[leadi] = lTemp;


            /*                      filt=filtold*0.9913112+ecg[leadi]*0.9956556-dataold*0.9956556;  // High pass 0.5Hz filter
                                    filtold=filt;
                                    dataold=ecg[leadi];

                                    buf5s[ibuf5s]=filt;
                                    //                      buf5s[ibuf5s]=ecg[leadi];
                                    ibuf5s++;
                                    if (ibuf5s>=sp5s)
                                    ibuf5s=0;
            */
            // Pass sample to beat detection and classification.
//            old = ecgbuf[ecgbufp];
//            ecgbuf[ecgbufp] = ecg[leadi];
//            ecgbufp++;
//            if (ecgbufp >= 40)
//              ecgbufp = 0;
            //                      for (i=0;i<40;i++)
            //                              sortbuf[i]=ecgbuf[i];
            //                      hpsort(40L, sortbuf-1);
//            insertsort(sortbuf, 40, old, ecg[leadi]);
//            ecg[leadi] = ecg[leadi] - sortbuf[20];

            delay = BeatDetectAndClassify(ecg[leadi], &beatType, &beatMatch);

            // If a beat was detected, annotate the beat location
            // and type.

            if (delay != 0) {
              DetectionTime = SampleCount - delay;
				DetectionTime *= InputFileSampleFrequency ;
				DetectionTime /= SAMPLE_RATE ;

              // Convert sample count to input file sample
              // rate.

              annot.time = DetectionTime;
              annot.anntyp = beatType;
              /*                            tempk=mykurtosis(buf5s,sp5s);
                                            if (tempk>127) {
                                            tempk=127;
                                            //                                      annot.anntyp=NOISE;
                                            }
                                            annot.subtyp = (char)tempk;
                                            if (annot.subtyp<5)
                                            annot.anntyp=NOISE;
              */
              annot.subtyp = 0;
              annot.chan = leadi;
              annot.num = leadj + 1;
              annot.aux = NULL;
              //                            if (annot.subtyp>=5)
              putann(0, &annot);
            }
            timecount = SampleCount;
            if ((timecount) >= next_minute) {
              (void) fprintf(stderr, ".");
              (void) fflush(stderr);
              if (++minutes >= 60) {
                (void) fprintf(stderr, "%ld\n", next_minute / spm);
                minutes = 0;
              }
              next_minute += spm;
            }
            if (timecount > datalength)
              break;
          }


          // Reset database after record is done.

          //                wfdbquit() ;



          isigsettime(from);
	  nsamp=nsamporig;
          break;
        }


    printf("Processing end \n");
    myquit();



    //#if 0
    /* This code is obsolete.  The annotation files are always
       written into "<record>.ate" in the current directory.
       They do not need to be copied in order to be read by bxbep,
       if the WFDB path includes both the current current directory
       and the one containing the .atr reference annotation files.
    */

    // Copy "atest.<record>" to "<record>.ate" for future ascess.
    // (This is necessary for PC files)

    /*          sprintf(fname,"%s.ate",record) ;
                newAnn0 = fopen(fname,"rb") ;
                sprintf(fname,"%s%s.ate",ECG_DB_PATH,record) ;
                newAnn1 = fopen(fname,"wb") ;

                // Copy byte image of annotation file in this
                // directory to a correctly named file in the
                // database directory.

                while(fread(&byte,sizeof(char),1,newAnn0) == 1)
                fwrite(&byte,sizeof(char),1,newAnn1) ;

                fclose(newAnn0) ;
                fclose(newAnn1) ;
    */
    //#endif
  }
}

/**********************************************************************
        NextSample reads MIT/BIH Arrhythmia data from a file of data
        sampled at ifreq and returns data sampled at ofreq.  Data is
        returned in vout via *vout.  NextSample must be initialized by
        passing in a nonzero value in init.  NextSample returns -1 when
   there is no more data left.
***********************************************************************/

int NextSample(int *vout, int nosig, int ifreq,
               int ofreq, int init) {
  int i;
  static int m, n, mn, ot, it, vv[WFDB_MAXSIG], v[WFDB_MAXSIG], rval;

  if (init) {
    i = gcd(ifreq, ofreq);
    m = ifreq / i;
    n = ofreq / i;
    mn = m*n;
    ot = it = 0;
    getvec(vv);
    if(nsamp!=-1L && --nsamp<1)
      return -1;

    // Change WFDB_INVALID_SAMPLE value to 0
    for (i = 0; i < nosig; i++)
      if (vv[i] < WFDB_INVALID_SAMPLE + 10)
        vv[i] = 0;

    rval = getvec(v);
    if(nsamp!=-1L && --nsamp<1)
      return -1;

    for (i = 0; i < nosig; i++)
      if (v[i] < WFDB_INVALID_SAMPLE + 10)
        v[i] = vv[i]; //=0;
  } else {
    while (ot > it) {
      for (i = 0; i < nosig; ++i)
        vv[i] = v[i];
      rval = getvec(v);
      if(nsamp!=-1L && --nsamp<1)
        return -1;

      for (i = 0; i < nosig; i++)
        if (v[i] < WFDB_INVALID_SAMPLE + 10)
          v[i] = vv[i]; //=0;

      if (it > mn) {
        it -= mn;
        ot -= mn;
      }
      it += n;
    }
    for (i = 0; i < nosig; ++i)
      vout[i] = vv[i] + (ot % n)*(v[i] - vv[i]) / n;
    ot += m;
  }

  return (rval);
}

// Greatest common divisor of x and y (Euclid's algorithm)

int gcd(int x, int y) {
  while (x != y) {
    if (x > y) x -= y;
    else y -= x;
  }
  return (x);
}


char *prog_name(char *s)
     
{
  char *p = s + strlen(s);

#ifdef MSDOS
  while (p >= s && *p != '\\' && *p != ':') {
    if (*p == '.')
      *p = '\0'; /* strip off extension */
    if ('A' <= *p && *p <= 'Z')
      *p += 'a' - 'A'; /* convert to lower case */
    p--;
  }
#else
  while (p >= s && *p != '/')
    p--;
#endif
  return (p + 1);
}


