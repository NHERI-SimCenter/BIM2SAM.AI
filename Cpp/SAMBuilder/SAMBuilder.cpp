/*------------------------------------------------------*
| This code is used to create SAM files                 |
| Inputs:  BIM                                          |
| Authors: Charles Wang,  UC Berkeley c_w@berkeley.edu  |
|          Frank McKenna, UC Berkeley                   |
| Date:    01/15/2019                                   |
*------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <cctype>
#include "ConcreteShearWall.h"




int main(int argc, char **argv)
{


  if (argc != 9)
  {
    printf("ERROR: correct usage: SAMBuilder fileNameBIM fileNameSAM nL nH beta An Ap Bn \n");
    // nL is the number of element in the length-direction of a section
    // nH is the number of element in the height-direction of a section
    exit(0);
  }

  char *filenameBIM = argv[1];
  char *filenameSAM = argv[2];
  int nL = atoi(argv[3]);
  int nH = atoi(argv[4]);

  double beta = atof(argv[5]);
  double An = atof(argv[6]);
  double Ap = atof(argv[7]);
  double Bn = atof(argv[8]);

  char *filenameEVENT = 0;



  ConcreteShearWall *theBuilding = new ConcreteShearWall();
  theBuilding->initConcrete(beta, An, Ap, Bn);
  theBuilding->readBIM(filenameEVENT, filenameBIM);
  theBuilding->writeSAM(filenameSAM, nL, nH);

  printf("SAM file created successfully. \n");

  return 0;
}
