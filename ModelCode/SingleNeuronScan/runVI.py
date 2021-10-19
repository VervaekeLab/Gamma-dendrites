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


def runVI(NEURONMOD):
    imus     = np.arange(-0.5,0.6,0.1)
    inpsegs  = inps
    frasegs  = fras
    for j in range(len(inpsegs)):
        for i in range(len(imus)):
            fname=NEURONMOD+"VI%i%i"%(i,inpsegs[j])
            outputfile=open('codrunVI.sh', 'a+')
            outputfile.write("env JNML_MAX_MEMORY_LOCAL=4000M jnml LEMS_Sim_%s.xml -neuron\n"%fname)
            outputfile.write(NRNPATH+"nrnivmodl\n")
            outputfile.write(NRNPATH+"nrniv -nogui -NFRAME 3000 LEMS_Sim_%s_nrn.py\n"%fname)
            outputfile.close()
            
            sf.VI(fname,
               temperature=6.3,
               x_size = 1,
               y_size = 1, 
               z_size = 1,
               bc_group_component = NEURONMOD,
               numCells_bc = 1,
               Imu = imus[i],
               inpseg = inpsegs[j],
               fracalong = frasegs[j],
               currinp=True,
               rec=True,
               generate_lems_simulation = True,
               validate = True,
               duration = 2500,
               dt = sf.DT)

runVI(NEURONMOD)
