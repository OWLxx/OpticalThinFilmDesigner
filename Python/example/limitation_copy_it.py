import numpy as np
from src import structure, optimize, plotting, meritFunction


limit = structure.Limitations(material=['Al2O3.txt', 'SiO2.txt', 'YAG.txt', 'Ta2O5.txt'], constriant={'minWave': 430,
                                  'maxWave': 650,
                                  'waveStep': 10,
                                  'angle':[0, 15, 35, 45, 55, 63],
                                  'target':540
                                  }, defaultStructure=['Al2O3.txt'] + ['Ta2O5.txt', 'SiO2.txt']*30 + ["YAG.txt"], meritFunction=meritFunction.meritFunction2)




limit = structure.Limitations(material=['YAG.txt', 'SiO2.txt', 'Ta2O5.txt', 'Al2O3.txt', 'MgF2.txt', '19.txt'], constriant={'minWave': 430,
                                  'maxWave': 650,
                                  'waveStep': 10,
                                  'angle':[0, 15, 35, 45, 55],
                                  'target':560
                                  }, defaultStructure=['Al2O3.txt'] + ['Ta2O5.txt', 'SiO2.txt']*15 + ['Ta2O5.txt', 'MgF2.txt']*14 +["19.txt"]+ ["YAG.txt"],
                              meritFunction=meritFunction.meritFunction1, padding=True)

# this is the coating designing for DFB lasers
limit = structure.Limitations(material=['Si.txt', 'Al2O3.txt', 'air.txt', 'InP.txt'], constriant={'minWave': 1330,
                                  'maxWave': 1335,
                                  'waveStep': 1,
                                  'angle':[0],
                                  'target':1300
                                  }, defaultStructure=['air.txt'] + ['Al2O3.txt', 'Si.txt']*25 + ["InP.txt"],
                              meritFunction=meritFunction.meritFunction4, padding=False)