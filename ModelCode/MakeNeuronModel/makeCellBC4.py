execfile('parametersBC4Klt.py')
def makeCell(cellid, morphfile):
    
    import parametersBC4Klt as pm 
    import neuroml
    import neuroml.loaders as loaders
    import neuroml.writers as writers
    import numpy as np

    ### cell morphology
    fn = morphfile
    doc = loaders.NeuroMLLoader.load(fn)
    print("Loaded morphology file from: "+fn)

    cell = doc.cells[0]

    ### set up subgroups of cell morphology
    axon_seg_group = neuroml.SegmentGroup(id="axon_group",neuro_lex_id="GO:0030424")  # See http://amigo.geneontology.org/amigo/term/GO:0030424
    soma_seg_group = neuroml.SegmentGroup(id="soma_group",neuro_lex_id="GO:0043025")
    dend_seg_group = neuroml.SegmentGroup(id="dendrite_group",neuro_lex_id="GO:0030425")
    inhomogeneous_parameter_dend = neuroml.InhomogeneousParameter(id="PathLengthOverDendrites",variable="p",metric="Path Length from root")
    inhomogeneous_parameter_axon = neuroml.InhomogeneousParameter(id="PathLengthOverAxon",variable="p",metric="Path Length from root")
    dend_seg_group.inhomogeneous_parameters.append(inhomogeneous_parameter_dend)
    axon_seg_group.inhomogeneous_parameters.append(inhomogeneous_parameter_axon)


    included_sections = []

    for seg in cell.morphology.segments:
        neuron_section_name = seg.name[seg.name.index('_')+1:]
        if not neuron_section_name in included_sections:
            if 'axon' in seg.name: 
                axon_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
                
            elif 'soma' in seg.name:
                soma_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
            
            elif 'dend' in seg.name:
                dend_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
            
            elif 'apic' in seg.name:
                dend_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
                
            else: # raise alarm if unidentified segment!
                raise Exception("Segment: %s is not axon, dend or soma!"%seg)
        
        included_sections.append(neuron_section_name)

    ### assign to cell object    
    cell.morphology.segment_groups.append(axon_seg_group)
    cell.morphology.segment_groups.append(soma_seg_group)
    cell.morphology.segment_groups.append(dend_seg_group)
    

    ### channels and properties

    channel_densities = []
    channel_density_non_uniforms = []

    
    ### leak: soma
    cd_pas_soma = neuroml.ChannelDensity(id="pas_chan_soma", segment_groups=soma_seg_group.id, ion="non_specific", ion_channel="pas", erev=str(pm.erev2)+" mV", cond_density=str(pm.gl1)+" mS_per_cm2")
    channel_densities.append(cd_pas_soma)
    
    ### leak: nonuniform g_L across dendrite
    cdnu_pas_dend = neuroml.ChannelDensityNonUniform(id="pas_chan_dend", ion="non_specific", ion_channel="pas", erev=str(pm.erev2)+" mV")
    vppas = neuroml.VariableParameter(parameter="condDensity", segment_groups=dend_seg_group.id)
    cdnu_pas_dend.variable_parameters.append(vppas)
    vppas.inhomogeneous_value = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOverDendrites",value=pm.dendnuFct_gl) 
    channel_density_non_uniforms.append(cdnu_pas_dend)

    ### leak: axon
    cd_pas_axon = neuroml.ChannelDensity(id="pas_chan_axon", segment_groups=axon_seg_group.id, ion="non_specific", ion_channel="pas", erev=str(pm.erev2)+" mV", cond_density=str(pm.gl3)+" mS_per_cm2")
    channel_densities.append(cd_pas_axon)
    
    ### Na: soma
    cd_na_soma = neuroml.ChannelDensity(id="na_chan_soma", segment_groups=soma_seg_group.id, ion="non_specific", ion_channel="Na_BC", erev=str(pm.ena_soma2)+" mV", cond_density=str(pm.gna_soma2)+" mS_per_cm2")
    channel_densities.append(cd_na_soma)

    ### Na: dendrite
    cdnu_na_dend = neuroml.ChannelDensityNonUniform(id="nanu_chan_dend", ion="non_specific", ion_channel="Na_BC", erev=str(pm.ena_dend2)+" mV")
    vnadend = neuroml.VariableParameter(parameter="condDensity", segment_groups=dend_seg_group.id)
    cdnu_na_dend.variable_parameters.append(vnadend)
    vnadend.inhomogeneous_value = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOverDendrites",value=pm.dendnuFct_na) 
    channel_density_non_uniforms.append(cdnu_na_dend)
    
    ### Na: nonuniform Na across axon
    cdnu_na_axon = neuroml.ChannelDensityNonUniform(id="na_chan_axon",ion="non_specific", ion_channel="Na_BC", erev=str(pm.ena_p_axon)+" mV")
    vpaxon = neuroml.VariableParameter(parameter="condDensity", segment_groups=axon_seg_group.id)
    cdnu_na_axon.variable_parameters.append(vpaxon)
    vpaxon.inhomogeneous_value = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOverAxon",value=pm.axonnuFct_na) 
    channel_density_non_uniforms.append(cdnu_na_axon)

    
    ### K: soma
    cd_k_soma = neuroml.ChannelDensity(id="k_chan_soma", segment_groups=soma_seg_group.id, ion="non_specific", ion_channel="K_BClt", erev=str(pm.ek_soma)+" mV", cond_density=str(pm.gk_soma)+" mS_per_cm2")
    channel_densities.append(cd_k_soma)

    ### K: dendrite 
       
    cdnu_k_dend0 = neuroml.ChannelDensity(id="k_chan_dend0", ion="non_specific", ion_channel="K_BClt", erev=str(pm.ek_dend)+" mV")
    vpk_dend0 = neuroml.VariableParameter(parameter="condDensity", segment_groups=dend_seg_group.id)
    cdnu_k_dend0.variable_parameters.append(vpk_dend0)
    vpk_dend0.inhomogeneous_value = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOverDendrites",value=pm.dendnuFct_K0) 
    channel_density_non_uniforms.append(cdnu_k_dend0)


    cdnu_k_dend1 = neuroml.ChannelDensity(id="k_chan_dend1", ion="non_specific", ion_channel="K_BC40act", erev=str(pm.ek_dend)+" mV")
    vpk_dend1 = neuroml.VariableParameter(parameter="condDensity", segment_groups=dend_seg_group.id)
    cdnu_k_dend1.variable_parameters.append(vpk_dend1)
    vpk_dend1.inhomogeneous_value = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOverDendrites",value=pm.dendnuFct_K1) 
    channel_density_non_uniforms.append(cdnu_k_dend1)
   
    
    ### K: axon 
    cd_k_axon = neuroml.ChannelDensity(id="k_chan_axon", segment_groups=axon_seg_group.id, ion="non_specific", ion_channel="K_BClt", erev=str(pm.ek_axon)+" mV", cond_density=str(pm.gk_axon)+" mS_per_cm2")
    channel_densities.append(cd_k_axon)

    ### membrane properties

    specific_capacitances = []

    specific_capacitances.append(neuroml.SpecificCapacitance(value=str(pm.Cm)+' uF_per_cm2', segment_groups='all'))
    init_memb_potentials = [neuroml.InitMembPotential(value=str(pm.Vinit2)+" mV", segment_groups='all')]
        
    spike_threshold = [neuroml.SpikeThresh(value="0 mV", segment_groups='all')]
    
    membrane_properties = neuroml.MembraneProperties(
        channel_density_non_uniforms=channel_density_non_uniforms,
        channel_densities=channel_densities,
        specific_capacitances=specific_capacitances,
        init_memb_potentials=init_memb_potentials,
        spike_threshes=spike_threshold)
    
    ### intracellular properties

    resistivities = []
    resistivities.append(neuroml.Resistivity(
        value=str(pm.Ri)+" ohm_cm", segment_groups='all'))

    intracellular_properties = neuroml.IntracellularProperties(resistivities=resistivities)

    bp = neuroml.BiophysicalProperties(id="biophys",
                                   intracellular_properties=intracellular_properties,
                                   membrane_properties=membrane_properties)
                                   
    cell.biophysical_properties = bp

    cell.id = cellid

    nml_doc2 = neuroml.NeuroMLDocument(id=cell.id)

    nml_doc2.includes.append(neuroml.IncludeType('../SimEx/channelConvert/pas.channel.nml')) 
    nml_doc2.includes.append(neuroml.IncludeType('../SimEx/channelConvert/Na_BC.channel.nml')) 
    nml_doc2.includes.append(neuroml.IncludeType('../SimEx/channelConvert/K_BClt.channel.nml'))
    nml_doc2.includes.append(neuroml.IncludeType('../SimEx/channelConvert/K_BC40act.channel.nml'))
   
    nml_doc2.cells.append(cell)

    nml_file = cell.id+'.cell.nml'

    writers.NeuroMLWriter.write(nml_doc2,nml_file)

    print("Saved modified morphology file to: "+nml_file)
                                   
                                   
    ###### Validate the NeuroML ######    

    from neuroml.utils import validate_neuroml2
    
    validate_neuroml2(nml_file)
    

