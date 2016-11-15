#! /usr/bin/env python
# -*- coding: latin-1; -*-
# $Id: $

import sys, os, os.path

runPath = os.path.dirname(sys.modules[__name__].__file__)
filePath = os.path.abspath(os.path.dirname(sys.argv[0]))
fileName = os.path.splitext(os.path.basename(__file__))[0]

import pfem

import pfemtools as wt
import viewer as v
    
w = None

class Module:
    def __init__(self, w, msh, pbl, scheme, extManager, gui):
       self.w = w
       self.msh = msh
       self.pbl = pbl       
       self.scheme = scheme
       self.extManager = extManager
       self.gui = gui

def getPfem():
    global w
    if w: return w
    w = pfem
    
    mshFile = runPath+os.sep+'birdImpact_deformable_panel_Mtf_Pfem.msh'
    
    print 'mshFile: ', mshFile
    
    msh = w.MshData()
    msh.load(mshFile)
    print msh
    
    rho0 = 1000.
    mu = 0.001
    U0 = 100
    N = 10

    pbl = w.Problem()
    pbl.rho0 = rho0
    pbl.mu = mu
    pbl.nonLinAlgorithm = 1
    pbl.solScheme = 1
    pbl.alpha = 1.2
    pbl.beta = 0.
    pbl.gravity = 0.
    pbl.scalingU = U0
    
    scheme = w.BackwardEuler(msh, pbl)

    w.Medium(msh, 13, mu, rho0, 3)
    w.Medium(msh, 16, mu, rho0, 1)
    
    # boundaries
    w.Boundary(msh, 15, 3, 0.0)
    w.Boundary(msh, 13, 1, 0.0)
    w.Boundary(msh, 13, 2, 0.0)
    
    #Initial velocity
    bird = w.Group(msh, 16)
    loadingset = w.LoadingSet(msh)
    loadingset.add(1,w.InitialVelocity(msh,bird,0.,-U0,0.))
    
    R = 0.01
    d = 2.5*(R/N)
    dt = 2e-6

    scheme.ttot = 40*((4*R)/U0 + d/U0)
    scheme.dt = dt
    scheme.savefreq=1
    scheme.nthreads=4
    scheme.gamma = 0.5
    scheme.omega = 0.5
    scheme.addRemoveNodesOption = True
    scheme.tollNLalgo = 1e-7
    
    #Results
    extManager = w.ExtractorsManager(msh)
    extManager.add(1,w.PositionExtractor(msh,315))
    '''extManager.add(1,w.IntForceExtractor(msh,"Wall"))
    extManager.add(2,w.ExtForceExtractor(msh,"Wall"))
    extManager.add(3,w.IneForceExtractor(msh,"Wall"))
    extManager.add(4,w.PressureExtractor(msh,"Wall"))
    extManager.add(5,w.PositionExtractor(msh,"Wall"))'''
    extManager.add(6,wt.KineticEnergyExtractor(msh,pbl,16))
    extManager.add(7,wt.ViscousEnergyExtractor(msh,pbl,scheme,16))
    extManager.add(8,wt.PressureWorkExtractor(msh,pbl,scheme,16))
    extManager.add(9,w.MassExtractor(msh,16))
    
    gui = v.MeshViewer(msh, scheme) 
    
    return Module(w, msh, pbl, scheme, extManager, gui)