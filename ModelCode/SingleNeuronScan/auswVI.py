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

def auswVI(path,NEURONMOD):
    imus    = np.arange(-0.5,0.5,0.1)
    inpsegs = inps
    for j in range(len(inpsegs)):
        ll = np.zeros((len(imus),2))    
        for i in range(len(imus)):
            fname = path+"v_"+NEURONMOD+"VI%i%iseg_id%i.dat"%(i,inpsegs[j],inpsegs[j])
            vv    = np.loadtxt(fname)
            vv   *= 1000
            vv    = vv[np.where(vv[:,0]<1500)[0],:]
            tsa   = vv[np.where(vv[:,1]>15.)[0],0]
            inxa  = tsa[np.where(np.diff(tsa)>1.)[0]+1]
            if len(inxa)>=2 and j==0:
                ll[i,:] = np.nan,np.nan
            else:    
                ll[i,:] = imus[i],vv[-1,1+j]
        np.savetxt(path+NEURONMOD+"%iVI.dat"%(inpsegs[j]),ll)


auswVI('./',NEURONMOD)
    
