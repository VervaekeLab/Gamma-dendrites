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

DT       = 0.025

def add_connectionWD(projection, id, pre_pop, pre_component, pre_cell_id, pre_seg_id, post_pop, post_component, post_cell_id, post_seg_id, fracalong, weight, delay):

    connection = ConnectionWD(id=id, \
                            pre_cell_id="../%s/%i/%s"%(pre_pop, pre_cell_id, pre_component), \
                            pre_segment_id=pre_seg_id, \
                            pre_fraction_along=0.5,
                            post_cell_id="../%s/%i/%s"%(post_pop, post_cell_id, post_component), \
                            post_segment_id=post_seg_id,
                            post_fraction_along=fracalong, delay=delay, weight=weight)

    projection.connection_wds.append(connection)
    


def add_population_in_rectangular_region(net, pop_id, cell_id, size, x_min, y_min, z_min, x_size, y_size, z_size, color=None):
    
        pop = Population(id=pop_id, component=cell_id, type="populationList", size=size)
        if color is not None:
            pop.properties.append(Property("color",color))
        net.populations.append(pop)

        for i in range(0, size) :
                index = i
                inst = Instance(id=index)
                pop.instances.append(inst)
                inst.location = Location(x=str(x_min +(x_size)*0), y=str(y_min +(y_size)*0), z=str(z_min+(z_size)*0))

                

def EPSPatten(network_id,
              temperature,
              x_size, 
              y_size, 
              z_size, 
              bc_group_component,
              inpseg,
              fracalong,
              ampa_syn_weight,
              currinp,
              delay=0.5,
              numCells_bc = 1,
              validate = True,
              rec = False,
              random_seed = 123458,
              generate_lems_simulation = False,
              duration = 1000,  # ms
              dt = 0.01):
    
    seed(randint(0,100000))

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id,type='networkWithTemperature', temperature=str(temperature)+'degC')
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))

    # The names of the groups/populations 
    bc_group = "BasketCells"
    ampasyn = ExpTwoSynapse(id="ampasyn", gbase=str(ampa_syn_weight)+"nS", erev="0mV", tau_rise="0.2 ms", tau_decay="1 ms")   
    nml_doc.exp_two_synapses.append(ampasyn)
    
    add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")

    spg=SpikeGenerator(id="spikeGenRegular", period=str(delay)+"ms")
    nml_doc.spike_generators.append(spg)
    add_population_in_rectangular_region(net,"SPGen", "spikeGenRegular", 1, 0, 0, 0, x_size, y_size, z_size, color="1 0 1")
    projspg = Projection(id="%s_%s_%s"%("SPG","SPGen", bc_group), presynaptic_population="SPGen", postsynaptic_population=bc_group, synapse="ampasyn")

    add_connectionWD(projspg, 0, "SPGen", "spikeGenRegular", 0, 0, bc_group, bc_group_component, 0, inpseg, fracalong,1, delay="0 ms")
    net.projections.append(projspg)

    if currinp:
        stim = PulseGenerator(id="stim",
                              delay='0 ms',
                              duration=str(duration)+' ms',
                              amplitude=str(Imu)+'nA')
        
        nml_doc.pulse_generators.append(stim)
        
        input_list = InputList(id="%s_input"%stim.id,
                               component=stim.id,
                               populations=bc_group)
        
        syn_input = Input(id=cnt,target="../%s/%i/%s" % (bc_group, 0, bc_group_component),destination="synapses",segment_id=str(inpseg), fraction_along=str(fracalong))
            
        input_list.input.append(syn_input)
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
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt, lems_seed=randint(0,10000))

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
            ls.create_output_file(of_bc, "v_"+network_id+"seg_id%i"%(inpseg)+".dat")
            #ls.create_output_file(of_bc, "v_"+network_id+"seg_id%i"%(0)+".dat")

                
            for i in range(numCells_bc):
                 if rec:
                     cntvi=0
                     intsegs=[0,inpseg]
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





