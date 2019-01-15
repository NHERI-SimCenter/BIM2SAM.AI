from collections import namedtuple
import json
from pprint import pprint
from math import floor, isnan
import os
from BIM import BIM




class BeamColumnSAM:
    """A calss of Beam-Column SAM model for concrete shear wall"""
    '''
    BIMFileName = ''
    stories = 0
    height = 0
    BIM = 0
    SAM = 0

    mats = []
    sections = []
    nodes = []
    elements = []
    sectionList = []

    numWebY = 1 #num of ele in Y direction, web
    numBEY = 1 #num of ele in Y direction, BE core
    numBECRY = 1 #num of ele in Y direction, BE right cover
    numBECLY = 1 #num of ele in Y direction, BE left cover
    numBECTY = 1 #num of ele in Y direction, BE top cover
    numBECBY = 1 #num of ele in Y direction, BE bottom cover
    nInt = 1 # num of Int
    '''
    def __init__(self):
        self.BIMFileName = ''
        self.stories = 0
        self.height = 0
        self.BIM = 0
        self.SAM = 0

        self.mats = []
        self.sections = []
        self.nodes = []
        self.elements = []
        self.sectionList = []

        self.numWebY = 1 #num of ele in Y direction, web
        self.numBEY = 1 #num of ele in Y direction, BE core
        self.numBECRY = 1 #num of ele in Y direction, BE right cover
        self.numBECLY = 1 #num of ele in Y direction, BE left cover
        self.numBECTY = 1 #num of ele in Y direction, BE top cover
        self.numBECBY = 1 #num of ele in Y direction, BE bottom cover
        self.nInt = 1 # num of Int


    def setMesh(self,numWebYt, numBEYt,numBECRYt,numBECLYt,numBECTYt,numBECBYt,nIntt):
        self.numWebY = numWebYt #num of ele in Y direction, web
        self.numBEY = numBEYt #num of ele in Y direction, BE core
        self.numBECRY = numBECRYt #num of ele in Y direction, BE right cover
        self.numBECLY = numBECLYt #num of ele in Y direction, BE left cover
        self.numBECTY = numBECTYt #num of ele in Y direction, BE top cover
        self.numBECBY = numBECBYt #num of ele in Y direction, BE bottom cover
        self.nInt = nIntt

    def readBIM(self, BIMFileName):
        self.BIMFileName = BIMFileName
        self.BIM = BIM(BIMFileName)
        
    
    def createSAM(self):

        SAM = {'StructuralAnalysisModel':{'BIM':os.path.basename(self.BIMFileName)}}
        SAM['StructuralAnalysisModel']['description'] = 'distributed plasticity frame model of RC wall'
        SAM['StructuralAnalysisModel']['engineer'] = 'NHERI SimCenter'
        SAM['StructuralAnalysisModel']['units'] = {"force": "kip",\
		                                            "length": "in",\
		                                            "time": "sec",\
		                                            "temperature": "F"}
        

        matTag = 0
        secTag = 0
        nodeTag = 0
        eleTag = 0

        for section in self.BIM.wallsections:
            l = section['length']
            t = section['thickness']
            tbe = t
            lbe = section['boundaryElementLength']
            lweb = l-2*lbe

            sectionList = []

            # get web concrete 
            conName = section['material']
            for mat in self.BIM.materials:
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
                    break
            '''
            #"Ec": 4603.88, "fc": -6.526, "epsc": -0.002835, "fcu": -1.305, "epscu": -0.008, "ratio": 0.1, "ft": 0.606, "Ets": 230.24
            eps = 2*(fc*1000)/57000/((-fc*1000)**0.5)
            epsc = eps
            fcu = 0.2*fc
            epscu = -0.008
            ratio = 0.1
            ft = 0.23717*(-fc)**0.5
            Ets = 0.05*57*(-fc*1000)**0.5
            '''

            # get BE concrete
            for mat in self.BIM.materials:
                if (mat['name'] == conName+'BE'):
                    masspervolumeConc = mat['masspervolume']
                    fcBE = mat['fpc']*(-1)
                    EcBE = mat['E']
                    nuBE = mat['nu']
                    epscBE = mat['eps0']*(-1)
                    epscuBE = mat['epsU']*(-1)
                    fcuBE = mat['fpcU']*(-1)
                    ratioBE = mat['alpha']
                    ftBE = mat['ft']
                    EtsBE = mat['Ets']
                    break
            '''
            #"Ec": 4603.88, "fc": -6.526, "epsc": -0.002835, "fcu": -1.305, "epscu": -0.008, "ratio": 0.1, "ft": 0.606, "Ets": 230.24
            epsBE = 2*(fcBE*1000)/57000/((-fcBE*1000)**0.5)
            epscBE = epsBE
            fcuBE = 0.2*fcBE
            epscuBE = -0.008
            ratioBE = 0.1
            ftBE = 0.23717*(-fcBE)**0.5
            EtsBE = 0.05*57*(-fcBE*1000)**0.5
            '''

            webVertRebarName = section['longitudinalRebar']['material']
            webVertnumThic = section['longitudinalRebar']['numBarsThickness']
            webVertbarArea = section['longitudinalRebar']['barArea']
            webVertspacing = section['longitudinalRebar']['spacing']
            webVertcover = section['longitudinalRebar']['cover']
            for mat in self.BIM.materials:
                if (mat['name'] == webVertRebarName):
                    masspervolumeVertRebar = mat['masspervolume']
                    E = mat['E']
                    fy = mat['fy']
                    fu = mat['fu']
                    epsu = mat['epsu']
                    break
            
            try:
                beVertRebarName = section['longitudinalBoundaryElementRebar']['material']
                beVertnumThic = section['longitudinalBoundaryElementRebar']['numBarsThickness']
                beVertnumLen = section['longitudinalBoundaryElementRebar']['numBarsLength']
                beVertbarArea = section['longitudinalBoundaryElementRebar']['barArea']
                beVertcover = section['longitudinalBoundaryElementRebar']['cover']
                for mat in self.BIM.materials:
                    if (mat['name'] == beVertRebarName):
                        masspervolumeVertRebar = mat['masspervolume']
                        Ebe = mat['E']
                        fybe = mat['fy']
                        fube = mat['fu']
                        epsube = mat['epsu']
                        epsrbe = mat['epsr']
                        break
            except:
                # didn't find boundary element
                Ebe = float('nan')
                fybe = float('nan')

            
            for n in range(0,self.nInt):
                # web concrete mat
                matWebConc = {}
                matWebConc['name'] = str(matTag + 1)
                matWebConc['type'] = 'Concrete02'
                matWebConc['Ec'] = Ec
                matWebConc['fc'] = fc
                matWebConc['epsc'] = epsc
                matWebConc['fcu'] = fcu
                matWebConc['epscu'] = epscu
                matWebConc['ratio'] = ratio
                matWebConc['ft'] = ft
                matWebConc['Ets'] = Ets
                self.mats.append(matWebConc)

                # BE concrete
                matBEConc = {}
                matBEConc['name'] = str(matTag + 2)
                matBEConc['type'] = 'Concrete02'
                matBEConc['Ec'] = EcBE
                matBEConc['fc'] = fcBE
                matBEConc['epsc'] = epscBE
                matBEConc['fcu'] = fcuBE
                matBEConc['epscu'] = epscuBE
                matBEConc['ratio'] = ratioBE
                matBEConc['ft'] = ftBE
                matBEConc['Ets'] = EtsBE
                self.mats.append(matBEConc)

                #{"name": "21", "type": "Steel02", "E": 29000, "fy": 84.64, "b": 0.00417547, "R0": 20, "cR1": 0.925, "cR2": 0.15, "a1": 0, "a2": 1, "a3": 0, "a4": 1, "sigini": 0},
                # Web rebar
                matWebRebar = {}
                matWebRebar['name'] = str(matTag + 3)
                matWebRebar['type'] = 'Steel02'
                matWebRebar['E'] = E
                matWebRebar['fy'] = fy
                matWebRebar['b'] = 0.005 # assumed
                matWebRebar['R0'] = 20 
                matWebRebar['cR1'] = 0.925
                matWebRebar['cR2'] = 0.15
                matWebRebar['a1'] = 0.0
                matWebRebar['a2'] = 1.0
                matWebRebar['a3'] = 0.0
                matWebRebar['a4'] = 1.0
                matWebRebar['sigini'] = 0.0
                self.mats.append(matWebRebar)
                # {"name": "31", "type": "MinMaxMaterial", "material": "21", "epsMin": -0.008, "epsMax": 0.0234},
                matWebRebar = {}
                matWebRebar['name'] = str(matTag + 4)
                matWebRebar['type'] = 'MinMaxMaterial'
                matWebRebar['material'] = str(matTag + 3)
                matWebRebar['epsMin'] = -0.008 # assumed
                matWebRebar['epsMax'] = 0.0785 # assumed
                self.mats.append(matWebRebar)

                # BE rebar
                if lbe > 0.000001: 
                    matBERebar = {}
                    matBERebar['name'] = str(matTag + 5)
                    matBERebar['type'] = 'Steel02'
                    matBERebar['E'] = Ebe
                    matBERebar['fy'] = fybe
                    matBERebar['b'] = 0.005 # assumed
                    matBERebar['R0'] = 20 
                    matBERebar['cR1'] = 0.925
                    matBERebar['cR2'] = 0.15
                    matBERebar['a1'] = 0.0
                    matBERebar['a2'] = 1.0
                    matBERebar['a3'] = 0.0
                    matBERebar['a4'] = 1.0
                    matBERebar['sigini'] = 0.0
                    self.mats.append(matBERebar)
                    matBERebar = {}
                    matBERebar['name'] = str(matTag + 6)
                    matBERebar['type'] = 'MinMaxMaterial'
                    matBERebar['material'] = str(matTag + 5)
                    matBERebar['epsMin'] = -0.008 # assumed
                    matBERebar['epsMax'] = 0.0785 # assumed
                    self.mats.append(matBERebar)

                #{"name": "90", "type": "Steel01", "E": 74936.7, "fy": 50, "b": 1, "a1": 0, "a2": 55, "a3": 0, "a4": 55},
                alphaShear = 0.042
                _Ec = 2*fc/eps
                Gc = alphaShear*_Ec
                if (tbe>t):
                    Av = l*t
                else:
                    Av = 5/6*l*t
                k_shear = Av*Gc
                matSteel = {}
                matSteel['name'] = str(matTag + 7)
                matSteel['type'] = 'Steel01'
                matSteel['E'] = k_shear
                matSteel['fy'] = 50
                matSteel['b'] = 1
                self.mats.append(matSteel)

                

                sect = {}
                sect['name'] = str(secTag + 1)
                sect['type'] = 'FiberSection2d'
                fibers = []

                wFiber = lweb / self.numWebY
                areaFiber = wFiber * t  
                coordX = lweb/2 + wFiber/2
                for nf in range(0,self.numWebY):
                    coordX -= wFiber
                    coordY = 0.0
                    fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                    fibers.append(fiber)
                if lbe > 0.000001:
                    # right BE core
                    wFiber = (lbe-beVertcover*2) / self.numBEY
                    areaFiber = wFiber * (t-beVertcover*2) 
                    coordX = lweb/2 + beVertcover - wFiber/2
                    for nf in range(0,self.numBEY):
                        coordX += wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 2)}
                        fibers.append(fiber)
                    # left BE core
                    wFiber = (lbe-beVertcover*2) / self.numBEY
                    areaFiber = wFiber * (tbe-beVertcover*2) 
                    coordX = -(lweb/2 + beVertcover - wFiber/2)
                    for nf in range(0,self.numBEY):
                        coordX -= wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 2)}
                        fibers.append(fiber)
                    # right BE right cover
                    wFiber = (beVertcover) / self.numBECRY
                    areaFiber = wFiber * tbe 
                    coordX = l/2 - beVertcover - wFiber/2
                    for nf in range(0,self.numBECRY):
                        coordX += wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # left BE left cover
                    wFiber = (beVertcover) / self.numBECRY
                    areaFiber = wFiber * tbe 
                    coordX = -(l/2 - beVertcover - wFiber/2)
                    for nf in range(0,self.numBECRY):
                        coordX -= wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # right BE left cover
                    wFiber = (beVertcover) / self.numBECLY
                    areaFiber = wFiber * tbe 
                    coordX = lweb/2 - wFiber/2
                    for nf in range(0,self.numBECLY):
                        coordX += wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # left BE right cover
                    wFiber = (beVertcover) / self.numBECLY
                    areaFiber = wFiber * tbe 
                    coordX = -(lweb/2 - wFiber/2)
                    for nf in range(0,self.numBECLY):
                        coordX -= wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # right BE top cover
                    wFiber = (lbe - 2*beVertcover) / self.numBECTY
                    areaFiber = wFiber * beVertcover 
                    coordX = lweb/2 + beVertcover - wFiber/2
                    for nf in range(0,self.numBECTY):
                        coordX += wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # left BE top cover
                    wFiber = (lbe - 2*beVertcover) / self.numBECTY
                    areaFiber = wFiber * beVertcover 
                    coordX = -(lweb/2 + beVertcover - wFiber/2)
                    for nf in range(0,self.numBECTY):
                        coordX -= wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # right BE bottom cover
                    wFiber = (lbe - 2*beVertcover) / self.numBECBY
                    areaFiber = wFiber * beVertcover 
                    coordX = lweb/2 + beVertcover - wFiber/2
                    for nf in range(0,self.numBECBY):
                        coordX += wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)
                    # left BE bottom cover
                    wFiber = (lbe - 2*beVertcover) / self.numBECBY
                    areaFiber = wFiber * beVertcover 
                    coordX = -(lweb/2 + beVertcover - wFiber/2)
                    for nf in range(0,self.numBECBY):
                        coordX -= wFiber
                        coordY = 0.0
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 1)}
                        fibers.append(fiber)

                # web rebar vert
                #webVertnumThic 
                areaFiber = webVertbarArea
                dFiber = (webVertbarArea / 3.14159)**0.5*2
                numBars = int(floor((lweb - webVertcover*2 - dFiber) / (webVertspacing+dFiber))+1)
                coordX = (webVertspacing*(numBars-1) + dFiber*numBars)/2 + webVertspacing + dFiber/2
                coordY = 0.0#t/2-webVertcover
                for nf in range(0,numBars):
                    coordX -= (webVertspacing+dFiber)
                    for nfT in range(0,webVertnumThic):
                        fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 4)}
                        fibers.append(fiber)

                if lbe > 0.000001:
                    # BE rebar vert 
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
                    for nf in range(0,numBars):
                        coordX += (beVertspacing+dFiber)
                        for nfT in range(0,beVertnumThic):
                            fiber = {"coord": [coordX, coordY], "area": areaFiber, "material": str(matTag + 6)}
                            fibers.append(fiber)   
                            fiber = {"coord": [-coordX, coordY], "area": areaFiber, "material": str(matTag + 6)}
                            fibers.append(fiber)    


                sect['fibers'] = fibers
                self.sections.append(sect)
                

                sect = {}
                sect['name'] = str(secTag + 2)
                sect['type'] = 'SectionAggregator'
                sect['section'] = str(secTag + 1)
                sect['materials'] = [str(matTag + 7)]
                sect['dof'] = ["Vy"]
                self.sections.append(sect)

                sectionList.append(str(secTag + 2))


                
                secTag += 2
                matTag += 7

            self.sectionList.append(sectionList)
                


            #pprint(section['boundaryElementLength'])
            
            SAM['StructuralAnalysisModel']['properties']={}
            SAM['StructuralAnalysisModel']['properties']['uniaxialMaterials'] = self.mats
            SAM['StructuralAnalysisModel']['properties']['ndMaterials'] = []
            SAM['StructuralAnalysisModel']['properties']['sections'] = self.sections

        # spring mat {"name": "99", "type": "ElasticMaterial", "Epos": 1e+12, "Eneg": 1e+12, "eta": 0}
        springMat = {}
        springMat['name'] = str(matTag + 1)
        springMat['type'] = 'ElasticMaterial'
        springMat['Epos'] = 1e12
        springMat['Eneg'] = 1e12
        springMat['eta'] = 0
        self.mats.append(springMat)
        matTag += 1

        # create crdTrans
        crdTag = 1
        SAM['StructuralAnalysisModel']['properties']['crdTransformations'] = {'name':str(crdTag), "type": 'CorotCrdTransf2d'}

        # create geometry
        #pprint(self.BIM.floors)
        node={}
        node['crd'] = [0, 0]
        node['name'] = nodeTag + 1
        node['ndf'] = 3
        self.nodes.append(node)
        nodeTag += 1

        for fl in self.BIM.floors:
            node={}
            node['crd'] = [0, fl['elevation']]
            node['name'] = nodeTag + 1
            node['ndf'] = 3
            self.nodes.append(node)
            nodeTag += 1
            if (nodeTag>2):
                element = {}
                element['name'] = eleTag+1
                element['nodes'] = [nodeTag-1,nodeTag]
                element['type'] = 'ForceBeamColumn2d'
                element['sections'] = self.sectionList[0]
                element['integration'] = {"type": "Lobatto"}
                element['massperlength'] = 0
                element['crdTransformation'] = str(crdTag)


                self.elements.append(element)
                eleTag += 1

        # spring elements
        for dof in ['Mz','Vy','P']:
            eleSpring = {}
            eleSpring['name'] = eleTag + 1
            eleSpring['type'] = 'ZeroLength'
            eleSpring['nodes'] = [1, 2]
            eleSpring['materials'] = [str(matTag)]
            eleSpring['dof'] = [dof]
            eleSpring['transMatrix'] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            self.elements.append(eleSpring)
            eleTag += 1

        SAM['StructuralAnalysisModel']['geometry'] = {}
        SAM['StructuralAnalysisModel']['geometry']['nodes'] = self.nodes
        SAM['StructuralAnalysisModel']['geometry']['elements'] = self.elements



        self.SAM = SAM

    def writeSAM(self,newSAMFile):
        with open(newSAMFile,'w') as jf:
            json.dump(self.SAM, jf,indent=4)
            print('SAM file created successfully.')




