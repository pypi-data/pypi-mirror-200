# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 17:21:31 2023

@author: eccn3
"""

from ase.io import read
from AtomsHelper.atoms_helper import geom2graph

names = ['Examples/point_cloud/CH3/CONTCAR_LDA',
         'Examples/point_cloud/CH3/CONTCAR_PBE']

atoms = []
geoms = []
point = []

for count, i in enumerate(names):
    atoms.append(read(i))
    geoms.append(geom2graph(atoms=atoms[count]))
for i in geoms:
    i.gen_graph(fill_bonds=False)
    
    
    
    