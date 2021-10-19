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

def auswPointCurr(path,NEURONMOD):
    inpsegs  = inps
    frasegs  = fras
    IMUS     = [0.0,0.025,0.05,0.075,0.1,0.125,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8]
    IMix     = ['00','0025', '005', '0075', '01', '0125', '015', '02', '025', '03','035','04', '045', '05','055','06','065','07','075','08']
    cutoff   = 500
    cutoff2  = 10000
    
    for j in xrange(len(inpsegs)):
        rcv     = np.zeros((len(IMUS),6))
        miss    = []
        if j==1:
            cutoff = 0
        for i in range(len(IMUS)):
            fname  = path+"v_pointcurrIO%sinp%iimu%s.dat"%(NEURONMOD,inpsegs[j],IMix[i])
            if os.path.isfile(fname):
                vv    = np.loadtxt(fname)
                vv   *= 1000
                avv   = vv.copy()
                ata,ala,dvv = avv[:,0],avv[:,1],np.diff(avv[:,1])
                imxal = np.where(ala>10.)[0]
                vv    = vv[np.where(vv[:,0]>cutoff)[0],:]
                vv    = vv[np.where(vv[:,0]<cutoff2)[0],:]
                tsa   = vv[np.where(vv[:,1]>10.)[0],0]
                inxa  = tsa[np.where(np.diff(tsa)>1.)[0]+1]
                
                if len(inxa)>=2:
                    da  = np.diff(inxa)                   
                    cv,rr,dd = np.std(da)/np.mean(da), 1000./np.mean(da), da[0]/da[-1]
                    
                    asa  = ata[imxal]
                    inxa = np.where(np.diff(asa)>1.)[0]
                    da   = np.diff(asa[inxa])
                    
                    if len(da)>2:
                        sp0 = np.where(dvv[max(0,imxal[0]-50):imxal[0]]>1.25)[0][0]+max(0,imxal[0]-50)
                        sp1 = np.where(dvv[(imxal[-1]-50):imxal[-1]]>1.25)[0][0]+(imxal[-1]-50)
                        t1,t2 = avv[sp0,1],avv[sp1,1]
                    else:
                        t1,t2 = 0,0
          
                else:
                    cv,rr,dd,t1,t2 = 0,0,0,0,0
                rcv[i,:] = IMUS[i],cv,rr,dd,t1,t2
                print rcv
            else:
                miss.append([i])
                print i
        np.savetxt(path+NEURONMOD+'_pointcurrIO%i_%i_%s.dat'%(cutoff,cutoff2,inpsegs[j]),rcv)



auswPointCurr('./',NEURONMOD)
    
