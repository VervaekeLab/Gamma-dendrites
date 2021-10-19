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

def auswEPSP(path,NEURONMOD):
    inpsegs = INPSEGS
    ll      = np.zeros((len(inpsegs),5))    
    for i in range(len(inpsegs)):
        fname   = path+'v_'+NEURONMOD+"EPSP%i"%(i)+'seg_id%i.dat'%(inpsegs[i])
        vv      = np.loadtxt(fname)
        vv     *= 1000
        vv      = vv[3500:,:]
        ll[i,:] = DISTS[i],max(vv[:,1]),vv[499,1],max(vv[:,2]),vv[499,2]
    np.savetxt(path+NEURONMOD+"EPSP.dat",ll)

auswEPSP('./',NEURONMOD)
    
