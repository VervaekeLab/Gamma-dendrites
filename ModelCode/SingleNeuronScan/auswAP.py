import neuroml.loaders as loaders
from neuroml import __version__
from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import Population
from neuroml import Location
from neuroml import Instance
from neuroml import GapJunction
from neuroml import Projection
from neuroml import Property
from neuroml import PulseGenerator
from neuroml import Connection
from neuroml import ConnectionWD
from neuroml import IncludeType
from neuroml import InputList
from neuroml import Input
from neuroml import PoissonFiringSynapse
from neuroml import SpikeGenerator
from neuroml import ExpTwoSynapse
from neuroml import ElectricalConnectionInstance
from neuroml import ElectricalProjection
from neuroml import VoltageClamp
import neuroml.writers as writers
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
from random import random
from random import randint
from random import uniform
from random import gauss
from random import seed
import numpy as np
from pylab import find
import os
import sys
import singleNeuron_fcs as sf
import setNeuron_params as sp

NEURONMOD                       = sys.argv[1]
INPSEGS,FRASEGS,DISTS,inps,fras = sp.setNeuPar(NEURONMOD)

def auswAP(path,NEURONMOD):
    inpsegs  = INPSEGS
    ll       = np.zeros((len(inpsegs),2))    
    fname    = path+'v_'+NEURONMOD+"APseg_id0.dat"
    vv       = np.loadtxt(fname)
    vv      *= 1000
    for i in range(len(inpsegs)):
        vvmn = min(vv[:1000,i+1])
        vvmx = max(vv[:,i+1])
        ll[i,:] = DISTS[i],vvmx-vvmn
    np.savetxt(path+NEURONMOD+"AP.dat",ll)

auswAP('./',NEURONMOD)
    
