#!/usr/bin/env python
import json as js
from irff.reax_data import get_data
from irff.initCheck import init_bonds


with open('ffield.json','r') as lf:
    j = js.load(lf)
    p_ = j['p']
    m_ = j['m']
    bo_layer_ = j['bo_layer']
    rcut = j['rcut']
    rcuta = j['rcutBond']

spec,bonds,offd,angs,tors,hbs = init_bonds(p_)

data = get_data(structure='cl20',
                direc='cl20.traj',
                dft='ase',
                rcut=rcut,
                rcuta=rcuta,
                batch=50,
                p=p_,spec=spec,bonds=bonds,
                angs=angs,tors=tors,hbs=hbs,
                variable_batch=True)

# print(len(data.bond))
# print(data.bond)
#print(data.B)
print(data.rbd.shape)

print(data.theta.shape)
#print(data.abij)
print('\n-  rv  -\n',len(data.rv))
print('\n-  nvb  -\n',data.nvb)
print('\n-  nhb  -\n',data.nhb)
# print(data.batch)
# print(data.nbd)
# for bd in data.dilink:
#     print(bd,data.dilink[bd])




