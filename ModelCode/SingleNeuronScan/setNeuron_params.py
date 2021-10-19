import numpy as np
path = '../MakeNeuronModel/MorphData/'

def setNeuPar(NEURONMOD):
    assert (NEURONMOD in ['jonasnmBC1','jonasnmBC2','jonasnmBC3','jonasnmBC4','jonasnmBC5','jonasnmBC6','jonasnmBC1Klt','jonasnmBC2Klt','jonasnmBC3Klt','jonasnmBC4Klt','jonasnmBC5Klt','jonasnmBC6Klt','BSBC5']), "invalid input"
    
    if 'BC1' in NEURONMOD:
        bla      = np.loadtxt(path+'BC1_apic_181_atten.dat')
        INPSEGS  = [int(bla[_,0]) for _ in range(len(bla))]
        FRASEGS  = [bla[_,1] for _ in range(len(bla))]
        DISTS    = [bla[_,2] for _ in range(len(bla))]
        inps     = [0,27381]
        fras     = [0.5,0.41176]
        
    if 'BC2' in NEURONMOD:
        bla      = np.loadtxt(path+'BC2_apic_91_atten.dat')
        INPSEGS  = [int(bla[_,0]) for _ in range(len(bla))]
        FRASEGS  = [bla[_,1] for _ in range(len(bla))]
        DISTS    = [bla[_,2] for _ in range(len(bla))]
        inps     = [0,18046]
        fras     = [0.5,0.66]
        
    if 'BC3' in NEURONMOD:
        bla      = np.loadtxt(path+'BC3_apic_415_atten.dat')
        INPSEGS  = [int(bla[_,0]) for _ in range(len(bla))]
        FRASEGS  = [bla[_,1] for _ in range(len(bla))]
        DISTS    = [bla[_,2] for _ in range(len(bla))]
        inps     = [0,39595]
        fras     = [0.5,0.894737]
        
    if 'BC4' in NEURONMOD:
        bla      = np.loadtxt(path+'BC4_apic_662_atten.dat')
        INPSEGS  = [int(bla[_,0]) for _ in range(len(bla))]
        FRASEGS  = [bla[_,1] for _ in range(len(bla))]
        DISTS    = [bla[_,2] for _ in range(len(bla))]
        inps     = [0,36601]
        fras     = [0.5,0.6]
        
    if 'BC5' in NEURONMOD:
        bla      = np.loadtxt(path+'BC5_apic_562_atten.dat')
        INPSEGS  = [int(bla[_,0]) for _ in range(len(bla))]
        FRASEGS  = [bla[_,1] for _ in range(len(bla))]
        DISTS    = [bla[_,2] for _ in range(len(bla))]
        inps     = [0,46425]
        fras     = [0.5,0.47253]
        
    if 'BC6' in NEURONMOD:
        bla      = np.loadtxt(path+'BC6_apic_431_atten.dat')
        INPSEGS  = [int(bla[_,0]) for _ in range(len(bla))]
        FRASEGS  = [bla[_,1] for _ in range(len(bla))]
        DISTS    = [bla[_,2] for _ in range(len(bla))]
        inps     = [0,56903]
        fras     = [0.5,0.667]

    return INPSEGS,FRASEGS,DISTS,inps,fras
