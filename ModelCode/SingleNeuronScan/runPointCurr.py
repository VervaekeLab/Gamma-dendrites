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
NRNPATH                         = sys.argv[2]
INPSEGS,FRASEGS,DISTS,inps,fras = sp.setNeuPar(NEURONMOD)

def runPointCurr(NEURONMOD):
    inpsegs  = inps
    frasegs  = fras
    IMUS     = [0.0,0.025,0.05,0.075,0.1,0.125,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8]
    IMix     = ['00','0025','005','0075','01','0125','015','02','025','03','035','04','045','05','055','06','065','07','075','08']
    for j in xrange(len(inpsegs)):
        for i in xrange(len(IMUS)):
            fname="pointcurrIO%sinp%iimu%s"%(NEURONMOD,inpsegs[j],IMix[i])
            outputfile=open('codrunPointCurr.sh', 'a+')
            outputfile.write("env JNML_MAX_MEMORY_LOCAL=4000M jnml LEMS_Sim_%s.xml -neuron\n"%fname)
            outputfile.write(NRNPATH+"nrnivmodl\n")
            outputfile.write(NRNPATH+"nrniv -nogui -NFRAME 3000 LEMS_Sim_%s_nrn.py\n"%fname)
            outputfile.close()                
            sf.pointCurr(fname,
                      temperature=6.3,
                      x_size = 1,
                      y_size = 1, 
                      z_size = 1,
                      bc_group_component = NEURONMOD,
                      numCells_bc = 1,
                      inpseg = inpsegs[j],
                      fracalong = frasegs[j],
                      numContacts = 1,
                      currinp=True,
                      imu=IMUS[i],
                      rec=True,
                      random_seed = randint(0,100000),
                      generate_lems_simulation = True,
                      validate = True,
                      duration = 2000,
                      dt = sf.DT)
                   
runPointCurr(NEURONMOD)
