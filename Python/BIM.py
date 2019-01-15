from collections import namedtuple
import json
from pprint import pprint
import math
import os
import numpy as np




class BIM:
    """A calss of BIM model for concrete shear wall"""

    Floor = namedtuple('Floor', ['name', 'elevation'])
    Cline = namedtuple('Cline', ['name', 'location'])

    Steel = namedtuple('Steel', ['name', 'type', 'masspervolume', 'fy', 'E'])
    Concrete = namedtuple('Concrete', ['name', 'type', 'masspervolume', 'fpc', 'E', 'nu'])
    LongitudinalRebar = namedtuple('LongitudinalRebar', ['material', 'numBarsThickness','barArea','spacing','cover'])
    TransverseRebar = namedtuple('TransverseRebar', ['material', 'numBarsThickness','barArea','spacing','cover'])
    LongitudinalBoundaryElementRebar = namedtuple('LongitudinalBoundaryElementRebar', ['material', 'numBarsLength',\
                                                  'numBarsThickness','barArea','cover'])
    TransverseBoundaryElementRebar = namedtuple('TransverseBoundaryElementRebar', ['material', 'numBarsLength',\
                                                  'numBarsThickness','barArea','spacing'])
    
    Wallsection = namedtuple('Wallsection', ['name', 'type', 'material', 'length', 'thickness',\
                                             'boundaryElementLength','longitudinalRebar',\
                                             'transverseRebar','longitudinalBoundaryElementRebar',
                                             'transverseBoundaryElementRebar'])
    

                        
    def __init__(self, BIMFileName):
        self.BIMFileName = BIMFileName
        # load BIM json
        with open(BIMFileName) as f:
            BIM = json.load(f)
        self.stories = BIM['GeneralInformation']['stories']
        self.height = BIM['GeneralInformation']['height']

        self.floors = BIM['StructuralInformation']['layout']['floors']
        self.clines = BIM['StructuralInformation']['layout']['clines']

        self.walls = BIM['StructuralInformation']['geometry']['walls']

        self.materials = BIM['StructuralInformation']['properties']['materials']
        self.wallsections = BIM['StructuralInformation']['properties']['wallsections']

        firstSection = BIM['StructuralInformation']['properties']['wallsections'][0]
        self.section = firstSection

        self.thickness = self.section['thickness']
        self.length = self.section['length']
        self.boundaryLength = self.section['boundaryElementLength']
        self.webLength = self.section['length'] - 2.0 * self.section['boundaryElementLength']

        self.StructuralInformation = BIM['StructuralInformation']

        self.features = []
  
        #pprint(self.walls[0])

    def getWebConcreteFeatures(self,section):
            # get web concrete 
            conName = section['material']
            for mat in self.materials:
                if (mat['name'] == conName):
                    masspervolumeConc = mat['masspervolume']
                    fc = mat['fpc']*(-1)
                    Ec = mat['E']
                    nu = mat['nu']
                    epsc = mat['eps0']*(-1)
                    eps = epsc
                    epscu = mat['epsU']*(-1)
                    fcu = mat['fpcU']*(-1)
                    ratio = mat['alpha']
                    ft = mat['ft']
                    Ets = mat['Ets']
                    return [Ec, fc]
                    break

    def getBEConcreteFeatures(self,section):
            # get web concrete 
            conName = section['material']
            for mat in self.materials:
                if (mat['name'] == conName):
                    masspervolumeConc = mat['masspervolume']
                    fc = mat['fpc']*(-1)
                    Ec = mat['E']
                    nu = mat['nu']
                    epsc = mat['eps0']*(-1)
                    eps = epsc
                    epscu = mat['epsU']*(-1)
                    fcu = mat['fpcU']*(-1)
                    ratio = mat['alpha']
                    ft = mat['ft']
                    Ets = mat['Ets']
                    return [Ec, fc]
                    break            


    def getWebRebarFeatures(self,section):
            # get web rebar 
            lweb = section['length']
            lBE = section['boundaryElementLength']
            webVertRebarName = section['longitudinalRebar']['material']
            webVertnumThic = section['longitudinalRebar']['numBarsThickness']
            webVertbarArea = section['longitudinalRebar']['barArea']
            webVertspacing = section['longitudinalRebar']['spacing']
            webVertcover = section['longitudinalRebar']['cover']
            areaFiber = webVertbarArea
            dFiber = (webVertbarArea / 3.14159)**0.5*2
            numBars = int(math.floor((lweb - webVertcover*2 - dFiber) / (webVertspacing+dFiber))+1)
            coordX = (webVertspacing*(numBars-1) + dFiber*numBars)/2 + webVertspacing + dFiber/2
            coordY = 0.0#t/2-webVertcover
            features = []
            for mat in self.materials:
                if (mat['name'] == webVertRebarName):
                    masspervolumeVertRebar = mat['masspervolume']
                    E = mat['E']
                    fy = mat['fy']
                    fu = mat['fu']
                    epsu = mat['epsu']
                    break
            for nf in range(0,numBars):
                    coordX -= (webVertspacing+dFiber)
                    for nfT in range(0,webVertnumThic):
                        #feature = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 4)}
                        feature = [coordX, coordY, E, fy, dFiber]
                        features.append(feature)

            return features


    def getBERebarFeatures(self,section):
            # get BE rebar 
            lweb = section['length']
            lbe = section['boundaryElementLength']
            try:
                tm = section['longitudinalBoundaryElementRebar']
            except:
                features = []
                print("didn't find boundary rebar")
                return features

            beVertRebarName = section['longitudinalBoundaryElementRebar']['material']
            beVertnumThic = section['longitudinalBoundaryElementRebar']['numBarsThickness']
            beVertnumLen = section['longitudinalBoundaryElementRebar']['numBarsLength']
            beVertbarArea = section['longitudinalBoundaryElementRebar']['barArea']
            beVertcover = section['longitudinalBoundaryElementRebar']['cover']
            for mat in self.materials:
                if (mat['name'] == beVertRebarName):
                    masspervolumeVertRebar = mat['masspervolume']
                    Ebe = mat['E']
                    fybe = mat['fy']
                    fube = mat['fu']
                    epsube = mat['epsu']
                    epsrbe = mat['epsr']
                    break
            areaFiber = beVertbarArea
            dFiber = (beVertbarArea / 3.14159)**0.5*2
            numBars = int(beVertnumLen)
            if numBars <= 1:
                    numBars = 1
                    beVertspacing = (lbe-beVertcover*2-dFiber*numBars)/(numBars)
            else:
                    beVertspacing = (lbe-beVertcover*2-dFiber*numBars)/(numBars-1)
            coordX = lweb/2 + beVertcover - beVertspacing - dFiber/2
            coordY = 0
            features = []
            for nf in range(0,numBars):
                    coordX += (beVertspacing+dFiber)
                    for nfT in range(0,beVertnumThic):
                        feature = [coordX, coordY, Ebe, fybe, dFiber]
                        features.append(feature)
                        feature = [-coordX, coordY, Ebe, fybe, dFiber]
                        features.append(feature)

            return features


    def getWallFeatures(self,walls):
        for wall in walls:
            floors = wall['floor']
            clines = wall['cline']
            elevations = []
            clineLocs = []
            for floor in self.floors:
                if floors[0] == floor['name']:
                    elevations.append(floor['elevation'])
                if floors[1] == floor['name']:
                    elevations.append(floor['elevation'])
            for cline in self.clines:
                if clines[0] == cline['name']:
                    clineLocs.append(cline['location'])
                if clines[1] == cline['name']:
                    clineLocs.append(cline['location'])

            height = math.fabs(elevations[0]-elevations[1])
            bottom = min(elevations)

            x0 = min(clineLocs[0][0], clineLocs[1][0]) 
            length = math.fabs(clineLocs[0][0] - clineLocs[1][0])
            x0 = x0 - length * 0.5 # move the x-center of the wall to (0,0)

            xc = x0 + length * 0.5
            yc = bottom + height * 0.5

            segment = wall['segment'][0]
            sectionName = segment['section']
            for section in self.wallsections:
                if sectionName == section['name']:
                    thickness = section['thickness']
                    #length = section['length']
                    lenBE = section['boundaryElementLength']
                    lenWeb = length - 2.0 * lenBE
                    z0 = 0.0 - thickness * 0.5

                    # web concrete
                    matType = 1.0
                    Ec, fc = self.getWebConcreteFeatures(section)
                    zc = z0 + thickness * 0.5
                    featuresConcWeb = [xc, yc, zc, lenWeb, height, thickness, matType, Ec, fc]
                    self.features.append(featuresConcWeb)
                    #print(featuresConcWeb)
                    # boundary concrete, right
                    matType = 1.0
                    Ec, fc = self.getBEConcreteFeatures(section)
                    xc = x0 + length - lenBE * 0.5
                    yc = yc
                    featuresConcBE = [xc, yc, zc, lenBE, height, thickness, matType, Ec, fc]
                    self.features.append(featuresConcBE)
                    #print(featuresConcBE)
                    # boundary concrete, left
                    matType = 1.0
                    Ec, fc = self.getBEConcreteFeatures(section)
                    xc = x0 + lenBE * 0.5
                    yc = yc
                    featuresConcBE = [xc, yc, zc, lenBE, height, thickness, matType, Ec, fc]
                    self.features.append(featuresConcBE)
                    #print(featuresConcBE)
                    # web vertical rebar
                    matType = 2.0
                    WebRebarFeatures = self.getWebRebarFeatures(section)
                    #print("web vertical rebar: ")
                    for f in WebRebarFeatures:
                        coordX, coordY, E, fy, dFiber = f
                        xc = coordX
                        yc = yc
                        zc = coordY
                        featuresRebarWeb = [xc, yc, zc, dFiber, height, dFiber, matType, E, fy]
                        self.features.append(featuresRebarWeb)
                        #print(featuresRebarWeb)  
                    # boundary vertical rebar
                    matType = 2.0
                    BERebarFeatures = self.getBERebarFeatures(section)
                    #print("BE vertical rebar: ")
                    for f in BERebarFeatures:
                        coordX, coordY, E, fy, dFiber = f
                        xc = coordX
                        yc = yc
                        zc = coordY
                        featuresRebarBE = [xc, yc, zc, dFiber, height, dFiber, matType, E, fy]
                        self.features.append(featuresRebarBE)
                        #print(featuresRebarBE)  
                    break
                

    def getFeatures(self, nDimRandomProj=512):
        self.getWallFeatures(self.walls)

        maxEConc = 4000.
        maxESteel = 29000.
        maxFConc = 6.0
        maxFSteel = 90.0

        # get the raw features
        rawFeatures = np.asarray(self.features) 

        # normalization
        rawFeatures = np.absolute(rawFeatures)
        indConcrete = np.where(rawFeatures[:,6] == 1.0) 
        indSteel = np.where(rawFeatures[:,6] == 2.0) 
        rawFeatures[indConcrete,7] = rawFeatures[indConcrete,7] / maxEConc
        rawFeatures[indSteel,7] = rawFeatures[indSteel,7] / maxESteel
        rawFeatures[indConcrete,8] = rawFeatures[indConcrete,8] / maxFConc
        rawFeatures[indSteel,8] = rawFeatures[indSteel,8] / maxFSteel


        # random projection 
        [m,nDimFeature] = rawFeatures.shape
        randomProjMatrix = np.random.rand(nDimFeature,nDimRandomProj)

        features = np.dot(rawFeatures, randomProjMatrix)



        features = features.sum(axis=0)
        #features = np.cos(features)
        return features

    def getSimpleFeatures(self):
        features = []
        features.append(self.height)
        features.append(self.length)
        features.append(self.thickness)
        for mat in self.materials:
                if (mat['name'] == 'Concrete'):
                    masspervolumeConc = mat['masspervolume']
                    fc = mat['fpc']*(-1)
                    Ec = mat['E']
                    nu = mat['nu']
                    epsc = mat['eps0']*(-1)
                    eps = epsc
                    epscu = mat['epsU']*(-1)
                    fcu = mat['fpcU']*(-1)
                    ratio = mat['alpha']
                    ft = mat['ft']
                    Ets = mat['Ets']
                    break
        features.append(Ec)
        features.append(-fc)
        return(features)