'''
# test
SAMModel = BeamColumnSAM()
SAMModel.readBIM('../Data/ConcreteShearWallBeamcolumn/For AI-M/DazioWSH6/RCWall_DazioWSH6_BIM.json')
SAMModel.setMesh(32, 32, 2, 2, 4, 4, 5)
SAMModel.createSAM()
SAMModel.writeSAM('../Data/ConcreteShearWallBeamcolumn/For AI-M/DazioWSH6/SAM_beamcolumn.json')
exit()
'''

dataDir = '../Data/ConcreteShearWallBeamcolumn/For AI-M/'

'''
testName = 'PilakoutasSW6'
BIMName = os.path.join(dataDir, testName,'RCWall_'+testName+'_BIM.json')
for nInt in [5,7,9]:
    SAMName = os.path.join(dataDir, testName,'RCWall_'+testName+'nInt'+str(nInt)+'_SAM.json')
    print(SAMName)

    SAMModel = BeamColumnSAM()
    SAMModel.readBIM(BIMName)
    SAMModel.setMesh(32, 32, 2, 2, 4, 4, nInt)
    SAMModel.createSAM()
    SAMModel.writeSAM(SAMName)
exit()
'''

'''
for testName in os.listdir(dataDir):
    BIMName = os.path.join(dataDir, testName,'RCWall_'+testName+'_BIM.json')
    print(testName)
    for nInt in [5,7,9]:
            SAMName = os.path.join(dataDir, testName,'RCWall_'+testName+'nInt'+str(nInt)+'_SAM.json')
            SAMModel = BeamColumnSAM()
            SAMModel.readBIM(BIMName)
            SAMModel.setMesh(32, 32, 2, 2, 4, 4, nInt)
            SAMModel.createSAM()
            SAMModel.writeSAM(SAMName)
            del(SAMModel)
exit()
'''

'''
for testName in os.listdir(dataDir):
    BIMName = os.path.join(dataDir, testName,'RCWall_'+testName+'_BIM.json')
    for nInt in [5,7,9]:
        SAMName = os.path.join(dataDir, testName,'RCWall_'+testName+'nInt'+str(nInt)+'_SAM.json')
        try:
            SAMModel = BeamColumnSAM()
            SAMModel.readBIM(BIMName)
            SAMModel.setMesh(32, 32, 2, 2, 4, 4, nInt)
            SAMModel.createSAM()
            SAMModel.writeSAM(SAMName)
            del(SAMModel)
        except:
            print(testName)
'''
