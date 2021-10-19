'''
Code to generate networks of fully reconstructed PV+-basket cells. Reconstructed cell models were adpated from

"Distinct nonuniform cable properties optimize rapid and efficient activation of fast-spiking GABAergic interneurons"
Anja Norenberg, Hua Hu, Imre Vida, Marlene Bartos, and Peter Jonas 
PNAS 107(2):894-899 (2010) DOI 10.1073/pnas.0910716107
 
and ModelDB

https://senselab.med.yale.edu/ModelDB/ShowModel?model=140789#tabs-1.

Dynamical basket cell model was extended from 

"Dendritic mechanisms underlying rapid synaptic activation of fast-spiking hippocampal interneurons"
Hua Hu, Marco Martina, and Peter Jonas 
Science 327(5961):52-58 (2010) DOI 10.1126/science.1177876

Networks are ring networks with a Gaussian connection profile (GABA-synapses) as in

"Fast synaptic inhibition promotes synchronized gamma oscillations in hippocampal interneuron networks"
Marlene Bartos, Imre Vida, Michael Frotscher, Axel Meyer, Hannah Monyer, Joerg R.P. Geiger, and Peter Jonas
PNAS 99(20):13222-13227 (2002) DOI 10.1073/pnas.192233099

"Shunting inhibition improves robustness of gamma oscillations in hippocampal interneuron networks by homogenizing firing rates"
Imre Vida, Marlene Bartos, and Peter Jonas
Neuron 49, 107-117 (2006) DOI 10.1015/j.neuron.2005.11.036

See also ModelDB:
https://senselab.med.yale.edu/modeldb/showModel.cshtml?model=21329

The main difference is that in our simulations interneuron synapses can be placed not only on the soma, but on a perisomatic range of <= 50 um, including parts of the basal and apical dendrites. First, a distance-dependent Gaussian connection profile decides if any two neurons within a neighborhood of maximally +/- N/4 are connected, and if so, the number of etablished synapses scales with the same Gaussian footprint and a maximal number numContacts (in our simulations six, if autapses are included, otherwise five).

External drive is present as poisson-firing synaptic conductances (AMPA-synapses).
Targets are either soma (SOMA=True) or distal apical dendrites (SOMA=False).

Varied are the rate per AMPA-synapse (pfsfreq), the peak amplitude of the GABA-synapses and the degree of input heterogeneity (pfsdisp). In particular, pfsfreq is drawn from a Gaussian with mean pfsfreq and variance pfsfreq*pfsdisp.

Python code adapted and modified from existing code in 
https://github.com/OpenSourceBrain/OpenCortex

To run from commandline:

python makeNetwork.py
chmod u+x mysim.sh;./mysim.sh


SOFTWARE VERSIONS : python/2.7.15; numpy/1.11.0; scipy/0.17.0; 
                    neuroml/0.2.18; jNeuroML/0.10.1; pyNeuroML/0.1.15; neuron/7.4

No guarantees for the code to work with newer versions of NeuroML2, PyNeuroML, jnml, Neuron, python.

Author: Birgit Kriener, April 2017
'''

execfile('funcs.py')
execfile('SegmentList.py')