def APatten(network_id,
            temperature,
            x_size, 
            y_size, 
            z_size, 
            bc_group_component,
            INPSEGS,
            currinp,
            Imu,
            numCells_bc = 1,
            validate = True,
            rec = False,
            random_seed = 123458,
            generate_lems_simulation = False,
            duration = 1000,  # ms
            dt = 0.01):
    
    seed(randint(0,100000))

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id,type='networkWithTemperature', temperature=str(temperature)+'degC')
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))

    # The names of the groups/populations 
    bc_group = "BasketCells"
        
    add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")

    if currinp:
        stim = PulseGenerator(id="stim",
                              delay='0 ms',
                              duration=str(duration)+' ms',
                              amplitude=str(Imu)+'nA')
        
        nml_doc.pulse_generators.append(stim)
        
        input_list = InputList(id="%s_input"%stim.id,
                               component=stim.id,
                               populations=bc_group)
        
        syn_input = Input(id=0,target="../%s/%i/%s" % (bc_group, 0, bc_group_component),destination="synapses",segment_id=str(0), fraction_along=str(0.5))
            
        input_list.input.append(syn_input)
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
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt, lems_seed=randint(0,10000))

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
            ls.create_output_file(of_bc, "v_"+network_id+"seg_id%i"%(0)+".dat")

                
            for i in range(numCells_bc):
                 if rec:
                     cntvi=0
                     intsegs=INPSEGS
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
   



def VI(network_id,
       temperature,
       x_size,  
       y_size,  
       z_size,  
       bc_group_component,
       Imu,     
       inpseg,
       fracalong,
       numCells_bc = 1,
       currinp=True,
       validate = True,
       rec = False,
       random_seed = 12345,
       generate_lems_simulation = False,
       duration = 1000, 
       dt = 0.01):
    
    seed(random_seed)

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id,type='networkWithTemperature', temperature=str(temperature)+'degC')
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))
    # The names of the groups/populations 
    bc_group = "BasketCells"
        
    # Generate basket cells 
    if numCells_bc>0:
        add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")
       

    if currinp:
        stim = PulseGenerator(id="stim",
                              delay='0 ms',
                              duration=str(duration)+' ms',
                              amplitude=str(Imu)+'nA')
        
        nml_doc.pulse_generators.append(stim)
        
        input_list = InputList(id="%s_input"%stim.id,
                               component=stim.id,
                               populations=bc_group)
          
        syn_input = Input(id=0,target="../%s/%i/%s" % (bc_group, 0, bc_group_component),destination="synapses",segment_id=str(inpseg), fraction_along=str(fracalong))
        input_list.input.append(syn_input)
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
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt)

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
            ls.create_output_file(of_bc, "v_"+network_id+"seg_id%i"%(inpseg)+".dat")
            for i in range(numCells_bc):
                 if rec:
                     cntvi=0
                     intsegs=[0,inpseg]
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



def Rinp(network_id,
         temperature,
         x_size,     # um
         y_size,     # um
         z_size,     # um
         bc_group_component,
         Imu,       # mean input drive in nA
         Ioff,
         inpseg,
         fracalong,
         numCells_bc = 1,
         validate = True,
         rec = False,
         random_seed = 12345,
         generate_lems_simulation = False,
         duration = 1000,  # ms
         dt = 0.01):
    
    seed(random_seed)

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id,type='networkWithTemperature', temperature=str(temperature)+'degC')
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))

    # The names of the groups/populations 
    bc_group = "BasketCells"

    add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")
       
    
    I_amps = [Imu,Ioff]
    stim_delays = [0,duration-500]
    for i in range(2):
        stim = PulseGenerator(id="stim%i"%(i),
                              delay=str(stim_delays[i])+'ms',
                              duration=str(duration)+' ms',
                              amplitude=str(I_amps[i])+'nA')
        nml_doc.pulse_generators.append(stim)
        input_list = InputList(id="%s_input"%stim.id,
                               component=stim.id,
                               populations=bc_group)  
        syn_input = Input(id=i,target="../%s/%i/%s" % (bc_group, 0, bc_group_component),destination="synapses",segment_id=str(inpseg), fraction_along=str(fracalong))
        input_list.input.append(syn_input)
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
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt)

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
            ls.create_output_file(of_bc, "v_"+network_id+"seg_id%i"%(inpseg)+".dat")
                            
            for i in range(numCells_bc):
                 if rec:
                     cntvi=0
                     intsegs=[0,inpseg]
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







