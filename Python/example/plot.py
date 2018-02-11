import numpy as np
from src import structure, optimize, plotting, meritFunction

# Quick Plot 
thickness = [218.79999999999981, 111.40000000000005, 118.2, 58.349999999999987, 161.29999999999984, 79.690000000000012, 99.600000000000009, 50.000000000000007, 225.90000000000001, 113.0, 174.5, 87.690000000000012, 128.79999999999998, 64.239999999999995, 131.09999999999999, 65.579999999999998, 155.59999999999999, 77.840000000000003, 133.0, 66.940000000000012, 185.29999999999998, 92.870000000000005, 124.7, 62.600000000000009, 157.59999999999997, 79.030000000000001, 115.3, 57.689999999999998, 138.80000000000001, 69.439999999999998, 149.69999999999999, 75.300000000000011, 204.19999999999996, 102.30000000000001, 116.50000000000001, 57.799999999999997, 127.0, 63.549999999999997, 157.09999999999997, 78.400000000000006, 171.59999999999999, 85.829999999999998, 160.19999999999999, 80.109999999999999, 139.89999999999998, 71.370000000000019, 104.10000000000002, 53.08000000000002, 184.39999999999992, 93.050000000000026]



print(len(thickness))
# limit = structure.Limitations(material=['YAG.txt', 'SiO2.txt', 'Ta2O5.txt', 'Al2O3.txt', 'MgF2.txt', '19.txt'], constriant={'minWave': 430,
#                                   'maxWave': 650,
#                                   'waveStep': 1,
#                                   'angle':range(90),
#                                   'target':560
#                                   }, defaultStructure=['Al2O3.txt'] + ['Ta2O5.txt', 'SiO2.txt']*15 + ['Ta2O5.txt', 'MgF2.txt']*14 +["19.txt"]+ ["YAG.txt"],
#                               meritFunction=meritFunction.meritFunction3, padding=True)
limit = structure.Limitations(material=['air.txt', 'Si.txt', 'Al2O3.txt', 'InP.txt'], constriant={'minWave': 1300,
                                  'maxWave': 1340,
                                  'waveStep': 1,
                                  'angle':[0],
                                  'target':1290
                                  }, defaultStructure=['air.txt'] + ['Al2O3.txt', 'Si.txt']*25 + ["InP.txt"],
                              meritFunction=meritFunction.meritFunction4, padding=False)
# struct = structure.PlotStruct(limit, thickness, phase=False)
# print(struct.MV)
# plotting.surfaceplot(struct.R, RP=struct.RP, RS=struct.RS, waves=struct.waves, angles=struct.angle)
structure = structure.QuickStruct(limit, thickness, phase=False)
plotting.quickplot(structure.R, structure.waves, structure.angle)