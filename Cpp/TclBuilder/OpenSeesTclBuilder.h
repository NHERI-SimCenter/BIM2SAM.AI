/*------------------------------------------------------*
| A class to create OpenSees tcl files                  |
| Inputs:  BIM/SAM/EVT/EDP                              |
| Authors: Charles Wang,  UC Berkeley c_w@berkeley.edu  |
|          Frank McKenna, UC Berkeley                   |
| Date:    01/15/2019                                   |
*------------------------------------------------------*/
#ifndef OPENSEES_TCLBUILDER_H
#define OPENSEES_TCLBUILDER_H
class json_t;
#include <fstream>
#include <vector>
#include <string>
#include <cstring>
#include <jansson.h>
using namespace::std;

class OpenSeesTclBuilder {

 public:
  OpenSeesTclBuilder();
  ~OpenSeesTclBuilder();

  int writeRV(const char *BIM,
	      const char *SAM,
	      const char *EVENT,
	      const char *tcl);

  int createInputFile(const char *BIM,
		      const char *SAM,
		      const char *EVENT,
		      const char *EDP,
		      const char *tcl);

  int createInputFile(const char *BIM,
		      const char *SAM,
		      const char *EVENT,
		      const char *EDP,
		      const char *tcl,
		      const char *UQvariables);
  int createInputFileBeamColumn(const char *BIM,
		      const char *SAM,
		      const char *EVENT,
		      const char *EDP,
		      const char *tcl);
          

  int processMaterials(ofstream &out);
  int processSections(ofstream &out);
  int processNodes(ofstream &out);
  int cookGeometry(ofstream &out);
  int cookDriver(ofstream &out);
  int cookMaterial(ofstream &out);
  int processElements(ofstream &out);
  int processDamping(ofstream &out);
  int processEvents(ofstream &s);
  int processEvent(ofstream &s, 
		   json_t *event, 
		   int &numPattern, 
		   int &numSeries);

  int getNode(int cline, int floor);
  int findNodesOnStraigntLine(double pt1[], double pt2[], int nodesOnline[]);
  int getNodeCrdByTag(int nodeTag, double pt[]);

  string getModelType(const char *SAM){
    filenameSAM = (char *)malloc((strlen(SAM) + 1) * sizeof(char));
    strcpy(filenameSAM, SAM);
    //printf("%s\n", filenameSAM);
    json_error_t error;
    rootSAM = json_load_file(filenameSAM, 0, &error);
    rootSAM = json_object_get(rootSAM, "Structural Analysis Model");
    if (rootSAM==0){
      rootSAM = json_object_get(json_load_file(filenameSAM, 0, &error), "StructuralAnalysisModel");
    }

    json_t *sections = json_object_get(json_object_get(rootSAM, "properties"),"sections");
    if (json_array_size(sections)>0)
      return "beamcolumn";
 
    return "continuum";

  }

  double getThickness(json_t *rootBIM, int sectionNum){
    /*
    filenameBIM = (char *)malloc((strlen(BIM) + 1) * sizeof(char));
    strcpy(filenameBIM, BIM);
    json_error_t error;
    json_t *rootBIM_tmp = json_load_file(filenameBIM, 0, &error);
    */
    json_t *SI = json_object_get(rootBIM, "StructuralInformation");
    json_t *properties = json_object_get(SI, "properties");
    json_t *wallsections = json_object_get(properties, "wallsections");
    json_t *firstSection = (json_array_get(wallsections, sectionNum));
    double thickness = json_number_value(json_object_get(firstSection, "thickness"));

    return thickness;

  }

  double getVerticalLoad(){

    json_error_t error0;
    rootEVENT = json_load_file((filenameEVENT), 0, &error0);
    json_t *EVENTS = json_object_get(rootEVENT, "Events");
    json_t *event = json_array_get(EVENTS,0);
    json_t *verticalLoad = json_array_get(json_object_get(event, "loads"),0);
    json_t *position = json_array_get(json_object_get(verticalLoad, "positions"),0);
    double P = json_number_value( json_array_get(json_object_get(position, "scales"),0));

    return P;

  }

  void getPeaks(vector<double> &peaks)
  {
    json_t *EVENTS = json_object_get(rootEVENT, "Events");
    json_t *event = json_array_get(EVENTS,0);
    json_t *timeseries = json_array_get(json_object_get(event, "timeSeries"),3);
    json_t *values = json_object_get(timeseries, "values");
    size_t index;
    json_t *value;
    double x1;
    double x2;
    double x3;
    json_array_foreach(values, index, value)
    {
      x3 = json_number_value( json_array_get(json_array_get(values,index),0));
      if (index<1)
        x1 = x3;
      if (index==1)
        x2 = x3;
      if (index>1)
      {
        if((x1-x2)*(x3-x2)>0)
          peaks.push_back(x2);
        x1 = x2;
        x2 = x3;
      }

    }

  }

  double getMoment(){

    json_error_t error0;
    rootEVENT = json_load_file((filenameEVENT), 0, &error0);
    json_t *EVENTS = json_object_get(rootEVENT, "Events");
    json_t *event = json_array_get(EVENTS,0);
    json_t *verticalLoad = json_array_get(json_object_get(event, "loads"),1);
    json_t *position = json_array_get(json_object_get(verticalLoad, "positions"),1);
    double M_over_L = json_number_value( json_array_get(json_object_get(position, "scales"),0));

    return M_over_L * getWallLength();

  }

  double getWallLength(){

    json_t *SI = json_object_get(rootBIM, "StructuralInformation");
    json_t *properties = json_object_get(SI, "properties");
    json_t *wallsections = json_object_get(properties, "wallsections");
    json_t *firstSection = (json_array_get(wallsections, 0));
    double length = json_number_value(json_object_get(firstSection, "length"));

    return length;

  }

 private:
  char *filenameBIM;
  char *filenameSAM;
  char *filenameEVENT;
  char *filenameEDP;
  char *filenameTCL;
  char *filenameUQ;

  json_t *rootBIM;
  json_t *rootSAM;
  json_t *rootEDP;
  json_t *rootEVENT;
  json_t *mapping;

  json_t *nodes, *elements;
  double volumeOfWall;

  

  int analysisType;
  int numSteps;
  double dT;
  int nStory;   //number of stories

  int NDM;
  int NDF;
};

#endif // OPENSEES_TCLBUILDER_H
