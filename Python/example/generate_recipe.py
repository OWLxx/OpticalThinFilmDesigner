import numpy as np
from src import structure, optimize, plotting, meritFunction

# You should set constraints in the following limit function

limit = structure.Limitations(material=['Si.txt','Al2O3.txt',   'InP.txt'], constriant={'minWave': 1300,
                                  'maxWave': 1340,
                                  'waveStep': 1,
                                  'angle':[0],
                                  'target':1270
                                  }, defaultStructure=['InP.txt'] + ['Al2O3.txt', 'Si.txt']*5 + ["InP.txt"],
                              meritFunction=meritFunction.meritFunction4, padding=False)

test = optimize.geneticAlgorithm(limit, '2matlaser')


