import matplotlib.pyplot as pl
import os
import sys
import numpy as np
import setNeuron_params as sp
### some style settings
labsize  = 26
ticksize = 20
linw     = 4
reds     = pl.get_cmap("Reds")
blues    = pl.get_cmap("Blues")
grays    = pl.get_cmap("Greys")
pl.rcParams['axes.linewidth'] = 4
pl.rcParams['xtick.direction'] ='out'
pl.rcParams['xtick.major.size'] = 8
pl.rcParams['xtick.major.width'] = 4
pl.rcParams['ytick.direction'] ='out'
pl.rcParams['ytick.major.size'] = 8
pl.rcParams['ytick.major.width'] = 4
pl.close('all')

NEURONMOD  = sys.argv[1]
INPSEGS,FRASEGS,DISTS,inps,fras = sp.setNeuPar(NEURONMOD)

path       = './'
dpath      = './'
figformats = ['pdf']

### load sim data
# vi0       = np.loadtxt(path+NEURONMOD+"%iVI.dat"%inps[0])
# vidend    = np.loadtxt(path+NEURONMOD+"%iVI.dat"%inps[1])

# curr0     = np.loadtxt(path+NEURONMOD+'_pointcurrIO500_10000_%i.dat'%inps[0])
# currdend  = np.loadtxt(path+NEURONMOD+'_pointcurrIO0_10000_%i.dat'%inps[1])

epsp      = np.loadtxt(path+NEURONMOD+"EPSP.dat")
apatt     = np.loadtxt(path+NEURONMOD+"AP.dat")

    
### relative EPSP    
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(epsp[:,0],(epsp[:,1]-epsp[:,2])/(epsp[:,3]-epsp[:,4]),'-',lw=linw,color=blues(0.5))
pl.xlabel('distance (um)',size=labsize)
pl.ylabel('EPSP$_{\sf soma}$/EPSP$_{\sf local}$',size=labsize)
pl.xticks([0,100,200],size=ticksize)
pl.xlim(0,270)
pl.yticks([0,0.5,1],size=ticksize)
pl.ylim(0,1.2)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('EPSPatten%s.%s'%(NEURONMOD,ff))

### absolute AP attenuation   
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(apatt[:,0],apatt[:,1],'-',lw=linw,color=blues(0.5))
pl.xlabel('distance (um)',size=labsize)
pl.ylabel('AP amplitude (mV)',size=labsize)
pl.xticks([0,100,200],size=ticksize)
pl.xlim(0,270)
pl.yticks([0,30,60,90],size=ticksize)
pl.ylim(0,110)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('APattenabs%s.%s'%(NEURONMOD,ff))

### relative AP attenuation      
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(apatt[:,0],apatt[:,1]/apatt[0,1],'-',lw=linw,color=blues(0.5))
pl.xlabel('distance (um)',size=labsize)
pl.ylabel('AP attenuation (%)',size=labsize)
pl.xticks([0,100,200],size=ticksize)
pl.xlim(0,270)
pl.yticks([0,0.2,0.4,0.6,0.8,1],size=ticksize)
pl.ylim(0,1.1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('APattenrel%s.%s'%(NEURONMOD,ff))

'''
  
### VI relationship soma    
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(vi0[:,0],vi0[:,1],'-',lw=linw,color=blues(0.5))       
pl.xlabel('input current (nA)',size=labsize)
pl.ylabel('potential @ soma (mV)',size=labsize)
pl.xticks([-0.2,-0.1,0],size=ticksize)
pl.yticks([-100,-80,-60],size=ticksize)
pl.ylim(-100,-60)
pl.xlim(-0.2,0.05)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('VIsoma%s.%s'%(NEURONMOD,ff))

### VI relationship apical dend (~230um)    
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(vidend[:,0],vidend[:,1],'-',lw=linw,color=blues(0.5))
pl.xlabel('input current (nA)',size=labsize)
pl.ylabel('potential @ 230um (mV)',size=labsize)
pl.xticks([-0.2,0,0.2,0.4],size=ticksize)
pl.xlim(-0.2,0.4)
pl.yticks([-80,-40,0],size=ticksize)
pl.ylim(-90,0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('VIdend%s.%s'%(NEURONMOD,ff))

### FI relationship soma    
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(curr0[:,0], curr0[:,2],'-',lw=linw,color=blues(0.5))
pl.xlabel('input current (nA)',size=labsize)
pl.ylabel('rate (1/s)',size=labsize)
pl.xticks([0,0.2,0.4,0.6,0.8],size=ticksize)
pl.xlim(0,0.8)
pl.yticks([0,100,200],size=ticksize)
pl.ylim(-10,220)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('FIsoma%s.%s'%(NEURONMOD,ff))

### FI relationship apical dend (~230um)        
fig,ax=pl.subplots(figsize=(5,5))
pl.plot(currdend[:,0], currdend[:,2],'-',lw=linw,color=blues(0.5))
pl.xlabel('input current (nA)',size=labsize)
pl.ylabel('rate (1/s)',size=labsize)
pl.xticks([0,0.2,0.4,0.6,0.8],size=ticksize)
pl.xlim(0,0.8)
pl.yticks([0,100,200],size=ticksize)
pl.ylim(-10,220)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
pl.subplots_adjust(bottom=0.22,left=0.27,right=0.95,top=0.97)
for ff in figformats:
    pl.savefig('FIdend%s.%s'%(NEURONMOD,ff))
   
'''
pl.show()