def pointCurr(network_id,
              temperature,
              x_size, 
              y_size, 
              z_size, 
              bc_group_component,
              inpseg,
              fracalong,
              numContacts,
              imu,
              numCells_bc = 1,
              currinp=True,
              validate = True,
              rec = False,
              random_seed = 123458,
              generate_lems_simulation = False,
              duration = 1000,  
              dt = 0.01):
    
    seed(randint(0,100000))

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id,type='networkWithTemperature', temperature=str(temperature)+'degC')
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))

    # The names of the groups/populations 
    bc_group = "BasketCells"

     # Generate basket cells 
    if numCells_bc>0:
        add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")
       
    if currinp:
        I_amps = [imu]
        stim_delays = [0]
        
        stim = PulseGenerator(id="stim%i"%(0),
                              delay=str(stim_delays[0])+'ms',
                              duration=str(duration)+' ms',
                              amplitude=str(I_amps[0])+'nA')
        
        nml_doc.pulse_generators.append(stim)

        input_list = InputList(id="%s_input"%stim.id,
                               component=stim.id,
                               populations=bc_group)
        
    
        syn_input = Input(id=0,
                          target="../%s/%i/%s" % (bc_group, 0, bc_group_component),
                          destination="synapses",segment_id=str(inpseg),
                          fraction_along=str(fracalong))
        input_list.input.append(syn_input)
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
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt, lems_seed=randint(0,10000))

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
            ls.create_output_file(of_bc, './v_'+network_id+".dat")
            for i in range(numCells_bc):
                 if rec:
                     cntvi=0
                     intsegs=[0,inpseg]
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







def pointCond(network_id,
              temperature,
              x_size,
              y_size,
              z_size,
              bc_group_component,
              inpseg,
              fracalong,
              numContacts,
              cnd,
              cix,
              numCells_bc = 1,
              condinp=True,
              validate = True,
              rec = False,
              random_seed = 123458,
              generate_lems_simulation = False,
              duration = 1000,
              dt = 0.01):
    
    seed(randint(0,100000))

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id,type='networkWithTemperature', temperature=str(temperature)+'degC')
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)

    if numCells_bc>0:
        nml_doc.includes.append(IncludeType(href='../NeuronModels/'+'%s.cell.nml'%bc_group_component))

    bc_group = "BasketCells"
    add_population_in_rectangular_region(net, bc_group, bc_group_component, numCells_bc, 0, 0, 0, x_size, y_size, z_size, color="0 0 1")
       
    if condinp:
        # Read in the file
        with open('constantSynapseXXX.nml', 'r') as file :
            filedata = file.read()
        # Replace the target string
        print 'constantSynapse%i'%cix
        filedata = filedata.replace('constantSynapseXXX', 'constantSynapse%i'%cix)
        filedata = filedata.replace('gbase="XXX nS"', 'gbase="%.5f nS"'%cnd)

        # Write the file out again
        with open('constantSynapse%i.nml'%cix, 'w') as file:
            file.write(filedata)
                
        nml_doc.includes.append(IncludeType('constantSynapse%i.nml'%cix))
        stim = 'constantSynapse%i'%cix
        input_list = InputList(id="%s_input"%stim,
                               component=stim,
                               populations=bc_group)
        syn_input = Input(id=0,
                          target="../%s/%i/%s" % (bc_group, 0, bc_group_component),
                          destination="synapses",segment_id=str(inpseg),
                          fraction_along=str(fracalong))
        input_list.input.append(syn_input)
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
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt, lems_seed=randint(0,10000))

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
            ls.create_output_file(of_bc, "v_"+network_id+".dat")
            for i in range(numCells_bc):
                 if rec:
                     cntvi=0
                     intsegs=[0,inpseg]
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





