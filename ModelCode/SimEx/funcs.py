### import needed neuroml and python packages
from neuroml import __version__
from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import Population
from neuroml import Location
from neuroml import Instance
from neuroml import Projection
from neuroml import Property
from neuroml import PulseGenerator
from neuroml import Connection
from neuroml import ConnectionWD
from neuroml import IncludeType
from neuroml import InputList
from neuroml import Input
from neuroml import PoissonFiringSynapse
from neuroml import ExpTwoSynapse
from neuroml import ElectricalConnectionInstance
from neuroml import ElectricalProjection
from neuroml import GapJunction
from neuroml import VoltageClamp
import neuroml.writers as writers
from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation
from random import random
from random import uniform
from random import gauss
from random import seed
from random import shuffle
import numpy as np
import os



### gap junction functions

def add_gap_junction_synapse(nml_doc, id, conductance):
    
    """
    Adds a <gapJunction> element to the document. See the definition of the 
    behaviour of this here: https://www.neuroml.org/NeuroML2CoreTypes/Synapses.html#gapJunction
    
    Returns the class created.
    """
    
    syn0 = GapJunction(id=id, conductance=conductance)

    nml_doc.gap_junctions.append(syn0)

    return syn0


def add_elect_connection(projection, id, presynaptic_population, pre_component, pre_cell_id, pre_seg_id, postsynaptic_population, post_component, post_cell_id, post_seg_id, gap_junction_id, pre_fraction=0.5, post_fraction=0.5):

    """
    Add a single electrical connection (via a gap junction) to a projection between `presynaptic_population` and `postsynaptic_population`
    """

    connection = ElectricalConnectionInstance(id=id, \
                                              pre_cell="../%s/%i/%s" % (presynaptic_population, pre_cell_id, pre_component), \
                                              post_cell="../%s/%i/%s" % (postsynaptic_population, post_cell_id, post_component), \
                                              synapse=gap_junction_id, \
                                              pre_segment=pre_seg_id, \
                                              post_segment=post_seg_id, \
                                              pre_fraction_along=pre_fraction, \
                                              post_fraction_along=post_fraction)

    projection.electrical_connection_instances.append(connection)



def add_probabilistic_dendrite_ring_gapjunx(net, presynaptic_population, pre_component, postsynaptic_population, post_component, prefix, gap_junction_id, sourceseglis, targetseglis, numContacts, numCells, numNeighbors_GJ):

    '''
    Creates electrical synapses (gap junctions) in a ring topology among soma and dendrites of 'numNeighbors_GJ' nearest neighbors with probability 0.5, for numCells cells in total. 

    '''
    
    if numCells==0:
        return None
        
    proj = ElectricalProjection(id="%s_%s_%s"%(prefix,presynaptic_population, postsynaptic_population), presynaptic_population=presynaptic_population, postsynaptic_population=postsynaptic_population)

    count = 0

    for i in range(0, numCells):
        for j in range(-numNeighbors_GJ,numNeighbors_GJ+1):
            nn=(i+j)%numCells  # mind the periodic boundary conditions
            if (not i==nn) and (random()<0.5):
                slis = sourceseglis
                shuffle(slis) # permute order of source segment list
                slis = slis[:numContacts] # take first numContacts entries of permuted list
                tlis = targetseglis
                shuffle(tlis) # permute order of target segment list
                tlis = tlis[:numContacts] # take first numContacts entries of permuted list
                for k in range(numContacts):
                    add_elect_connection(proj, count, presynaptic_population, pre_component,i, slis[k], postsynaptic_population, post_component, nn, tlis[k], gap_junction_id, pre_fraction=random(), post_fraction=random())  # add synapses on randomly drawn source and target segments at random segment position 
                    count+=1
    net.electrical_projections.append(proj)                
    return proj

### chemical synapse functions

def add_connectionWD(projection, id, pre_pop, pre_component, pre_cell_id, pre_seg_id, post_pop, post_component, post_cell_id, post_seg_id, weight, delay):

    connection = ConnectionWD(id=id, \
                            pre_cell_id="../%s/%i/%s"%(pre_pop, pre_cell_id, pre_component), \
                            pre_segment_id=pre_seg_id, \
                            pre_fraction_along=0.5,
                            post_cell_id="../%s/%i/%s"%(post_pop, post_cell_id, post_component), \
                            post_segment_id=post_seg_id,
                            post_fraction_along=0.5, delay=delay, weight=weight)

    projection.connection_wds.append(connection)


