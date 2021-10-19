To run a network simulation scan from commandline, type

chmod u+x RunSim.sh; ./RunSim.sh

That will create a network scan through an array of poisson rates per AMPA synapse and dispersions for one given peak GABA amplitude (see makeNetwork_fullmodel.py for specifics).

To run a network with sinusoidally modulated current, change makeNetwork_fullmodel.py makeNetwork_fullmodel_Theta.py 

If you use a recent version of NeuroML2 (including jnml, pyneuroml) use LAPTOP=False (or 0). Worked for Neuron7.4, neuroml version 0.2.18, numpy version 1.11.0, python 2.7.12, but cannot be guaranteed to work without adaptations with newer software versions.

Author: Birgit Kriener, Dec 2019
