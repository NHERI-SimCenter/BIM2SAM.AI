from collections import namedtuple
import json
from pprint import pprint
from math import floor
import os




class BIM:
    """A calss of Beam-Column BIM model for concrete shear wall"""

    '''
    BIMFileName = ''
    stories = 0
    height = 0

    StructuralInformation = {}
    walls = []
    materials = []
    wallsections = []
    floors = []
    clines = []
    '''

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

        self.materials = BIM['StructuralInformation']['properties']['materials']
        self.wallsections = BIM['StructuralInformation']['properties']['wallsections']

        self.walls = BIM['StructuralInformation']['geometry']['walls']

        self.StructuralInformation = {}
  
        #pprint(self.walls[0])


