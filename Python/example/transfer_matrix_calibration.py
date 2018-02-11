from src import structure
from src import plotting
import numpy as np
# Filmetric calculator
# https://www.filmetrics.com/reflectance-calculator?wmin=400&wmax=700&wstep=1&angle=30&pol=mixed&units=nm&mmat=ITO&mat[]\
# =SiO2&d[]=250&mat[]=MgF2&d[]=250&mat[]=Al2O3&d[]=250&smat=ITO&sptype=r
mats = ['Al2O3.txt', 'ITO.txt', 'MgF2.txt', 'etalon-SiO2.txt', 'TiO2.txt', 'air.txt']      # material names
materials = [mats[5], mats[3], mats[1],mats[3], mats[1], mats[3]]
thickness = [69, 94, 27, 10]
limit = structure.Limitations(material=mats, constriant={'minWave': 350,
                                  'maxWave': 800,
                                  'waveStep': 2,
                                  'angle':[0, 30],
                                  'target':560
                                  })


strc = structure.Struct([materials, thickness], limit)
p = plotting.quickplot(strc.R,  strc.waves,  strc.angles)