def add_connectionWDrand(projection, id, pre_pop, pre_component, pre_cell_id, pre_seg_id, post_pop, post_component, post_cell_id, post_seg_id, weight, delay):

    connection = ConnectionWD(id=id, \
                            pre_cell_id="../%s/%i/%s"%(pre_pop, pre_cell_id, pre_component), \
                            pre_segment_id=pre_seg_id, \
                            pre_fraction_along=random(),
                            post_cell_id="../%s/%i/%s"%(post_pop, post_cell_id, post_component), \
                            post_segment_id=post_seg_id,
                            post_fraction_along=random(), delay=delay, weight=weight)

    projection.connection_wds.append(connection)    


def add_probabilistic_ring_projection_delay(net, presynaptic_population, pre_component, postsynaptic_population, post_component, prefix, synapse, numCells, numNeighbors, weight):
    '''
    Creates chemical synapses in a ring topology among somata of 'numNeighbors'
    nearest neighbors with Gaussian connectivity profile, for numCells cells 
    in total. 
    Delays are created by sum of synaptic delay d0 (0.5 ms) plus distance-
    dependent part d=|i-j|*0.2 ms, i,j neuron index.
    '''
    
    # Gauss profile used in Vida et al (2006): f(d) = 9.9736*exp(d**2/-1152), i.e. footprint of sigma=24
    # then compared to uniform random number in [0,10]; here we use probability profile f(d) in [0,1]
    def connprob(x,sig):
        return np.exp(-x**2/2./sig**2)

    cpb = 24.*numCells
    d0 = 0.5 # constant synaptic delay in ms
    
    if numCells==0:
        return None
        
    proj = Projection(id="%s_%s_%s"%(prefix,presynaptic_population, postsynaptic_population), presynaptic_population=presynaptic_population, postsynaptic_population=postsynaptic_population, synapse=synapse)

    count = 0
    dlist = []
    for i in range(0, numCells):
        for j in range(-numNeighbors,numNeighbors+1):
            nn=(i+j)%numCells      # mind the periodic boundary conditions
            if (random()<connprob(abs(j),cpb)) and (not i==nn): # establish connections with probability-dependent probability (Bernoulli trial), no autapses
                dring = abs(j)*0.2 # distance-dependent conduction delay in ms; assuming pairwise distance=50um between 200 neurons on the ring and conduction velocity of 0.25 m/s
                add_connectionWD(proj, count, presynaptic_population, pre_component, i, 0, postsynaptic_population, post_component, nn, 0, weight, str(d0+dring)+" ms")  # add synapses between somata of source and target cell
                count+=1
                    
    net.projections.append(proj)

    return proj
    

def add_probabilistic_dendrite_ring_projection(net, presynaptic_population, pre_component, postsynaptic_population, post_component, prefix, synapse, numCells, numNeighbors, sourceseglis, targetseglis, numContacts, weight):
    '''
    Creates chemical synapses in a ring topology among somata and dendrites
    of 'numNeighbors' nearest neighbors with Gaussian connectivity profile, 
    for numCells cells in total. 
    Delays are created by sum of synaptic delay d0 (0.5 ms) plus distance-
    dependent part d=|i-j|*0.2 ms, i,j neuron index.
    '''
    
    def connprob(x,sig):
        return np.exp(-x**2/2./sig**2)

    cpb = 24*numCells
    d0 = 0.5 # constant synaptic delay in ms
    
    if numCells==0:
        return None
        
    proj = Projection(id="%s_%s_%s"%(prefix,presynaptic_population, postsynaptic_population), presynaptic_population=presynaptic_population, postsynaptic_population=postsynaptic_population, synapse=synapse)

    count = 0
    for i in range(0, numCells):
        for j in range(-numNeighbors,numNeighbors+1):
            nn=(i+j)%numCells # mind the periodic boundary conditions
            if (random()<connprob(abs(j),cpb)) and (not i==nn): # establish connections with probability-dependent probability (Bernoulli trial), no autapses 
                numc = int(numContacts*connprob(abs(j),cpb)) # draw realized number of contacts between the two cells with same conn-profile
                dring = abs(j)*0.2 # distance-dependent conduction delay in ms; assuming pairwise distance=50um between 200 neurons on the ring and conduction velocity of 0.25 m/s
                slis = sourceseglis
                shuffle(slis) # permute order of source segments list
                slis = slis[:numc] # take first numContacts entries of permuted list
                tlis = targetseglis 
                shuffle(tlis) # permute order of target segments list
                tlis = tlis[:numc] # take first numContacts entries of permuted list
                for inx in range(numc):
                    add_connectionWDrand(proj, count, presynaptic_population, pre_component, i, slis[inx], postsynaptic_population, post_component, nn, tlis[inx], weight, str(d0+dring)+" ms") # add synapses on randomly drawn source and target segments at random segment position 
                    count+=1
    net.projections.append(proj)
    return proj

