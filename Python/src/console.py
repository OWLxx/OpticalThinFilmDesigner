import re
import numpy as np
import pandas as pd
import lmfit
from matplotlib import pyplot as plt


class preProcessing(object):
    def __init__(self, functionality, para1=None, para2=None, para3=None):
        '''
        determine the functionality of running
        functionality in ['calculating', 'fitting', 'designing', 'localMinimizing' ]
        if functionality == 'calculating':
            para1 = structure
            para1 = [['incident', 'material1', 'material2', ..., 'materialN', 'emergent'], [thickness1, ...,
             thicknessN]]
            para2 = limitations in python dictionary format
            eg:{'minWave':400, 'maxWave':700, 'waveStep':1, 'angle':[0,30,60], 'coherent':True, 'save2SQLite': False}
            note: length in nanometer, angle in deg, if more than 10 angle is revolved, output would be surface plot
            para3 = merit function (cost function)
                    merit function: input: reflectance, wavelength, angle,  output merit value, the LOWER, the BETTER
        elif functionality == 'fitting':
            para1 = expected structure
            para1 = [['incident', 'material1', 'material2', ..., 'materialN', 'emergent'], [thickness1, ...,
             thicknessN]]
            eg:   [['air.txt', 'SiO2.txt', 'TiO2.txt', 'air.txt'], [56, 92]]
            para2 include minWave, maxWave, waveStep, angle, coherent, method, boundLow, boundHigh, type
            para3 = measured REFLECTANCE
            eg: [[400, 450, 500, 550, 600], [0.034, 0.025, 0.046, 0.033]]
        elif functionality == 'designing':
            currently the designing is based on Bragg pair constrainted genetic algorithm
        elif functionality == 'localMinimizing'
            currently the local optimization is based LDS
        '''
        if functionality == 'calculating':
            mat = {}         # index data
            materials = set(para1[0])
            for m in materials:
                mat[m] = self.readFile(m, para2)
            if para2['coherent']:
                self.result = tf_coherent.coherent_calc(para1, mat, para2)
            else:
                self.result = tf_incoherent.incoherent_calc(para1, mat, para2)
        if functionality == 'fitting':
            mat = {}         # index data
            materials = set(para1[0])
            for m in materials:
                mat[m] = self.readFile(m, para2)
            params = lmfit.Parameters()
            for i, tck in enumerate(para1[1]):
                if tck < 100000:
                    params.add('layer{}'.format(i), value=tck, vary=True, min=para2['boundLow'][i], max=para2['boundHigh'][i])
                else:
                    params.add('layer{}'.format(i), value=tck, vary=False)

            def residual(params, x=None, y=None):
                # x is wavelength, ydata is measurement
                thickness = []
                for i in range(len(para1[1])):
                    thickness.append(params['layer{}'.format(i)])
                pa1 = [para1[0], thickness]
                pa2 = {'angle':para2['angle'], 'minWave':x[0], 'maxWave':x[-1], 'waveStep':x[1]-x[0]}
                cur = tf_incoherent.incoherent_calc(pa1, mat, pa2)
                if para2['type'] == 'R':
                    cal = list(cur.R[para2['angle'][0]])
                else:
                    cal = list(cur.R[para2['angle'][0]])
                mv = sum([np.abs(cal[i]-y[i]) for i in range(len(x))])
                print(mv)
                return mv

            out = lmfit.minimize(residual, params, method=para2['method'], kws = {'x':para3[0], 'y':para3[1]})
            print(lmfit.fit_report(out))

    def readFile(self, filename, constrains):
         filepath = "./indexfile/" + filename
         f = open(filepath, 'r')
         dataInFile = {}
         for line in f.readlines():
             if re.match('[0-9.]{3,8}\t[0-9.]{1,15}\t[.-z]{1,8}', line) is not None:
                 curWave, curn, curk = line.split('\t')
                 dataInFile[float(curWave)] = [float(curn), float(curk)]
             elif re.match('[0-9.]{3,8}\t[0-9.]{1,15}', line) is not None:        # no k values in the index file
                 curWave, curn, curk = line.split('\t')
                 dataInFile[float(curWave)] = [float(curn), 0]
         targetWave = range(constrains['minWave'], constrains['maxWave']+constrains['waveStep'], constrains['waveStep'])
         fileWave = sorted(dataInFile.keys())
         output = []
         count = 0                                                                # count waves in fileWave
         preN = dataInFile[fileWave[count]]
         preWave = fileWave[count]
         for i in range(len(targetWave)):
             while targetWave[i]>fileWave[count]:
                 preN = dataInFile[fileWave[count]]
                 preWave = fileWave[count]
                 count += 1
             if targetWave[i]==fileWave[count]:
                 if np.absolute(dataInFile[targetWave[i][1]]) < 0.01:
                     dataInFile[targetWave[i][1]] = 0
                 output.append(complex(*dataInFile[targetWave[i]]))
             else:
                 ratio = (targetWave[i] - preWave) / (fileWave[count] - preWave)  # pickup linear point
                 ntemp = (1-ratio)*preN[0] + ratio*dataInFile[fileWave[count]][0]
                 ktemp = (1-ratio)*preN[1] + ratio*dataInFile[fileWave[count]][1]
                 if np.absolute(ktemp)<0.01:
                     ktemp = 0
                 output.append(complex(ntemp, ktemp))
         return output

    def cmpplt(self, x, y1, y2):
        plt.figure(1)
        a1, = plt.plot(x, y1, label='y1')
        a2, = plt.plot(x, y2, label='y2')
        lgd = [a1, a2]
        plt.legend(handles=lgd)
        plt.xlabel('Wavelength (nm)')
        plt.grid(True)
        plt.show()



