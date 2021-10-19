import sys

assert (sys.argv[1] in ['jonasnmBC1Klt','jonasnmBC2Klt','jonasnmBC3Klt','jonasnmBC4Klt','jonasnmBC5Klt','jonasnmBC6Klt','BSBC5']), "invalid input"

NEURONMOD = sys.argv[1]
NRNPATH   = sys.argv[2]
RUNIDS = ['AP','EPSP']#,'VI','PointCurr','Rinp']

outputfile = open('runSingleScan.sh', 'a+')
for runID in RUNIDS:
    outputfile.write("python run%s.py %s %s\n"%(runID,NEURONMOD,NRNPATH))
    outputfile.write("chmod u+x codrun%s.sh; ./codrun%s.sh\n"%(runID,runID))
    outputfile.write("rm codrun*;rm LEM*;rm *net.nml;rm *mod;rm time*;rm *hoc\n\n")
    outputfile.write("python ausw%s.py %s\n\n"%(runID,NEURONMOD))
    
outputfile.close()    


