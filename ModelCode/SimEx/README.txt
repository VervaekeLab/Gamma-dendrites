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

In the paper we typically varied the rate per AMPA-synapse (pfsfreq), the peak amplitude of the GABA-synapses and the degree of input heterogeneity (pfsdisp). In particular, pfsfreq is drawn from a Gaussian with mean pfsfreq and variance pfsfreq*pfsdisp.

Python code adapted and modified from existing code in 
https://github.com/OpenSourceBrain/OpenCortex

To run from commandline:

python makeNetwork.py
chmod u+x mysim0.sh;./mysim0.sh


SOFTWARE VERSIONS : python/2.7.15; numpy/1.11.0; scipy/0.17.0; 
                    neuroml/0.2.18; jNeuroML/0.10.1; pyNeuroML/0.1.15; neuron/7.4

No guarantees for the code to work with newer versions of NeuroML2, PyNeuroML, jnml, Neuron, python.


Author: Birgit Kriener, April 2017
