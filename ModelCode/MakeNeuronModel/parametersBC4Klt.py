import numpy as np


border        = 120.      # in mum
border2       = 200.
# passive membrane properties
Ri            = 178       # in Ohm cm
Cm            = 0.92      # in muF cm-2
Vinit2        = -66.3     # in mV
erev2         = -75.      # in mV 
Rm1           = 5000      # in Ohm cm2
Rm2           = 21000.
Rm3           = 139000
gl1           = 1000./Rm1 # in mS cm-2
gl2           = 1000./Rm2
gl3           = 1000./Rm3
#gl1,gl2,gl3  = 0.2, 0.048, 0.0072

temperature   = 23        # in degC

# active membrane properties
## Na ##

gna_soma2     = 120      # in mS cm-2 
ena_soma2     = 55.      # in mV 
gna_dend2     = 5.       # in mS cm-2 
ena_dend2     = 55.      # in mV
gna_p_axon    = 400      # in mS cm-2 
ena_p_axon    = 55.      # in mV
gna_d_axon    = 35.      # in mS cm-2 
ena_d_axon    = 55.      # in mV

## K ##
gk_soma       = 60.      # in mS cm-2 
ek_soma       = -90.     # in mV 
gk_dend       = 60       # in mS cm-2
ek_dend       = -90.     # in mV
gk_apic       = 60       # in mS cm-2 
ek_apic       = -90.     # in mV
gk_axon       = 60.      # in mS cm-2 
ek_axon       = -90.     # in mV
gKdist        = 30.
gKprox        = 60.


#### x 10 factor from transformation to SI units S/m**2= 1000 mS/10000 cm**2
dendnuFct_gl     = "(%(gl).8f"%{'gl':gl2*10} + " + %(glnu).8f"%{'glnu':(gl1-gl2)*10} +" * (H(%(bord)i"%{"bord":border}+"-p)))"
#normal K channel proximally
dendnuFct_K0     = "(%(gl).8f"%{'gl':0.*10.} + " + %(glnu).8f"%{'glnu':(gKprox)*10} +" * (H(%(bord)i"%{"bord":border2}+"-p)))"
dendnuFct_K1     = "(%(gl).8f"%{'gl':gKdist*10.} + " + %(glnu).8f"%{'glnu':(0.-gKdist)*10} +" * (H(%(bord)i"%{"bord":border2}+"-p)))"
dendnuFct_na   = "%(gna).8f"%{'gna':gna_dend2*10}
axonnuFct_na     = "(%(gl).8f"%{'gl':gna_d_axon*10} + " + %(glnu).8f"%{'glnu':(gna_p_axon-gna_d_axon)*10} +" * (H(%(bord)i"%{"bord":border}+"-p)))"