### place neurons in space (for ring nets irrelevant, conn based on neuron ID
def add_population_in_rectangular_region(net, pop_id, cell_id, size, x_min, y_min, z_min, x_size, y_size, z_size, color=None):
    
        pop = Population(id=pop_id, component=cell_id, type="populationList", size=size)
        if color is not None:
            pop.properties.append(Property("color",color))
        net.populations.append(pop)

        for i in range(0, size) :
                index = i
                inst = Instance(id=index)
                pop.instances.append(inst)
                inst.location = Location(x=str(x_min +(x_size)*random()), y=str(y_min +(y_size)*random()), z=str(z_min+(z_size)*random()))



### simulation of net:
def generate_BC_cell_layer(network_id,
                           fname,                # output filename
                           x_size,               # x-dim (um), irrelevant for ring net
                           y_size,               # y-dim (um)
                           z_size,               # z-dim (um)
                           bc_group_component,   # neuron model
                           bc_syn_weight,        # peak GABA conductance (nS)
                           bc_syn_erev,          # GABA syn reversal potenials (mV)
                           bc_syn_tau_rise,      # GABA syn rise time (ms)
                           bc_syn_tau_decay,     # GABA syn decay time (ms)   
                           bc_gj_weight,         # gap junction coupling strength (nS)
                           ampa_syn_weight,      # peak AMPA conductance (nS)
                           pfs_freq,             # mean rate per poisson-firing synapse (1/s)
                           pfs_disp,             # dispersion of rate/syn around mean (1/s)        
                           numCells_bc = 20,     # number of cells 
                           numNeighbors_bc = 5,  # max  number of neighbors per side
                           numContactsPFS = 20,  # number of input AMPA syns
                           numContacts = 5,      # max number of syns between any two neurons
                           rec = False,          # for apical stim, can record from 10 sites
                           API = False,          # apical drive?
                           SOMA = False,         # somatic drive?
                           connections = True,   # network connections?
                           activate = False,     # activate network after a transient?
                           gapjunx = True,       # gap junctions?
                           validate = True,      # validate LEMS
                           random_seed = 12345,  # simulation seed
                           generate_lems_simulation = False, # gen LEMS sim
                           duration = 500,       # sim duration (ms)
                           dt = 0.01):           # sim time step (ms)
    
    seed(random_seed)

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id)
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))

    # The names of the groups/populations 
    bc_group = "BasketCells"

    # Generate basket cells 
    if numCells_bc>0:
        add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")

    # Connect cells in randomized ring structure
    if connections:
        if not activate:
            bc_syn = ExpTwoSynapse(id="bc_syn", gbase=str(1)+"nS", erev=str(bc_syn_erev)+"mV", tau_rise=str(bc_syn_tau_rise)+"ms", tau_decay=str(bc_syn_tau_decay)+"ms")
            nml_doc.exp_two_synapses.append(bc_syn)

            add_probabilistic_dendrite_ring_projection(net, bc_group, bc_group_component, bc_group, bc_group_component, 'NetConn', "bc_syn", numCells_bc, numNeighbors_bc, bclis, bclis, numContacts,bc_syn_weight)
        
        if activate: # NOTE: start time can be set in expTwoSynapseAct.nml
                     # if you want current-based synapses, use expTwoSynapseCurr.nml
            nml_doc.includes.append(IncludeType('./synapseNML/expTwoSynapseAct.nml'))
            add_probabilistic_dendrite_ring_projection(net, bc_group, bc_group_component, bc_group, bc_group_component, 'NetConn', "expTwoSynapseAct", numCells_bc, numNeighbors_bc, bclis, bclis, numContacts, bc_syn_weight)
             
    if gapjunx:
        gj_syn = add_gap_junction_synapse(nml_doc, id="gj_syn", conductance=str(bc_gj_weight)+"nS")
        add_probabilistic_dendrite_ring_gapjunx(net, bc_group, bc_group_component, bc_group, bc_group_component, 'GapJunx',"gj_syn", apilis, apilis, 8,  numCells_bc, 4)
      
    # Randomize initial potentials via voltage clamp
    vc_dur = 2  # ms
    for i in range(0, numCells_bc):
        tmp = -72.5 + random()*15
        vc = VoltageClamp(id='VClamp%i'%i, delay='0ms', duration='%ims'%vc_dur, simple_series_resistance='1e6ohm', target_voltage='%imV'%tmp)
        
        nml_doc.voltage_clamps.append(vc)
        
        input_list = InputList(id='input_%i'%i, component='VClamp%i'%i, populations=bc_group)
        input = Input(id=i, target='../%s/%i/%s'%(bc_group, i, bc_group_component), destination='synapses')
        input_list.input.append(input)
        
        net.input_lists.append(input_list)
    
      
    ### poisson-firing synapses

    ampa_syn = ExpTwoSynapse(id="ampa_syn", gbase=str(ampa_syn_weight)+"nS", erev="0mV", tau_rise="0.2 ms", tau_decay="2.0 ms")
    
    nml_doc.exp_two_synapses.append(ampa_syn)
        
    cntpfs=0

    PFV=[gauss(pfs_freq, pfs_disp) for _ in range(0,numCells_bc)]
       
    for i in range(numCells_bc):
        pfs= PoissonFiringSynapse(id="poissonFiringSyn%i"%i,
                                  average_rate=str(PFV[i])+"Hz",
                                  synapse="ampa_syn", 
                                  spike_target="./ampa_syn")
            
        nml_doc.poisson_firing_synapses.append(pfs)
        input_list = InputList(id="%s_input"%pfs.id,
                               component=pfs.id,
                               populations=bc_group) 
            
        if API:
            rrinx = range(len(apilis))
            shuffle(rrinx)
            rrinx = rrinx[:numContactsPFS]
            ### if recording from ten locations
            if i==0 and rec==True:
                recl=[apilis[rrinx[_]] for _ in range(10)]
                
            for isyn in range(numContactsPFS):
                expInp = Input(id=cntpfs,
                               target="../%s/%i/%s" %(bc_group,i,bc_group_component),
                               destination="synapses",
                               segment_id=apilis[rrinx[isyn]],
                               fraction_along=fraclis[rrinx[isyn]])
                input_list.input.append(expInp)
                cntpfs+=1
                
        if SOMA:
            for isyn in range(numContactsPFS):
                expInp = Input(id=cntpfs,
                               target="../%s/%i/%s" %(bc_group,i,bc_group_component),
                               destination="synapses",
                               segment_id=0,
                               fraction_along=0.5)
                input_list.input.append(expInp)
                cntpfs+=1
                
        net.input_lists.append(input_list)     

            
    #######   Write to file  ######    

    print("Saving to file...")
    nml_file = network_id+'.net.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file)

    print("Written network file to: "+nml_file)


    if validate:

        ###### Validate the NeuroML ######    

        from neuroml.utils import validate_neuroml2
        validate_neuroml2(nml_file) 
        
    if generate_lems_simulation:
        # Create a LEMSSimulation to manage creation of LEMS file

        # IN NEWER VERSIONS: lems_seed -> simulation_seed
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt, lems_seed=np.random.randint(0,10000))
        # Point to network as target of simulation
        ls.assign_simulation_target(net.id)
        
        # Include generated/existing NeuroML2 files
        ls.include_neuroml2_file('../NeuronModels/'+'%s.cell.nml'%bc_group_component)
        ls.include_neuroml2_file(nml_file)

        # Specify Displays and Output Files
        if numCells_bc>0:
          
            disp_bc = "display_bc"
            ls.create_display(disp_bc, "Voltages Basket Cells", "-80", "40")

            of_bc = 'Volts_file_bc'
            ls.create_output_file(of_bc, fname)

                
            for i in range(numCells_bc):
                if rec and pfsinp:
                    cntvi=0
                    intsegs=[0]+recl
                    for seg_id in intsegs:
                        quantity = '%s/%i/%s/%s/v'%(bc_group, i, bc_group_component,seg_id)
                        ls.add_line_to_display(disp_bc, "MF %i: Vm"%cntvi, quantity, "1mV", pynml.get_next_hex_color())
                        ls.add_column_to_output_file(of_bc, "v_%i"%cntvi, quantity)
                        cntvi+=1
                else:
                    quantity = '%s/%i/%s/v'%(bc_group, i, bc_group_component)
                    ls.add_line_to_display(disp_bc, "MF %i: Vm"%i, quantity, "1mV", pynml.get_next_hex_color())
                    ls.add_column_to_output_file(of_bc, "v_%i"%i, quantity)

        # Save to LEMS XML file
        lems_file_name = ls.save_to_file()
    else:
        
        ls = None
        
    print "-----------------------------------"
    
    return nml_doc, ls
