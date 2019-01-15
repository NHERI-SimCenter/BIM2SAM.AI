/*------------------------------------------------------*
| This code is used to create OpenSees tcl files        |
| Inputs:  BIM/SAM/EVT/EDP                              |
| Authors: Charles Wang,  UC Berkeley c_w@berkeley.edu  |
|          Frank McKenna, UC Berkeley                   |
| Date:    01/15/2019                                   |
*------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include "OpenSeesTclBuilder.h"

int main(int argc, char **argv)
{

  if (argc != 6 && argc != 7) {
    printf("HELLO\n");
    printf("ERROR: correct usage: createTcl fileNameBIM fileNameSAM fileNameEVENT filenameEDP TCLdir\n");
    exit(0);
  }

  char *filenameBIM = argv[1];
  char *filenameSAM = argv[2];
  char *filenameEVENT = argv[3];
  char *filenameEDP = argv[4];
  char *filenameTCL = argv[5];

  OpenSeesTclBuilder *thePreprocessor = new OpenSeesTclBuilder();

  string ModelType = thePreprocessor->getModelType(filenameSAM);// continuum or beamcolumn?
  

if (!ModelType.compare("beamcolumn"))
{
  std::cout << "Model type: " << ModelType << endl;
  thePreprocessor->createInputFileBeamColumn(filenameBIM, 
				     filenameSAM, 
				     filenameEVENT,
				     filenameEDP,
				     filenameTCL);

}else if(!ModelType.compare("continuum")){
  std::cout << "Model type: " << ModelType << endl;
  if (argc == 6) {

    thePreprocessor->createInputFile(filenameBIM, 
				     filenameSAM, 
				     filenameEVENT,
				     filenameEDP,
				     filenameTCL);
  } else {

    thePreprocessor->createInputFile(filenameBIM, 
				     filenameSAM, 
				     filenameEVENT,
				     filenameEDP,
				     filenameTCL,
				     argv[6]);
  }
}else{
  std::cout << "No matching model type." << endl;
}

  delete thePreprocessor;
  
  return 0;
}

