#!/usr/bin/env python
import json as js
from irff.reax_data import get_data
from irff.initCheck import init_bonds
from irff.reax_nn_develop import ReaxFF_nn


rn = ReaxFF_nn(libfile='ffield.json',
               dataset={'cl20':'cl20.traj'},
               dft='ase',
               opt=[],optword='nocoul',
               be_layer=[9,0],
               mf_layer=[9,1],
               batch=1000,
               clip_op=False,
               interactive=True,
               to_train=False) 
molecules = rn.initialize()
rn.session(learning_rate=1.0e-10,method='AdamOptimizer')


bop = rn.get_value(rn.bop['cl20'])
print('\n-  bop  -\n',bop.shape)

dbop = rn.get_value(rn.dbop['cl20'])
print('\n-  dbop  -\n',dbop.shape)

dDeltap = rn.get_value(rn.dDeltap['cl20'])
print('\n-  dDeltap  -\n',dDeltap.shape)

