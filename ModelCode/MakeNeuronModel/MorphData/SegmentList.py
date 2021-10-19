SEGPATH = './MorphData/'
def sl1():
    segs0 = np.loadtxt(SEGPATH+'BC1_apic_0_apistim.dat')
    segs1 = np.loadtxt(SEGPATH+'BC1_apic_51_apistim.dat')
    
    apilis0 = [int(_) for _ in segs0[:,0]]
    apilis1 = [int(_) for _ in segs1[:,0]]

    apilis  = apilis0
    apilis  = np.append(apilis,apilis1)

    fraclis0 = [_ for _ in segs0[:,1]]
    fraclis1 = [_ for _ in segs1[:,1]]
    fraclis  = fraclis0
    fraclis  = np.append(fraclis,fraclis1)

    m3segs = np.loadtxt(SEGPATH+'peri_frac_BC1.dat')
    m3segs[np.nonzero(m3segs[:,1]==1)]=0.99
    baslis = [int(_) for _ in m3segs[:,0]]

    return apilis,fraclis,baslis


def sl2():
    ### load relevant segment data for NEURONMOD to be used
    segs2 = np.loadtxt(SEGPATH+'apic_2_stim.dat')
    segs18 = np.loadtxt(SEGPATH+'apic_18_stim.dat')
    segs34 = np.loadtxt(SEGPATH+'apic_34_stim.dat')
    segs57 = np.loadtxt(SEGPATH+'apic_57_stim.dat')
    segs64 = np.loadtxt(SEGPATH+'apic_64_stim.dat')
    segs77 = np.loadtxt(SEGPATH+'apic_77_stim.dat')

    apilis0 = [int(_) for _ in segs2[:,0]]
    apilis1 = [int(_) for _ in segs18[:,0]]
    apilis2 = [int(_) for _ in segs34[:,0]]
    apilis3 = [int(_) for _ in segs57[:,0]]
    apilis4 = [int(_) for _ in segs64[:,0]]
    apilis5 = [int(_) for _ in segs77[:,0]]
    #apilis  = [apilis0,apilis1,apilis2,apilis3,apilis4,apilis5] # if indiv branches needed
    apilis  = apilis0
    apilis  = np.append(apilis,apilis1)
    apilis  = np.append(apilis,apilis2)
    apilis  = np.append(apilis,apilis3)
    apilis  = np.append(apilis,apilis4)
    apilis  = np.append(apilis,apilis5)
    fraclis0 = [_ for _ in segs2[:,1]]
    fraclis1 = [_ for _ in segs18[:,1]]
    fraclis2 = [_ for _ in segs34[:,1]]
    fraclis3 = [_ for _ in segs57[:,1]]
    fraclis4 = [_ for _ in segs64[:,1]]
    fraclis5 = [_ for _ in segs77[:,1]]
    #fraclis  = [fraclis0,fraclis1,fraclis2,fraclis3,fraclis4,fraclis5]
    fraclis  = fraclis0
    fraclis  = np.append(fraclis,fraclis1)
    fraclis  = np.append(fraclis,fraclis2)
    fraclis  = np.append(fraclis,fraclis3)
    fraclis  = np.append(fraclis,fraclis4)
    fraclis  = np.append(fraclis,fraclis5)

    m3segs = np.loadtxt(SEGPATH+'perisomapi_seg_frac2.dat')
    m3segs[np.nonzero(m3segs[:,1]==1)]=0.99
    baslis = [int(_) for _ in m3segs[:,0]]
    
    return apilis,fraclis,baslis

def sl3():
    segs0 = np.loadtxt(SEGPATH+'BC3_apic_0_apistim.dat')
    apilis0 = [int(_) for _ in segs0[:,0]]
    apilis  = apilis0
    
    fraclis0 = [_ for _ in segs0[:,1]]
    fraclis  = fraclis0
   
    m3segs = np.loadtxt(SEGPATH+'peri_frac_BC3.dat')
    m3segs[np.nonzero(m3segs[:,1]==1)]=0.99
    baslis = [int(_) for _ in m3segs[:,0]]

    return apilis,fraclis,baslis

def sl4():
    segs0 = np.loadtxt(SEGPATH+'BC4_apic_0_apistim.dat')
    apilis0 = [int(_) for _ in segs0[:,0]]
    apilis  = apilis0
    
    fraclis0 = [_ for _ in segs0[:,1]]
    fraclis  = fraclis0
   
    m3segs = np.loadtxt(SEGPATH+'peri_frac_BC4.dat')
    m3segs[np.nonzero(m3segs[:,1]==1)]=0.99
    baslis = [int(_) for _ in m3segs[:,0]]

    return apilis,fraclis,baslis

def sl5():
    segs0 = np.loadtxt(SEGPATH+'BC5_apic_0_apistim.dat')
    segs1 = np.loadtxt(SEGPATH+'BC5_apic_19_apistim.dat')
    segs2 = np.loadtxt(SEGPATH+'BC5_apic_384_apistim.dat')
    apilis0 = [int(_) for _ in segs0[:,0]]
    apilis1 = [int(_) for _ in segs1[:,0]]
    apilis2 = [int(_) for _ in segs2[:,0]]
    apilis  = apilis0
    apilis  = np.append(apilis,apilis1)
    apilis  = np.append(apilis,apilis2)
    fraclis0 = [_ for _ in segs0[:,1]]
    fraclis1 = [_ for _ in segs1[:,1]]
    fraclis2 = [_ for _ in segs2[:,1]]
    fraclis  = fraclis0
    fraclis  = np.append(fraclis,fraclis1)
    fraclis  = np.append(fraclis,fraclis2)
    m3segs = np.loadtxt(SEGPATH+'peri_frac_BC5.dat')
    m3segs[np.nonzero(m3segs[:,1]==1)]=0.99
    baslis = [int(_) for _ in m3segs[:,0]]

    return apilis,fraclis,baslis


def sl6():
    segs0 = np.loadtxt(SEGPATH+'BC6_apic_0_apistim.dat')
    segs1 = np.loadtxt(SEGPATH+'BC6_apic_289_apistim.dat')

    apilis0 = [int(_) for _ in segs0[:,0]]
    apilis1 = [int(_) for _ in segs1[:,0]]

    apilis  = apilis0
    apilis  = np.append(apilis,apilis1)

    fraclis0 = [_ for _ in segs0[:,1]]
    fraclis1 = [_ for _ in segs1[:,1]]
    fraclis  = fraclis0
    fraclis  = np.append(fraclis,fraclis1)

    m3segs = np.loadtxt(SEGPATH+'peri_frac_BC6.dat')
    m3segs[np.nonzero(m3segs[:,1]==1)]=0.99
    baslis = [int(_) for _ in m3segs[:,0]]


    return apilis,fraclis,baslis


def segml(ind):
    if ind==1:
        apilis,fraclis,baslis=sl1()
    if ind==2:
        apilis,fraclis,baslis=sl2()
    if ind==3:
        apilis,fraclis,baslis=sl3()
    if ind==4:
        apilis,fraclis,baslis=sl4()
    if ind==5:
        apilis,fraclis,baslis=sl5()
    if ind==6:
        apilis,fraclis,baslis=sl6()  
    return apilis,fraclis,baslis 
