# Parvalbumin interneuron dendrites enhance gamma oscillations
### Birgit Kriener, Hua Hu, Koen Vervaeke
#### Institute of Basic Medical Sciences, Department of Physiology, University of Oslo

## Code and technical details

The folder ModelCode contains the basic code to reproduce all simulations that produced the results presented in the paper.
Simulation scripts are written in python/2.7 and generate xml and nml files that can be used to run simulations in NEURON/7.4 via the pyNeuroML-interface in NeuroML/v2beta4 (https://www.neuroml.org/neuromlv2).

* **ModelCode/NeuronModels** contains the nml-files for cell morphologies and biophysical parameters. These can be generated with the code contained in **ModelCode/MakeNeuronModel** (see ModelCode/MakeNeuronModel/README.txt).
* **ModelCode/SingleNeuronScan** contains code needed for single cell simulations and analysis (see ModelCode/SingleNeuronScan/README.txt).
* **ModelCode/SimEx** contains basic code for ring network simulations (see ModelCode/SimEx/README.txt).

The folder **AdditionalMaterial** contains some more detailed information on the derivation of connectivity statistics in ring and two-dimensional networks, as well as the synchrony measure used and discussed in the paper.
