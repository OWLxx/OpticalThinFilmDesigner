import re
import numpy as np
import pandas as pd


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
            para2 include minWave, maxWave, waveStep, angle, coherent, method
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
                self.result = transferMatrixCoherent.coherent_calc(para1, mat, para2)
                self.result.main()
            else:
                self.result = transferMatrixIncoherent.incoherent_calc(para1, mat, para2)
                self.result.main()
        if functionality == 'fitting':
            if para2['method'] == 'LS':
                def helper(X, Y):
                    # X is wavelength
                    # Y is thickness, which need to be fit
                    if para2['coherent']:
                        pass


    def readFile(self, filename, constrains):
         filepath = "./indexfile/" + filename
         f = open(filepath, 'r')
         dataInFile = {}
         for line in f.readlines():
             if re.match('[0-9.]{3,8}\t[0-9.]{1,15}\t[.-z]{1,8}', line) is not None:
                 curWave, curn, curk = line.split('\t')
                 dataInFile[int(curWave)] = [float(curn), float(curk)]
             elif re.match('[0-9.]{3,8}\t[0-9.]{1,15}', line) is not None:        # no k values in the index file
                 curWave, curn, curk = line.split('\t')
                 dataInFile[int(curWave)] = [float(curn), 0]
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
                 output.append(complex(*dataInFile[targetWave[i]]))
             else:
                 ratio = (targetWave[i] - preWave) / (fileWave[count] - preWave)  # pickup linear point
                 ntemp = (1-ratio)*preN[0] + ratio*dataInFile[fileWave[count]][0]
                 ktemp = (1-ratio)*preN[1] + ratio*dataInFile[fileWave[count]][1]
                 output.append(complex(ntemp, ktemp))
         return output