if __name__ == "__main__":

    ### choose cell model to run nmind=index of cell model (1,2,3,4,5,6); main model=2
    nmind            = 2
    NEURONMOD        = 'jonasnmBC%iKlt'%nmind
    apilis,fraclis,bclis = segml(nmind)      # potential apical targets (ID,loc) and targets for BC coupling
    RATES            = [50]                  # poisson rate/AMPA synapse (1/s), external drive
    DISP             = [0.0]                 # dispersion = std(rate/syn)/mean(rate/syn) (%)
    LAPTOP           = True                  # if True, use older NeuroML2 version on local machine only, else cluster run with newer version
    SOMA             = 0                     # if 1, AMPA syns placed on soma
    API              = 1-SOMA                # if 1, AMPA syns placed on distal apical dend 
    GJ               = 0                     # if 1, gap junctions present
    numCells_bc      = 200                   # number of neurons in network
    numNeighbors_bc  = int(numCells_bc/4.)   # max size of neighborhood = 2xnumNeighbors_bc
    bc_syn_weight    = 2.                    # peak GABA amplitude (nS)
    bc_syn_erev      = -75.                  # GABA synapse reversal potential (mV)
    bc_syn_tau_rise  = 0.16                  # GABA synapse conductance rise time (ms)
    bc_syn_tau_decay = 1.8                   # GABA synapse conductance decay time (ms) 
    bc_gj_weight     = 0.1*GJ                # gap junction coupling strength (nS)
    ampa_syn_weight  = 2.                    # peak AMPA amplitude (mV)
    numContacts      = 6                     # maximal number of synaptic contacts between any two BC
                                             # (note: w/o autapses maximally established number is 5)   
    dt               = 0.025                 # sim time step (ms)
    duration         = 500                   # sim duration (ms)
    
    for ict in range(len(DISP)):    
        
        for ift in range(len(RATES)):
            pfs_freq = RATES[ift]
            pfs_disp = DISP[ict]*pfs_freq       
            RUNNAME = "myrunfrq%iict%i"%(ift,ict)
            if API:
                numContactsPFS =100
                fname = "N%i"%(numCells_bc) + "w%s"%(bc_syn_weight) + "gjw%s"%(bc_gj_weight) +"rev%s"%(bc_syn_erev) + "ts%s"%(bc_syn_tau_decay)+  "pfsfreq%s"%(pfs_freq)+ "pfsdisp%s"%(DISP[ict]) + "ampaw%s"%(ampa_syn_weight) + "numContacts%i"%(numContacts)+"numContactsPFS%i"%(numContactsPFS) + NEURONMOD +"PFSAPI.dat"
            if SOMA:
                numContactsPFS =50
                fname = "N%i"%(numCells_bc) + "w%s"%(bc_syn_weight) + "gjw%s"%(bc_gj_weight) +"rev%s"%(bc_syn_erev) + "ts%s"%(bc_syn_tau_decay)+  "pfsfreq%s"%(pfs_freq) + "pfsdisp%s"%(DISP[ict]) + "ampaw%s"%(ampa_syn_weight) + "numContacts%i"%(numContacts)+"numContactsPFS%i"%(numContactsPFS) + NEURONMOD +"PFSSOMA.dat"

            outputfile=open('mysim%i.sh'%ict, 'a+')
            outputfile.write("env JNML_MAX_MEMORY_LOCAL=2000M jnml LEMS_Sim_%s.xml -neuron -nogui -run\n"%RUNNAME)
            outputfile.close()

            generate_BC_cell_layer(RUNNAME,
                                   fname  = fname,
                                   x_size = 500, 
                                   y_size = 500,
                                   z_size = 500,
                                   bc_group_component = NEURONMOD,
                                   numCells_bc        = numCells_bc,
                                   numNeighbors_bc    = numNeighbors_bc,
                                   numContactsPFS     = numContactsPFS,
                                   numContacts        = numContacts,
                                   bc_syn_weight      = bc_syn_weight,
                                   bc_syn_erev        = bc_syn_erev,
                                   bc_syn_tau_rise    = bc_syn_tau_rise,
                                   bc_syn_tau_decay   = bc_syn_tau_decay,
                                   bc_gj_weight       = bc_gj_weight,
                                   ampa_syn_weight    = ampa_syn_weight,
                                   pfs_freq           = pfs_freq,
                                   rec                = False,
                                   pfs_disp           = pfs_disp,
                                   SOMA               = SOMA,
                                   API                = API,
                                   connections        = True,
                                   activate           = True,
                                   gapjunx            = GJ,
                                   generate_lems_simulation = True,
                                   validate           = True,
                                   random_seed=np.random.randint(0,1000000),
                                   duration           = duration,
                                   dt                 = dt)



