##################################################################
#                                                                #
# SINGLE NEURON BEHAVIOR                                         #
#                                                                #
# Run, evaluate and plot single neuron ephys data                #
#                                                                #
# Author: B Kriener, Dec 2019; update Sep 2021                   #
#                                                                #
###################################################################


To run single cell scan, first set the neuronmodel you want to run in execRun.sh (as is that is jonasnmBC2; replace this with one of the models present in ../NeuronModels/ (note: only the part that comes before .cell.nml). Then type

chmod u+x execRun.sh;./execRun.sh

in commandline.

This will compile and execute the following routines:

runAP.py          # runs sims to compute the AP attenuation along long apical dendrites
auswAP.py         # evaluates data produced by runAP.py

runEPSP.py        # runs sims to compute relative EPSP attenuation along long apical dendrite
auswEPSP.py       # evaluates data produced by runEPSP.py

runRinp.py        # runs simulation to compute input resistance
auswRinp.py       # evaluates data produced by runRinp.py

These two will take a while and are thus not in per default:

runVI.py          # runs VI-relationship at soma and distal apical dendritic location (~230um)
auswVI.py         # evaluates data produced by runVI.py

runPointCurr.sh   # runs simulations of placing a point current (DC) source along a long apical dendrite (~10um steps)
auswPointCurr.py  # evaluates data produced by runPointCurr.py


You can then generate plots by calling:
python singleNeuron_plot.py


