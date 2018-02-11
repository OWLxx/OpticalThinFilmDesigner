import os
import numpy as np
from src import structure
from src import optimize, plotting

cur_path = os.path.dirname(__file__)
filepath = os.path.relpath('..\\testdata\\fitting_5layer.txt')
f = open(filepath)
measurement = [[], [], [], []]
for data in f.readlines():
    if data[0].isdigit():
        waves, deg0, deg30, deg60 = [float(i) for i in data.split()]
        measurement[0].append(waves)
        measurement[1].append(deg0/100)
        measurement[2].append(deg30/100)
        measurement[3].append(deg60/100)

a = [['air.txt','AlSiO2.txt', 'ITOa.txt', 'AlSiO2.txt', 'ITOa.txt', 'AlSiO2.txt', 'Willow.txt','AlSiO2.txt', 'ITOa.txt','AlSiO2.txt', 'ITOa.txt','AlSiO2.txt', 'air.txt'],
                         [69, 94, 27, 10, 138, 1000000, 138, 10, 27, 94, 69]]
limit = structure.Limitations(material=None, constriant={'minWave': 350,
                                  'maxWave': 800,
                                  'waveStep': 2,
                                  'angle':[0, 30],
                                  'target':560
                                  })
init = structure.Struct(a, limit)
measurement = np.array(measurement).T
init.waves = measurement[:, 0]
init.constraint['angle'] = [0, 30]
init.angles = [0, 30]
init.initialize()


print(measurement)
# methods 'lm', 'trf', 'dogbox'
# optimized_structure = optimize.curveFitting_lmfit(measurement[:, 1:3], init, [40, 60, 10, 5, 90, 0, 90, 5, 10, 60, 40], [140, 150, 50, 30, 170, 0, 170, 30, 50, 150, 140], method = 'slsqp')

# [87.4, 106.9, 27.7, 7, 134]    [82.6, 86.6, 10, 5, 100], [72.2, 133, 10, 9.558, 98.7], [77.980172748029844, 91.730417896851904, 1.6653345369377348e-14, 6.6764868228883723, 90.0]
# [65.799390870376897, 85.664902673085152, 3.6315132734277e-06, 2.601215795782255, 148.34445620994182]
# [69.475326824564348, 127.08839802097336, 26.917744602779937, 29.999999255106239, 96.819039184923724]
optimized_structure = [83.239417193557614, 109.14329714154911, 31.509048596995285, 11.496578942655471, 118.91354209239651, 1000000, 124.9487917837659, 10.269635368476909, 30.968196128460669, 115.70927235471542, 69.0]
optstruct = structure.Struct([['air.txt','AlSiO2.txt', 'ITOa.txt', 'AlSiO2.txt', 'ITOa.txt', 'AlSiO2.txt', 'Willow.txt','AlSiO2.txt', 'ITOa.txt','AlSiO2.txt', 'ITOa.txt','AlSiO2.txt', 'air.txt'],
                              optimized_structure], limit)

optstruct.initialize()
plotting.quickplot(measurement[:, 1:4], optstruct.waves, [0, 30, 60])

plotting.compare3(measurement[:, 1:3], init.R, optstruct.R, optstruct.waves, [0, 30])

