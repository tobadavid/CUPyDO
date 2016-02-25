#!/usr/bin/env python
# -*- coding: latin-1; -*-
# ~/dev/Offi/oo_metaB/bin/Metafor -nogui ./fsi.py

from toolbox.utilities import *
workdir = 'workspace/beam'

def getMetafor(p={}):
    import beam
    return beam.getMetafor(p)


class MtfSolver:
    def __init__(self):
        self.t1      = 0.0        
        self.t2      = 0.0
        self.metafor = None

    def run(self, t1, t2):
        if(not self.metafor):
            self.__firstrun(t1, t2)
        else:
            self.__nextrun(t1, t2)
        self.t1=t1
        self.t2=t2

    def __firstrun(self, t1, t2):
        load(__name__)
        setDir(workdir)
        #p = {'tend' : 0.04 }
        p = {}
        self.metafor = instance(p)
        
        tsm = self.metafor.getTimeStepManager()
        dt=t2-t1
        dt0=dt
        dtmax=dt
        tsm.setInitialTime(t1, dt0)
        tsm.setNextTime(t2, 1, dtmax)
        meta()        

    def __nextrun(self, t1, t2):
        if self.t1==t1:
            # rerun from t1
            if self.t2!=t2:
                raise Exception("bad t2 (%f!=%f)" % (t2, self.t2)) 
            
            loader = fac.FacManager(self.metafor)
            nt = loader.lookForFile(0)
            loader.eraseAllFrom(nt)
            self.metafor.getTimeIntegration().restart(nt)
        else:
            raise Exception("not implemented") 

def main():
    solid = MtfSolver()
    for i in range(10):
        t1=0.0
        t2=1.0
        print '='*80
        print "running from %f to %f: try #%d" % (t1,t2,i+1)
        print '='*80
        solid.run(t1,t2)
    
if __name__ == "__main__":
    main()


