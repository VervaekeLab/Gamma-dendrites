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

def auswPointCond(path,NEURONMOD):
    inpsegs  = inps
    frasegs  = fras    
    cnds     = np.arange(1.,16.,1)
    cdix     = [int(_) for _ in cnds]
    cutoff   = 500
    cutoff2  = 10000
    
    for j in xrange(len(inpsegs)):
        rcv     = np.zeros((len(cdix),4))
        miss    = []
        for i in xrange(len(cnds)):
            fname    = path+"v_pointcondIO%sinp%icnd%s.dat"%(NEURONMOD,inpsegs[j],cdix[i])        
            if os.path.isfile(fname):
                vv   = np.loadtxt(fname)
                vv  *= 1000
                vv   = vv[np.where(vv[:,0]>cutoff)[0],:]
                vv   = vv[np.where(vv[:,0]<cutoff2)[0],:]
                tsa  = vv[np.where(vv[:,1]>-10.)[0],0]
                inxa = tsa[np.where(np.diff(tsa)>1.)[0]+1]
                if len(inxa)>=2:
                    da = np.diff(inxa)
                    rcv[i,:] = cnds[i], np.std(da)/np.mean(da), 1000./np.mean(da), da[0]/da[-1]
            else:
                miss.append([i])
                print i
        np.savetxt(path+NEURONMOD+'_pointcondIO%i_%i_%s.dat'%(cutoff,cutoff2,inpsegs[j]),rcv)
       
auswPointCond('./',NEURONMOD)
    
