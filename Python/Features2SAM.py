from BIM2SAM import BIM2SAM
from BIM import BIM
import numpy as np
import pandas as pd

# ------------------------------
# Continuum model demo
# ------------------------------


N = 10
beta = 0.5
An = 0.5
Ap = 0.5
Bn = 0.5
pars = [N, beta, An, Ap, Bn]
BIMFileName = "../Data/features2SAM/BIM.json"
SAMFileName = "../Data/features2SAM/SAM_Continuum.json"
BIM2SAM(BIMFileName, SAMFileName, 'continuum', pars)



# ------------------------------
# Beam-Column model demo
# ------------------------------

BIMFileName = "../Data/features2SAM/BIM.json"
SAMFileName = "../Data/features2SAM/SAM_BeamColumn.json"
nInt = 5
pars = [nInt]
BIM2SAM(BIMFileName, SAMFileName, 'beamcolumn', pars)
