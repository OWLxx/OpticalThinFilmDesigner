'''
OSRAM Edition, 50~60 layer bandpass filter design, 3 material design
RD = 0.9049
TP = 0.9851
MV = 0.725
'''
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import cmath
import time
import sys
import re
import csv
import random
import operator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter


class inputArg(object):
    def __init__(self, incidentLight='average'):
        self.minWave = 400
        self.waveStep = 10
        self.maxWave = 700
        self.minPassband = 430
        self.maxPassband = 470
        self.minStopband = 490
        self.maxStopband = 650
        self.centralWave = (self.minStopband + self.maxStopband) / 2
        self.incidentMaterial = 'Al2O3.txt'
        self.emergentMaterial = 'YAG.txt'
        '''
        Materials: air.txt, Al2O3.txt, YAG.txt, MgF2.txt, Ta2O5.txt, SiO2.txt, ITO.txt, TiO2.txt
        '''
        self.material1 = 'MgF2.txt'
        self.material2 = 'Ta2O5.txt'
        self.material3 = 'SiO2.txt'
        self.material4 = 'ITO.txt'
        self.incident = 'Al2O3.txt'
        self.emergent = 'YAG.txt'
        self.layerNumber = 10
        self.materialNumber = 3
        self.angle = [0, 15 , 32, 40, 48, 60]
        self.fixedLayerIndex = 1.95
        self.fixedLayerThickness = 0
        self.incidentLight = incidentLight
        index_file, wav_in = indexfile_format(self.materialNumber, self.minWave, self.waveStep, self.maxWave,
                                              self.incident, self.emergent, self.material1, self.material2,
                                              self.material3, self.material4, self.fixedLayerIndex)
        self.indexFile = index_file
        # print index_file
        self.n1 = index_file.loc[self.centralWave]['material1']
        self.n2 = index_file.loc[self.centralWave]['material2']
        if self.materialNumber >= 3: self.n3 = index_file.loc[self.centralWave]['material3']
        if self.materialNumber >= 4: self.n4 = index_file.loc[self.centralWave]['material4']
        self.uncoatedStructure = [['incident', 'fixed_layer', 'emergent'], [1000]]
        self.compStructure_twoMaterial = [
            ['incident', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'emergent'],
            [128.6, 82.8, 107.4, 69.1, 109.8, 70.7, 109.4, 70.4, 123.2, 79.3, 122.5, 78.8, 120.2, 77.4, 110.7, 71.3,
             108, 69.5, 103.5, 66.6, 106.7, 68.7, 119.6, 77, 127.7, 82.3, 112.4, 72.3, 120.1, 77.3, 122.5, 78.8, 109.4,
             70.4, 107.2, 69, 107.2, 69, 104.8, 67.5, 109.2, 70.3, 108.8, 70.1, 118.3, 76.2, 127.3, 81.9, 131.3, 84.5]]
        self.spolarized_twoMaterial = [
            ['incident', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
             'material2', 'material1', 'material2', 'emergent'],
            [128.6, 82.8, 107.20000000000002, 68.9, 113.49999999999979, 74.39999999999979, 116.29999999999961,
             77.29999999999961, 125.19999999999989, 81.29999999999988, 133.0999999999994, 89.3999999999994,
             123.49999999999982, 80.69999999999982, 110.8, 71.39999999999999, 108.79999999999995, 70.29999999999995,
             105.79999999999987, 68.89999999999986, 107.09999999999998, 69.09999999999998, 120.39999999999995,
             77.79999999999995, 128.2, 82.79999999999997, 114.1999999999999, 74.0999999999999, 120.29999999999998,
             77.49999999999999, 123.19999999999996, 79.49999999999996, 111.89999999999986, 72.89999999999986,
             107.39999999999999, 69.19999999999999, 107.39999999999999, 69.19999999999999, 104.99999999999999,
             67.69999999999999, 109.39999999999999, 70.49999999999999, 108.99999999999999, 70.29999999999998,
             118.49999999999999, 76.39999999999999, 127.49999999999999, 82.1, 131.5, 84.69999999999999]]

    # genNo=2, timeLimit=None,layerNo=10, incident=None, emergent=None, material1=None, material2=None, material3=None, material4=None
    def recipeGenerator_geneticAlgorithm(self, genNo=2, timeLimit=None, layerNo=10, incident=None, emergent=None,
                                         material1=None, material2=None, material3=None, material4=None):
        # time limit in seconds
        # initialize
        if not incident: incident = self.incidentMaterial
        if not emergent: emergent = self.emergentMaterial
        if not material1: material1 = self.material1
        if not material2: material2 = self.material2
        if not material3: material3 = self.material3
        if not material4: material4 = self.material4
        if not genNo: genNo = 2
        if timeLimit: genNo = 0
        if not layerNo: layerNo = self.layerNumber
        angle = self.angle
        centralWave = (self.minStopband + self.maxStopband) / 2
        incidentLightType = self.incidentLight
        if self.materialNumber == 2:
            tag = '_'.join(str(x) for x in
                           [layerNo, incident, emergent, material1, material2, self.minPassband, self.maxPassband,
                            self.minStopband, self.maxStopband])
        elif self.materialNumber == 3:
            tag = '_'.join(str(x) for x in
                           [layerNo, incident, emergent, material1, material2, material3, self.minPassband,
                            self.maxPassband, self.minStopband, self.maxStopband])
        elif self.materialNumber == 4:
            tag = '_'.join(str(x) for x in
                           [layerNo, incident, emergent, material1, material2, material3, material4, self.minPassband,
                            self.maxPassband, self.minStopband, self.maxStopband])

        index_file, wav_in = indexfile_format(self.materialNumber, self.minWave, self.waveStep, self.maxWave, incident,
                                              emergent, material1, material2, material3, material4,
                                              self.fixedLayerIndex)
        # genetic algorithm
        ga = Genetic_algorithm_for_thin_film_filter(self.materialNumber, genNo, index_file, layerNo, angle,
                                                    centralWave, tag, incidentLightType, timeLimit)
        best_overall, best_in_gen = ga.genetic_algorithm_main()
        print 'Returned structure:{}'.format(best_overall)
        structure_in_thickness = best_overall[2]

        rta = Transfer_matrix_method(index_file, self.uncoatedStructure, self.angle,
                                     incidentLightType='average')
        meritValue_uncoated, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, self.compStructure_twoMaterial,  self.angle,
                                     incidentLightType='average')
        meritValue_ref, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, self.uncoatedStructure,  self.angle,
                                     incidentLightType='average')
        meritValue_uncoated, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, best_overall[2],  self.angle, incidentLightType='average')
        meritValue_sample, _, RR, TT, AA, RRS, RRP, TTS, TTP = rta.transfer_matrix_main()
        print 'Merit value of current:{}, uncoated:{}, reference:{}'.format(meritValue_sample, meritValue_uncoated,
                                                                            meritValue_ref)
        print '#######################################################################################################'
        '''
        save to sql
        '''

        conn = psycopg2.connect("dbname=optical_filter user=postgres password=nibaxing")
        cur = conn.cursor()
        # cur.execute("INSERT INTO twomatframe (sampleid, material1, material2, meritvalue, substrate, emergent, lt1, lt2, lt3, lt4, lt5, lt6, lt7, lt8, lt9, lt10) \
        #               VALUES (%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)",(np.random.randint(100000),material1, material2, meritValue_sample, incident, emergent, \
        #                                                                              best_overall[2][1][0], best_overall[2][1][1], best_overall[2][1][2], \
        #                                                                              best_overall[2][1][3], best_overall[2][1][4], best_overall[2][1][5], \
        #                                                                              best_overall[2][1][6], best_overall[2][1][7], best_overall[2][1][8], \
        #                                                                              best_overall[2][1][9]))
        cur.execute("INSERT INTO twomatframe (sampleid, material1, material2, meritvalue, substrate, emergent, lt1, lt2, lt3, lt4, lt5, lt6, lt7, lt8, lt9, lt10,lt11, lt12, lt13, lt14, lt15, lt16, lt17, lt18, lt19, lt20,lt21, lt22, lt23, lt24) \
                      VALUES (%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",(np.random.randint(100000),material1, material2, meritValue_sample, incident, emergent, \
                                                                                     best_overall[2][1][0], best_overall[2][1][1], best_overall[2][1][2], \
                                                                                     best_overall[2][1][3], best_overall[2][1][4], best_overall[2][1][5], \
                                                                                     best_overall[2][1][6], best_overall[2][1][7], best_overall[2][1][8], \
                                                                                     best_overall[2][1][9],best_overall[2][1][10], best_overall[2][1][11], best_overall[2][1][12], \
                                                                                     best_overall[2][1][13], best_overall[2][1][14], best_overall[2][1][15], \
                                                                                     best_overall[2][1][16], best_overall[2][1][17], best_overall[2][1][18], \
                                                                                     best_overall[2][1][19],best_overall[2][1][20], best_overall[2][1][21], best_overall[2][1][22], \
                                                                                     best_overall[2][1][23]))

        conn.commit()
        cur.close()
        conn.close()

        # self.resultPlot(RR + RRS + RRP, TT + TTS + TTP, flag=1, key=2, meritValueinGeneration=best_in_gen)

    def plotStructure(self, structure, angle=None, minWave=None, maxWave=None, waveStep=None, flag=0, incident=None,
                      emergent=None, material1=None, material2=None, material3=None, material4=None):
        # :param flag:  flag=0 without transmission, flag=1 with transmission
        if not incident: incident = self.incidentMaterial
        if not emergent: emergent = self.emergentMaterial
        if not material1: material1 = self.material1
        if not material2: material2 = self.material2
        if not material3: material3 = self.material3
        if not material4: material4 = self.material4
        if not angle: angle = self.angle
        if not minWave: minWave = self.minWave
        if not maxWave: maxWave = self.maxWave
        if not waveStep:
            waveStep = self.waveStep
        else:
            self.waveStep = waveStep

        print angle

        index_file, wav_in = indexfile_format(self.materialNumber, minWave, waveStep, maxWave, incident, emergent,
                                              material1, material2, material3, material4, self.fixedLayerIndex)

        self.indexFile = index_file

        # limitations = self.layerNumber
        rta = Transfer_matrix_method(index_file, structure, angle, incidentLightType='average')
        meritValue_sample, structure, RR, TT, AA, RRS, RRP, TTS, TTP = rta.transfer_matrix_main()
        print meritValue_sample
        print RR
        print len(RR[0]), len(RRS[0]), len(RRP[0]), len(TT), len(TTS), len(TTP)
        self.resultPlot(RR + RRS + RRP, TT + TTS + TTP, flag=1,waveStep=waveStep, angles=angle)

    def localMinimum(self, material1=None, material2=None, structure=None, stop=1):
        # input structure with material and thickness
        # local minimum based on old_structure
        if structure is None:
            structure = self.spolarized_twoMaterial
        if material1:
            indexFile, wav_in = indexfile_format(self.materialNumber, self.minWave, self.waveStep, self.maxWave,
                                              self.incident, self.emergent, material1, material2,
                                              self.material3, self.material4, self.fixedLayerIndex)
        else:
            indexFile = self.indexFile

        # calculate merit value
        incidentLightType = 'average'
        rta = Transfer_matrix_method(indexFile, structure, self.angle, incidentLightType)
        meritValue_original, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        mvCur = meritValue_original
        print 'Original merit value is {} '.format(mvCur)

        variation = structure[1]
        mirror = [[k for k in j] for j in structure]  # back up structure
        # up = [[k for k in j] for j in mirror]
        # down = [[k for k in j] for j in mirror]
        # left = [[k for k in j] for j in mirror]
        # right = [[k for k in j] for j in mirror]
        # delta = 0.1
        # iter = 0
        # mv_iter = meritValue_original
        # mvcur = 0
        # while mvcur - mv_iter < -0.002:
        #     if iter is not 0: mv_iter = mvcur
        #     for i in range(len(variation) - 1):
        #         vector = [0, 0]  # direction of optimization
        #         rta = Transfer_matrix_method(indexFile, mirror, self.weighting, self.angle,
        #                                      incidentLightType='average')
        #         mvmirror, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         up[1][i] = up[1][i] + delta
        #         rta = Transfer_matrix_method(indexFile, up[:], self.weighting, self.angle,
        #                                      incidentLightType='average')
        #         mvup, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         down[1][i] -= delta
        #         down = down[:]
        #         rta = Transfer_matrix_method(indexFile, down[:], self.weighting, self.angle,
        #                                      incidentLightType='average')
        #         mvdown, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         left[1][i + 1] += delta
        #         left = left[:]
        #         rta = Transfer_matrix_method(indexFile, left[:], self.weighting, self.angle,
        #                                      incidentLightType='average')
        #         mvleft, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         right[1][i + 1] -= delta
        #         right = right[:]
        #         rta = Transfer_matrix_method(indexFile, right[:], self.weighting, self.angle,
        #                                      incidentLightType='average')
        #         mvright, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         print 'mvmirror is ', mvmirror
        #         print mvup, mvdown, mvleft, mvright, '################'
        #         if mvup < mvdown and mvup < mvmirror:
        #             vector[0] = mvmirror - mvup
        #         elif mvdown < mvup and mvdown < mvmirror:
        #             vector[0] = mvdown - mvmirror
        #         if mvright < mvleft and mvright < mvmirror:
        #             vector[1] = mvmirror - mvright
        #         elif mvleft < mvright and mvleft < mvmirror:
        #             vector[1] = mvleft - mvmirror
        #         factor = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
        #         print 'layer {}, factor {}'.format(i, factor)
        #         if factor == 0:
        #             mvcur = mvmirror
        #             continue
        #         vector = [k / factor for k in vector]
        #         print i, '#####'
        #         mirror[1][i], mirror[1][i + 1] = mirror[1][i] + vector[0] * delta, mirror[1][i + 1] + vector[1] * delta
        #         rta = Transfer_matrix_method(indexFile, mirror, self.weighting, self.angle,
        #                                      incidentLightType='average')
        #         mvcur, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         mvpre = mvcur + 0.001
        #         while abs(mvcur - mvpre) < 0.01:  # Newton's method
        #             delta = delta - mvcur / (mvcur - mvpre)
        #             mvpre = mvcur
        #             mirror[1][i], mirror[1][i + 1] = mirror[1][i] + vector[0] * delta, mirror[1][i + 1] + vector[
        #                 1] * delta
        #             rta = Transfer_matrix_method(indexFile, mirror, self.weighting, self.angle,
        #                                          incidentLightType='average')
        #             mvcur, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        #         print '{}th layer, mv is {}'.format(i, mvcur)
        #     iter += 1
        #     print '{}th iternation, mv is {}, structure is {}'.format(iter, mvcur, mirror)
        # print 'The final mirror is', mirror
        ####################################
        delta = 0.1
        iter = 0
        mv = 0
        mv_iter = meritValue_original
        while True:
            print mirror
            if mv!=0: mv_iter = mv
            for i in range(0,len(variation)-1):
                mirror[1][i] += delta
                mirror[1][i+1] += delta
                # print mirror
                rta = Transfer_matrix_method(indexFile, mirror,  self.angle, incidentLightType)
                mv, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
                if mv < meritValue_original:
                    delta = 0.1
                else:
                    delta = -0.1
                    mv = meritValue_original - 0.01
                    mirror = structure
                while mv < mvCur:
                    mvCur = mv
                    mirror[1][i] += delta
                    mirror[1][i+1] += delta
                    rta = Transfer_matrix_method(indexFile, mirror,  self.angle, incidentLightType)
                    mv, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
                mirror[1][i] -= delta
                mirror[1][i+1] -= delta
                print '{}th layer, mv is {}, mirror is {}'.format(i, mv, mirror)
            iter += 2
            print '{}th iternation, mv is {}'.format(iter, mv)
            print mv, mv_iter
            if mv >= mv_iter: break
        print mirror
        # file = open('localMin.txt', 'a')
        # file.write(str(mirror))
        # file.close()
        conn = psycopg2.connect("dbname=optical_filter user=postgres password=nibaxing")
        cur = conn.cursor()
        # cur.execute("INSERT INTO twomatframe (sampleid, material1, material2, meritvalue, substrate, emergent, lt1, lt2, lt3, lt4, lt5, lt6, lt7, lt8, lt9, lt10) \
        #               VALUES (%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)",(np.random.randint(100000),material1, material2, meritValue_sample, incident, emergent, \
        #                                                                              best_overall[2][1][0], best_overall[2][1][1], best_overall[2][1][2], \
        #                                                                              best_overall[2][1][3], best_overall[2][1][4], best_overall[2][1][5], \
        #                                                                              best_overall[2][1][6], best_overall[2][1][7], best_overall[2][1][8], \
        #                                                                              best_overall[2][1][9])6
        cur.execute("INSERT INTO optimizedstructure1 (meritvalue, material1, material2, lt1, lt2, lt3, lt4, lt5, lt6, lt7, lt8, lt9, lt10,lt11, lt12, lt13, lt14, lt15, lt16, lt17, lt18, lt19, lt20,lt21, lt22, lt23, lt24) \
                      VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)",(mv,material1, material2, mirror[1][0], mirror[1][1], mirror[1][2], mirror[1][3], mirror[1][4], mirror[1][5], mirror[1][6], mirror[1][7], \
                            mirror[1][8], mirror[1][9], mirror[1][10], mirror[1][11], mirror[1][12], mirror[1][13], mirror[1][14], mirror[1][15], mirror[1][16], mirror[1][17], mirror[1][18], mirror[1][19], mirror[1][20], mirror[1][21], mirror[1][22], mirror[1][23]))
        conn.commit()
        cur.close()
        conn.close()

    def localMininum2(self, structure, step):
        rta = Transfer_matrix_method(self.indexFile, structure,  self.angle, 'average')
        mv, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
        thickness = structure[1]
        for i in range(0, len(thickness), 2):
            ratio = thickness[i+1]/thickness[i]
            curthick = thickness[:]
            cur_mv = []
            for var in np.arange(-10, 11):
                curthick[i] = thickness[i] + var*step
                curthick[i+1] = thickness[i+1] + ratio*var*step
                curstruct = [structure[0], curthick]
                print curstruct
                rta = Transfer_matrix_method(self.indexFile, curstruct,  self.angle, 'average')
                mv, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
                cur_mv.append(mv)
            mvindex = min([(i,j) for i,j in enumerate(cur_mv)], key = lambda x:x[1])[0]
            print cur_mv[mvindex], i, 'i'
            thickness[i] = thickness[i] + (mvindex-10)*step
            thickness[i] = thickness[i] + (mvindex-10)*step*ratio
        print [structure[0] + thickness]


    def discrepancy_optimize(self, structure):
        '''
        temp use at 7.16
        pick 2 among 24 = 552
        pick 2 among 12 = 132
        pick 2 among 50 = 2450   * avg 20 iteration * avg 10 updates * avg 2s = 272 h
        '''
        def pairOptimize(ti1, ti2, structure):
            materials = structure[0]
            thickness = structure[1]
            curstructure = [materials, thickness]
            rta = Transfer_matrix_method(self.indexFile, curstructure,  self.angle, 'average')
            mv_curmax, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
            print 'Inputed material\'s index is {}'.format(mv_curmax)
            mv_pre = 1 # initialize
            overall_iter = 0
            while (overall_iter==0 or mv_pre > mv_curmax) and overall_iter<=20:
                print 'last merit value is {}, overall iteration is {}, current mv is {}'.format(mv_pre, overall_iter, mv_curmax)
                print 'current structure is {}'.format([materials, thickness])
                mv_pre = mv_curmax
                inner_iter = 0
                mv_pre_inner = 1  # initialize
                while (inner_iter==0 or mv_pre_inner > mv_curmax) and inner_iter<=50:
                    mv_pre_inner = mv_curmax
                    for thickindex in [ti1, ti2]:
                        # determine directions
                        thickness_temp = thickness[:]
                        thickness_temp[thickindex] += 0.1
                        curstructure = [materials, thickness_temp]
                        rta = Transfer_matrix_method(self.indexFile, curstructure,  self.angle, 'average')
                        mv_positive, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
                        thickness_temp[thickindex] -= 0.2
                        curstructure = [materials, thickness_temp]
                        rta = Transfer_matrix_method(self.indexFile, curstructure,  self.angle, 'average')
                        mv_negative, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
                        thickness_temp[thickindex] += 0.1
                        # optimize
                        if mv_positive >= mv_pre_inner and mv_negative >= mv_pre_inner:
                            continue  # early stop
                        else:
                            sign = (-1, 1)[mv_positive<mv_negative]
                            initial_step = step = 0.1
                            mv_pre_singlelayer = 1
                            temp_count = 0
                            while mv_curmax < mv_pre_singlelayer or step > initial_step:  # only end with the smallest increasement
                                if mv_curmax == mv_pre_singlelayer or temp_count==0:
                                    step = initial_step
                                else:
                                    step = step*2     # exponentially growth
                                mv_pre_singlelayer = mv_curmax  # record mv of last optimization

                                thickness_temp = thickness[:]
                                thickness_temp[thickindex] += sign * step

                                curstructure = [materials, thickness_temp]
                                rta = Transfer_matrix_method(self.indexFile, curstructure,  self.angle, 'average')
                                mv_current, _,_,_,_,_,_,_,_ = rta.transfer_matrix_main()
                                if mv_current < mv_curmax:  # if mv is better, update thickness and mv_curmax
                                    mv_curmax = mv_current
                                    thickness = thickness_temp[:]
                                    print 'thickness updated, {}, the inside count{}, current mv is {}'.format(thickness, temp_count, mv_curmax)
                                # else, nothing happends, last time. In next iteration, step would become initial_step.
                                # if still nothing happends, this iteration would end
                                temp_count += 1
                    inner_iter += 1
                overall_iter += 1
            structure = [materials, thickness]
            return thickness[ti1], thickness[ti2]
        thickness = structure[1]
        for ti1 in range(0,len(thickness),2):
            for ti2 in range(1,len(thickness),2):
                if ti1 != ti2:
                    print('#######', ti1, ti2, structure)
                    t1, t2 = pairOptimize(ti1, ti2, structure)
                    thickness[ti1], thickness[ti2] = t1, t2
                    structure[1] = thickness[:]
                    print '!!!', structure
        # conn = psycopg2.connect("dbname=optical_filter user=postgres password=nibaxing")
        # cur = conn.cursor()
        # cur.execute('''DROP TABLE IF EXISTS twodLDS ''')
        # cur.execute('''CREATE TABLE twodLDS ( id SERIAL, mat1 char(20), mat2 char(20)) ''')
        # for i in range(len(structure[1])):
        #     cur.execute('''ALTER TABLE twodLDS ADD COLUMN layer{} NUMERIC '''.format(i))
        # cur.execute('''INSERT INTO twodLDS ''')




    def recipeGenerator_pureCoupling_test(self, layer=None):
        def findThickness(padmat, padthic, matIndex):
            if matIndex == 1:
                ntemp = self.n1
            elif matIndex == 2:
                ntemp = self.n2
            elif matIndex == 3:
                ntemp = self.n3
            elif matIndex == 4:
                ntemp = self.n4
            materials = {1: 'material1', 2: 'material2', 3: 'material3', 4: 'material4'}
            curthic = int(np.real(0.25 * self.centralWave / ntemp))
            curmat = ['incident'] + padmat + [materials[matIndex]] + ['fixed_layer', 'emergent']
            mv = []
            for i in range(curthic - 30, curthic + 90):
                curstructure = [curmat, padthic + [i] + [1000]]
                rta = Transfer_matrix_method(self.indexFile, curstructure, self.weighting, self.angle,
                                             incidentLightType='average')
                mvcur, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
                mv.append((mvcur, i))
            return min(mv, key=lambda x: x[0])

        case = self.materialNumber
        materials = {1: 'material1', 2: 'material2', 3: 'material3', 4: 'material4'}
        padmat = []
        padthic = []
        if layer == None: layer = 24
        i = len(padmat)  # counter for layer
        mvs = []
        while i < layer:  # layers
            curbatch = []
            for matIndex in range(1, case + 1):  # materials
                if padmat == [] or materials[matIndex] != padmat[-1]:
                    mvcur, curthick = findThickness(padmat, padthic, matIndex)
                    curbatch.append((matIndex, curthick, mvcur))
                    # print mvcur, materials[matIndex], padmat, '####'
            print 'curbatch', curbatch, i
            (material, thick, mv) = min(curbatch, key=lambda x: x[-1])
            tempstr = 'material' + str(material)
            if i != 0:
                print 'layer', i, 'mvcurrent', mv, padmat, padthic
            padmat.append(tempstr)
            padthic.append(thick)
            mvs.append(mv)
            i += 1
        print 'merit_value', mvs
        print padmat
        print padthic

    def meritvalueCompare(self, structure, material1=None, material2=None):
        if material1:
            index_file, wav_in = indexfile_format(self.materialNumber, self.minWave, self.waveStep, self.maxWave,
                                              self.incident, self.emergent, material1, material2,
                                              self.material3, self.material4, self.fixedLayerIndex)
            self.indexFile = index_file
        else:
            index_file = self.indexFile
        angle = self.angle
        weight = meritFunctions()
        weight1 = weight.meritFunction1()
        weight2 = weight.meritFunction2()
        weight3 = weight.meritFunction4(angle)
        print index_file

        rta = Transfer_matrix_method(index_file, self.compStructure_twoMaterial, weight1, [0, 10, 20],
                                     incidentLightType='average')
        meritValue_ref, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, self.uncoatedStructure, weight1, [0, 10, 20],
                                     incidentLightType='average')
        meritValue_uncoated, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, structure, weight1, [0, 10, 20], incidentLightType='average')
        meritValue_sample, _, RR, TT, AA, RRS, RRP, TTS, TTP = rta.transfer_matrix_main()
        print 'Merit value in merit function 1- current:{}, uncoated:{}, reference:{}'.format(meritValue_sample,
                                                                                              meritValue_uncoated,
                                                                                              meritValue_ref)
        print '#######################################################################################################'
        rta = Transfer_matrix_method(index_file, self.uncoatedStructure, weight2, [0, 10, 20],
                                     incidentLightType='average')
        meritValue_uncoated, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, self.compStructure_twoMaterial, weight2, [0, 10, 20],
                                     incidentLightType='average')
        meritValue_ref, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, structure, weight2, [0, 10, 20], incidentLightType='average')
        meritValue_sample, _, RR, TT, AA, RRS, RRP, TTS, TTP = rta.transfer_matrix_main()
        print 'Merit value in merit function 2- current:{}, uncoated:{}, reference:{}'.format(meritValue_sample,
                                                                                              meritValue_uncoated,
                                                                                              meritValue_ref)
        print '#######################################################################################################'
        rta = Transfer_matrix_method(index_file, self.uncoatedStructure, weight3, self.angle,
                                     incidentLightType='average')
        meritValue_uncoated, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, self.compStructure_twoMaterial, weight3, self.angle,
                                     incidentLightType='average')
        meritValue_ref, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        rta = Transfer_matrix_method(index_file, structure, weight3, self.angle, incidentLightType='average')
        meritValue_sample, _, RR, TT, AA, RRS, RRP, TTS, TTP = rta.transfer_matrix_main()
        print 'Merit value in merit function 3- current:{}, uncoated:{}, reference:{}'.format(meritValue_sample,
                                                                                              meritValue_uncoated,
                                                                                              meritValue_ref)
        print '#######################################################################################################'

    def couple2structure(self):
        print self.indexFile
        structure1 = [['incident', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material3', 'material1', 'material2', 'material1', 'material3', 'material1', 'material3', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'emergent'], [69.732413485318972, 101.47037335685636, 79.49495137326366, 115.6762256268163, 76.240772077282116, 110.94094153682968, 72.52171002473176, 105.52918829113068, 61.829406623649518, 89.970397709746024, 89.970397709746024, 89.970397709746024, 63.688937649924689, 92.676274332595526, 77.793952906923252, 77.793952906923252, 86.58805193118414, 86.58805193118414, 55.785930788255207, 81.176298685485136, 76.240772077282116, 110.94094153682968, 51.137103222567262, 74.411607128361368, 74.846123807575722, 108.91153406969254, 71.12706175502538, 103.49978082399355]]

        # a = inputArg('average')
        # a.meritvalueCompare(structure1, material1='SiO2.txt', material2='Ta2O5.txt')
        # mat11 = 'SiO2.txt'  # should be mat 3
        # mat12 = 'Ta2O5.txt'   # should be mat 2
        # for i,ele in enumerate(structure1[0]):
        #     if ele == 'material2': structure1[0][i] = 'material2'
        #    if ele == 'material1': structure1[0][i] = 'material3'
        structure2 = [['incident', 'material3', 'material1', 'material2', 'material1', 'material3', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material3', 'material1', 'material2', 'material1', 'material3', 'material1', 'emergent'], [79.823360374060385, 85.260115606936424, 77.635420346988511, 120.6647398843931, 96.05862011115741, 102.60115606936417, 85.073544452089195, 132.22543352601159, 66.013351432768658, 102.60115606936417, 68.337765215612635, 106.21387283236997, 71.12706175502538, 110.54913294797689, 58.110344571099169, 90.317919075144516, 70.662178998456596, 109.82658959537574, 66.94311694590624, 104.04624277456648, 58.110344571099169, 90.317919075144516, 88.617459398321259, 94.65317919075143, 75.775889320713318, 117.77456647398844, 89.970397709746024, 96.098265895953759]]


        # mat21 = 'MgF2.txt'
        # mat22 = 'ITO.txt'
        # for i, ele in enumerate(structure2[0]):
        #     if ele == 'material1': structure2[0][i] = 'material1'
        #     if ele == 'material2': structure2[0][i] = 'material4'
        structure1[0].pop()
        structure2[0].pop(0)

        ############################################ Single Padding Layer ##############################################
        mv = []
        materials = ['material1', 'material2', 'material3', 'material4']
        mati = 0
        matj = 2
        thickness1 = 59
        thickness2 = 63
        structure = [structure1[0]+structure2[0], structure1[1]+structure2[1]]
        structure3 = [structure1[0]+[materials[mati]] + [materials[matj]]+structure2[0], structure1[1]+[thickness1]+[thickness2]+structure2[1]]
        print structure1[0]+structure2[0]
        print structure1[0]
        print structure2[0]
        print '###', structure3
        rta = Transfer_matrix_method(self.indexFile, structure3, self.angle, 'average')
        mvc, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
        print 'mvc', mvc, materials[mati], materials[matj], thickness1, thickness2
        for mati in range(0,1):
            for matj in range(2,3):
                if mati != matj:
                    for thickness1 in range(40,60,1):
                        for thickness2 in range(60,80,1):
                            structure3 = [structure1[0]+[materials[mati]] + [materials[matj]]+structure2[0], structure1[1]+[thickness1]+[thickness2]+structure2[1]]
                            # print '#########', structure3
                            rta = Transfer_matrix_method(self.indexFile, structure3, self.angle, 'average')
                            mvc, _, _, _, _, _, _, _, _ = rta.transfer_matrix_main()
                            conn = psycopg2.connect("dbname=optical_filter user=postgres password=nibaxing")
                            cur = conn.cursor()
                            cur.execute("INSERT INTO firstBF (material1,material2, t1, t2, mv) VALUES (%s, %s, %s, %s, %s)",(materials[mati], materials[matj], thickness1, thickness2, mvc))
                            conn.commit()
                            cur.close()
                            conn.close()
                            mv.append((mvc, materials[mati], materials[matj], thickness1, thickness2))
                            print mvc
        print mv


        #
        #
        #
        #
        # structure = [structure1[0]+structure2[0], structure1[1]+structure2[1]]
        # a = inputArg('average')
        # a.meritvalueCompare(structure)

    def resultPlot(self, ref, trans=[], angles=None, waveStep=None, flag=0, key=1, meritValueinGeneration=[]):
        '''
        :param ref:  ref = r + rs + rp
        :param flag:  flag=0 without transmission, flag=1 with transmission
        :param key: if key=1, regular plot; if key=2, plot in genetic algorithm
        :return: None
        add transmission plot at 6/6/2017
        '''

        if waveStep <= 2:
            '''
            calculate accurate merit value
            '''
            rtemp = ref[:len(ref)/3]
            angles.append(90)
            r_pass = 0
            r_stop = 0
            for i in range(len(rtemp)):
                if angles[i] <=15:
                    r_pass += np.average(rtemp[i][30:70]) * (np.sin(np.deg2rad(angles[i+1])) - np.sin(np.deg2rad(angles[i]))) /np.sin(np.deg2rad(15))
                    r_stop += np.average(rtemp[i][90:250]) * (np.sin(np.deg2rad(angles[i+1])) - np.sin(np.deg2rad(angles[i])))
                else:
                    r_stop += np.average(rtemp[i][30:250]) * (np.sin(np.deg2rad(angles[i+1])) - np.sin(np.deg2rad(angles[i])))
            print r_pass, r_stop,'###' ,1-r_pass
            mv = 0.5 * (1+r_stop)*(1-0.725) / (1-0.725*r_stop) * (1-r_pass)
            print mv, 1-mv, '######################'



            angles = angles[:-1]
            '''
            SQL part
            '''
            conn = psycopg2.connect("dbname=optical_filter user=postgres password=nibaxing")
            cur = conn.cursor()

            cur.execute(''' DROP TABLE IF EXISTS curreflection''')
            cur.execute(''' CREATE TABLE curreflection(
                          id  SERIAL PRIMARY KEY)
            ''')
            fwav = [('w'+str(i)).replace('.', '_') for i in np.arange(self.minWave, self.maxWave+waveStep, waveStep)]
            # delete this

            for wav in fwav:


                cur.execute('''ALTER TABLE curreflection ADD {} TEXT  '''.format(str(wav).replace('.', '_')))
            for r in range(len(ref)):
                temp = []
                for i in ref[r]:
                    if i>0.001:
                        temp.append(str(i))
                    else:
                        temp.append('0')
                cur.execute('''INSERT INTO curreflection({}) VALUES({}) '''.format(','.join(fwav), ','.join(temp)))



            conn.commit()
            cur.close()
            conn.close()

        #######################################################
        if angles is None: angles = self.angle
        if not waveStep: waveStep = self.waveStep
        wav_in = np.arange(self.minWave, self.maxWave + waveStep, waveStep)
        lenAngle = len(angles)
        # print 'len ref', len(ref)


        if lenAngle <= 10:  # regular plot
            for index, ele in enumerate(angles):
                print 'R {} degree'.format(ele), ref[index + 0]
                print 'RS {} degree'.format(ele), ref[index + lenAngle]
                print 'RP {} degree'.format(ele), ref[index + 2 * lenAngle]
            plt.figure(1)

            plt.subplot(221)
            p1 = []
            for index, ele in enumerate(angles):
                temp, = plt.plot(wav_in, ref[index], label='R% ${}^o$ '.format(ele))
                p1.append(temp)
            plt.xlabel('Wavelength (nm)')
            # plt.legend(handles=[p11, p12, p13, p14])
            plt.legend(handles=p1)
            plt.ylim([0, 1])
            plt.ylabel('ratio')
            plt.title('Average Reflection')
            plt.grid(True)

            plt.subplot(222)
            p2 = []
            for index, ele in enumerate(angles):
                temp, = plt.plot(wav_in, ref[index + lenAngle], label='R% ${}^o$ '.format(ele))
                p2.append(temp)
            plt.xlabel('Wavelength (nm)')
            plt.legend(handles=p2)
            plt.ylim([0, 1])
            plt.ylabel('ratio')
            plt.title('RS')
            plt.grid(True)

            plt.subplot(223)
            p3 = []
            for index, ele in enumerate(angles):
                temp, = plt.plot(wav_in, ref[index + 2 * lenAngle], label='R% ${}^o$ '.format(ele))
                p3.append(temp)
            plt.xlabel('Wavelength (nm)')
            plt.legend(handles=p3)
            plt.ylim([0, 1])
            plt.ylabel('ratio')
            plt.title('RP')
            plt.grid(True)
            if not flag: plt.show()

            if flag:
                for index, ele in enumerate(angles):
                    print 'T {} degree'.format(ele), trans[index + 0]
                    print 'TS {} degree'.format(ele), trans[index + lenAngle]
                    print 'TP {} degree'.format(ele), trans[index + 2 * lenAngle]
                plt.figure(2)

                plt.subplot(221)
                p1 = []
                for index, ele in enumerate(angles):
                    temp, = plt.plot(wav_in, trans[index], label='T% ${}^o$ '.format(ele))
                    p1.append(temp)
                plt.xlabel('Wavelength (nm)')
                # plt.legend(handles=[p11, p12, p13, p14])
                plt.legend(handles=p1)
                plt.ylim([0, 1])
                plt.ylabel('ratio')
                plt.title('Average Transmission')
                plt.grid(True)

                plt.subplot(222)
                p2 = []
                for index, ele in enumerate(angles):
                    temp, = plt.plot(wav_in, trans[index + lenAngle], label='T% ${}^o$ '.format(ele))
                    p2.append(temp)
                plt.xlabel('Wavelength (nm)')
                plt.legend(handles=p2)
                plt.ylim([0, 1])
                plt.ylabel('ratio')
                plt.title('TS')
                plt.grid(True)

                plt.subplot(223)
                p3 = []
                for index, ele in enumerate(angles):
                    temp, = plt.plot(wav_in, trans[index + 2 * lenAngle], label='R% ${}^o$ '.format(ele))
                    p3.append(temp)
                plt.xlabel('Wavelength (nm)')
                plt.legend(handles=p3)
                plt.ylim([0, 1])
                plt.ylabel('ratio')
                plt.title('TP')
                plt.grid(True)

            plt.show()
        else:  # 3d plot
            R = []
            RS = []
            RP = []
            for index, ele in enumerate(angles):
                R.append(ref[index])
                RS.append(ref[index + lenAngle])
                RP.append(ref[index + 2 * lenAngle])
            # print np.shape(R)   shape is 12L, 226L
            wav = np.array(wav_in)
            angle = np.array(angles)
            wav, angle = np.meshgrid(wav, angle)

            fig1 = plt.figure(1)
            ax1 = fig1.gca(projection='3d')  # axis 3D
            # The function gca() returns the current axes (a matplotlib.axes.Axes instance), and gcf() returns the current
            #  figure (matplotlib.figure.Figure instance).
            surf1 = ax1.plot_surface(wav, angle, R, cmap=cm.seismic, rcount=200, ccount=200)
            # cmap ref: https://matplotlib.org/examples/color/colormaps_reference.html

            ax1.zaxis.set_major_locator(LinearLocator(10))
            ax1.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

            # Add colorbar
            fig1.colorbar(surf1, shrink=0.5, aspect=5)
            ax1.set_xlabel('wavelength (nm)')
            ax1.set_ylabel('angle (deg)')
            ax1.set_zlabel('reflectance')
            ax1.text2D(0.5, 0.95, 'avg Ref', transform=ax1.transAxes)

            fig2 = plt.figure(2)
            ax2 = fig2.gca(projection='3d')
            surf2 = ax2.plot_surface(wav, angle, RS, cmap=cm.summer, rcount=200, ccount=200)
            fig2.colorbar(surf2, shrink=0.5, aspect=5)
            ax2.set_xlabel('wavelength (nm)')
            ax2.set_ylabel('angle (deg)')
            ax2.set_zlabel('reflectance')
            ax2.text2D(0.5, 0.95, 's-ref', transform=ax2.transAxes)

            fig3 = plt.figure(3)
            ax3 = fig3.gca(projection='3d')
            surf3 = ax3.plot_surface(wav, angle, RP, cmap=cm.winter, rcount=200, ccount=200)
            fig3.colorbar(surf3, shrink=0.5, aspect=5)
            ax3.set_xlabel('wavelength (nm)')
            ax3.set_ylabel('angle (deg)')
            ax3.set_zlabel('reflectance')
            ax3.text2D(0.5, 0.95, 'p-ref', transform=ax3.transAxes)

            plt.show()



# inputs: indexfile, structure, weighting, angle, incidentLightType
class Transfer_matrix_method(object):  # calculate only one sample for one time
    # add s, p and average options at 6/7/2017
    # add inverse 6/7/2017
    # input index_file data frame, structure in 2d list/array form, weighting in 3 list form
    # All decimals
    # return Meritvalue_sample, self.structure.tolist(), RR, TT, AA, RRS, RRP, TTS, TTP

    def __init__(self, indexfile, structure, angle, incidentLightType='average'):
        # indexfile is a data frame, contains 4-5 materials, their index values at different wavelength
        # structure, [[],[]]  1st is material, 2nd is thickness
        # , 3 for angular weight, 4 for stop angle weight
        # default stop band for angle is 35 degree
        # print 'indexfile is', indexfile
        self.waves = np.array(indexfile.index) * 1e-9
        self.total_wave_number = len(self.waves)
        index_incident = list(indexfile['incident'])
        # print'index_incident', index_incident
        index_emergent = list(indexfile['emergent'])  # must convert to list, or index will be included
        index_material1 = list(indexfile['material1'])
        index_material2 = list(indexfile['material2'])
        try:
            index_material3 = list(indexfile['material3'])
        except KeyError:
            index_material3 = np.ones(self.total_wave_number)
        try:
            index_material4 = list(indexfile['material4'])
        except KeyError:
            index_material4 = np.ones(self.total_wave_number)
        try:
            fixed_layer_index = list(indexfile['fixed_layer_index'])
        except KeyError:
            pass

        self.material = structure[0]
        # print structure, '######'
        self.structure = np.array(structure[1]) * 1e-9  # thickness
        self.angle = angle
        self.incidentLight = incidentLightType
        self.indexlist = []
        # print 'mat is', self.material
        for mat in self.material:
            if mat == 'incident':
                self.indexlist.append(index_incident)
            elif mat == 'material1':
                self.indexlist.append(index_material1)
            elif mat == 'material2':
                self.indexlist.append(index_material2)
            elif mat == 'material3':
                self.indexlist.append(index_material3)
            elif mat == 'material4':
                self.indexlist.append(index_material4)
            elif mat == 'fixed_layer':
                self.indexlist.append(fixed_layer_index)
            elif mat == 'emergent':
                self.indexlist.append(index_emergent)

    def transfer_matrix_main(self):
        # calculate Reflection, transmission and absorption of a system
        # return Meritvalue_sample, self.structure.tolist(), RR, TT, AA, RRS, RRP, TTS, TTP
        Meritvalue_sample = []
        # print 'thickness is', self.structure
        Meritvalue_detail = []  # merit value at different angle
        RR = []  # reflection for all angles at all wavelength
        RRS = []
        RRP = []
        TT = []
        TTS = []
        TTP = []
        AA = []
        for ang in self.angle:
            wav_count = 0
            R = []
            RS = []
            RP = []
            T = []
            TS = []
            TP = []
            A = []
            Meritvalue_temp = []  # merit value for a wavelength
            while wav_count < len(self.waves):
                TSmatrix, TPmatrix, theta_list = self.tmatrix_method(wav_count, ang)
                # print 'theta_list', theta_list
                P1 = self.pmatrix_method_coherent(wav_count, self.structure, theta_list)
                System_matrix = self.system_matrix_coherent(TSmatrix, TPmatrix, P1)
                r, t, a, rs, rp, ts, tp = self.rta_calculation_coherent(System_matrix)
                # print 'r', r, 't', t, 'a' ,a
                if self.incidentLight == 'p-polarized':
                    r = rp
                    t = tp
                elif self.incidentLight == 's-polarized':
                    r = rs
                    t = ts
                R.append(r)
                RS.append(rs)
                RP.append(rp)
                T.append(t)
                TS.append(ts)
                TP.append(tp)
                A.append(a)
                wav_count += 1
            RR.append(R)
            # print len(RR)
            RRS.append(RS)
            RRP.append(RP)
            TT.append(T)
            TTS.append(TS)
            TTP.append(TP)
            AA.append(A)
        # Now calculate the new merit value
        pb_index1, pb_index2 = int(len(self.waves) * 3/30), int(len(self.waves) * 7/30)
        sb_index1, sb_index2 = int(len(self.waves) * 9/30), int(len(self.waves) * 25/30)


        if len(self.angle) >=2:
            R_pb = RR[0][pb_index1:pb_index2+1] + RR[1][pb_index1:pb_index2+1]
            R_pb = float(np.mean(R_pb))
            R_sb = []
            factor1 = 1/np.sin(np.deg2rad(15))  # ratio for passband
            factor2 = 1/np.sin(np.deg2rad(self.angle[-1]))  # ratio for stopband
            for i in range(len(self.angle)):
                if i == 0:
                    factor_cur = np.sin(np.deg2rad(self.angle[1]/2)) * factor2
                elif i == len(self.angle)-1:
                    factor_cur = (np.sin(np.deg2rad(self.angle[i])) - np.sin(0.5*(np.deg2rad(self.angle[i-1])+np.deg2rad(self.angle[i-1]))))* factor2
                else:
                    factor_cur = (np.sin(0.5*(np.deg2rad(self.angle[i+1])+np.deg2rad(self.angle[i]))) - np.sin(0.5*(np.deg2rad(self.angle[i])+np.deg2rad(self.angle[i-1])))) * factor2
                if i <= 1:  # the first two angle has some part in passband
                    R_sb.append(factor_cur*np.average([RR[i][j] for j in range(sb_index1, sb_index2+1)]))
                else:
                    R_sb.append(factor_cur*np.average([RR[i][j] for j in range(pb_index1, sb_index2+1)]))
            '''
            OSRAM Merit value part
            '''
            R_sb = sum(R_sb)
            RF = 0.725
            meritValue = 0.5*(1-RF)*(1+R_sb)/(1-RF*R_sb)*(1-1.5*R_pb)
            print 'R_pb, R_pb, MeritValue', R_pb, R_sb, 1.0 - meritValue
        else:
            meritValue = 0
        return 1.0 - meritValue, self.structure.tolist(), RR, TT, AA, RRS, RRP, TTS, TTP

    def tmatrix_method(self, count, ang):
        # count is for current wavelength
        length = len(self.indexlist)
        TS = []
        TP = []
        layer_num = 0
        thetai = np.deg2rad(ang)
        thetalist = []
        thetalist.append(thetai)
        while layer_num < length - 1:  # for each layer
            # print 'indexlist', self.indexlist
            # print 'layernumber', layer_num, 'count', count
            n1 = self.indexlist[layer_num][count]
            n2 = self.indexlist[layer_num + 1][count]
            thetat = np.conj(cmath.asin(n1 / n2 * np.sin(thetai)))  # Snell's law
            thetalist.append(thetat)  # for theta in P matrix
            ts = 2 * n1 * np.conj(cmath.cos(thetai)) / (
            n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            tp = 2 * n1 * np.conj(cmath.cos(thetai)) / (
            n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            rs = (n1 * np.conj(cmath.cos(thetai)) - n2 * np.conj(cmath.cos(thetat))) / (
            n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            rp = (n2 * np.conj(cmath.cos(thetai)) - n1 * np.conj(cmath.cos(thetat))) / (
            n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            thetai = thetat  # update theta for next interface
            TS.append([[1 / ts, rs / ts], [rs / ts, 1 / ts]])
            TP.append([[1 / tp, rp / tp], [rp / tp, 1 / tp]])
            layer_num += 1
        return TS, TP, thetalist

    def pmatrix_method_coherent(self, wav_count, sam, theta_list):
        length = len(self.indexlist)  # length of all materials include incident and emergent
        P1 = []
        layer_num = 1  # skip incident
        while layer_num < length - 1:  # skip emergent
            # print self.indexlist,  'indexlist'
            n = self.indexlist[layer_num][wav_count]
            thickness = sam[layer_num - 1]
            theita = theta_list[layer_num]
            # print 'theita', theita
            # cosine = cmath.cos(theita)
            # if np.iscomplex(cosine): theita = theita * np.exp(1j*np.pi/2)
            wave = self.waves[wav_count]
            p1 = [[np.exp(-2 * np.pi * n * thickness * 1j * cmath.cos(theita) / wave), 0],
                  [0, np.exp(2 * np.pi * n * thickness * 1j * cmath.cos(theita) / wave)]]
            P1.append(p1)
            layer_num += 1
        return P1

    def system_matrix_coherent(self, TS, TP, P1):
        Ss1, Ssb1 = self.matrix_multiplicate(TS, P1)
        Sp1, Spb1 = self.matrix_multiplicate(TP, P1)
        # print 'Ss1', Ss1, 'Sp1', Sp1
        return (Ss1, Sp1, Ssb1, Spb1)

    def matrix_multiplicate(self, T, P):
        # two side calculation!!!
        count = 0
        S = np.identity(2)
        SB = np.identity(2)
        TB = []
        PB = []
        while count < len(T):
            T[count] = np.array(T[count])
            T[count].reshape(2, 2)
            # print len(T), count, len(T)-1-count
            # print T[50]
            TB.append(np.array(T[len(T) - 1 - count]))
            TB[count].reshape(2, 2)
            S = np.dot(S, T[count])
            SB = np.dot(S, TB[count])

            if count < len(T) - 1:
                P[count] = np.array(P[count])
                PB.append(np.array(P[len(P) - 1 - count]))
                P[count].reshape(2, 2)
                PB[count].reshape(2, 2)
                S = np.dot(S, P[count])
                SB = np.dot(SB, PB[count])
            count += 1
        return S, SB

    def rta_calculation_coherent(self, System_matrix):
        ss1, sp1, ssb1, spb1 = System_matrix

        RS = np.absolute(ss1[1][0] / ss1[0][0]) ** 2
        RP = np.absolute(sp1[1][0] / sp1[0][0]) ** 2
        RSB = np.absolute(ssb1[1][0] / ssb1[0][0]) ** 2
        RPB = np.absolute(spb1[1][0] / spb1[0][0]) ** 2

        TS = 1 / np.absolute(ss1[0][0]) ** 2
        TP = np.absolute(np.linalg.det(sp1) / sp1[0][0]) ** 2
        TSB = 1 / np.absolute(ssb1[0][0]) ** 2
        TPB = np.absolute(np.linalg.det(spb1) / spb1[0][0]) ** 2
        if RS > 1: RS = 1
        if RP > 1: RP = 1
        if RSB > 1: RSB = 1
        if RPB > 1: RPB = 1
        R = (RS + RP) / 2.
        RB = (RSB + RPB) / 2.
        T = (TS + TP) / 2.
        TB = (TSB + TPB) / 2.
        A = 1 - R - T
        AB = 1 - RB - TB

        return RB, T, A, RSB, RPB, TS, TP




# inputs: case, gen_loop_number, index_file, layerNo, weighting, angle, central_wave, tag, incidentLightType, timeLimit=0
# add timeLimit 6/7/2017, timeLimit in seconds
class Genetic_algorithm_for_thin_film_filter:
    def __init__(self, case, gen_loop_number, index_file, layerNo,  angle, central_wave, tag,
                 incidentLightType, timeLimit=None):
        self.case = int(case)
        self.current_generation = 1
        self.index_file = index_file
        self.tag = tag
        self.gen_loop_number = gen_loop_number
        self.pop_size = 100  # sample size for each population
        self.co = 0.9  # chance of cross over
        self.mu = 0  # chance of mutation
        self.central_wave = central_wave
        self.layer_number = layerNo
        self.total_wave_number = len(self.index_file['material1'])
        self.current_center = 90
        self.current_range = 30
        self.angle = angle
        self.incidentLightType = incidentLightType
        self.timeLimit = timeLimit
        if timeLimit:
            self.timeOut = timeLimit + time.time()
            self.current_generation = 0
        else:
            self.timeOut = None
        print 'tag=', tag

    def genetic_algorithm_main(self):
        current_generation = 1
        # disable if not in GUI
        # ui.progressBar.setMaximum(self.gen_loop_number+1)
        # ui.progressBar.setValue(1)
        best_in_gen = []
        best_overall = []
        indexfile = self.index_file
        old_samples = []
        while current_generation <= self.gen_loop_number or time.time() < self.timeOut:
            if current_generation == 1:
                old_samples = self.pad_first_batch()
            samples = self.pad_current_bunch(old_samples)  # pad into 100 samples
            # print 'padded samples', samples
            merit_and_structure = []
            merit_value = []
            for sam in range(len(samples)):  # find merit values in each sample
                structure = translate_structure(samples[sam], self.central_wave, self.index_file)
                # print '###', structure
                transfer = Transfer_matrix_method(indexfile, structure, self.angle, self.incidentLightType)
                mv, _, _, _, _, _, _, _, _ = transfer.transfer_matrix_main()
                merit_value.append(mv)
                merit_and_structure.append([mv, current_generation, structure])  # this is for output
            good_index = [i[0] for i in sorted(enumerate(merit_and_structure), key=lambda x: x[1][0])][0:40]  # sort
            new_samples = [samples[i] for i in good_index]
            new_sample_merit_value = [merit_value[i] for i in good_index]
            current_good_sample = sorted(merit_and_structure, key=lambda x: x[0])[0:3]  # sort, for display and save
            best_in_gen.append(current_good_sample[0])
            print 'Current good sample is {}'.format(current_good_sample[0])
            self.current_center, self.current_range = structure2csv(current_good_sample[0], self.tag,
                                                                    self.current_center, self.current_range,
                                                                    self.central_wave, self.index_file,
                                                                    self.case)  # write to csv
            cross_over_samples = self.crossover(new_samples, new_sample_merit_value)
            new_samples.extend(cross_over_samples)
            old_samples = new_samples
            if self.timeLimit is None: current_generation += 1
            # ui.progressBar.setValue(current_generation)

        best_overall = [i for i in sorted(best_in_gen, key=lambda x: x[0])][0]
        return best_overall, best_in_gen

    def pad_first_batch(self):
        try:
            data = read_csv_log(self.tag)
            history_data = []
            for ele in data:
                structure, _ = best_old_sample(ele, self.central_wave, self.index_file, self.case)
                history_data.append(structure)
            print 'history_data', history_data
            if len(history_data) >= 40:
                return history_data[0:40]
            else:
                return history_data
        except IOError:
            return None

    def pad_current_bunch(self, current_batch):
        layers = self.layer_number
        if current_batch is None: current_batch = []
        padding_number = self.pop_size - len(current_batch)
        case = self.case
        padding_count = 0
        pad_bunch = []
        phase_center = []
        try:
            data = read_csv_log(self.tag)
            structure, _ = best_old_sample(data, self.central_wave, self.index_file, self.case)
            if structure != []:
                pad_bunch.append(structure)
                phase_center, phase_range = frequency_analyze(data, self.central_wave, self.index_file, self.tag)
                padding_number -= 1
        except (IOError, IndexError):
            pass
        while padding_count < padding_number:
            current_layer_no = 0
            current_sample = []
            old_material = 0
            while current_layer_no < layers:
                current_material = self.choose_material(case, old_material)
                old_material = current_material
                if (phase_center and np.random.rand(1) < 0.33):
                    current_phase = np.random.normal(phase_center, phase_range / 3, 1)
                else:
                    current_phase = np.random.normal(self.current_center, self.current_range / 3, 1)
                current_sample.extend([int(current_material), int(current_phase)])
                current_layer_no += 2
            pad_bunch.append(current_sample)
            padding_count += 1
        if current_batch is [] or None:
            return pad_bunch
        else:
            return current_batch + pad_bunch

    def choose_material(self, case, old_material):  # random int from 1-10
        if case == 2:
            return 1  # low, high, size
        if case == 3:
            if old_material in [0, 1, 2]:
                return np.random.randint(1, 3, 1)
            if old_material == 3:
                return random.choice([1, 3])
        if case == 4:
            if old_material in [0, 1, 2, 4]:
                return np.random.randint(1, 6, 1)
            if old_material == 3:
                return random.choice([1, 3, 4, 5, 6])
            if old_material == 5:
                return random.choice([1, 2, 3, 5])
            if old_material == 6:
                return random.choice([1, 3, 4, 5, 6])

    def crossover(self, samples, mvs):
        count = 0
        cross_over_sample = []
        while count < 15:
            new_mvs = [np.exp(-i / 500) for i in mvs]
            total_mv = sum(new_mvs)
            current_sum = 0
            mv_normalize = [0]
            for ele in new_mvs:
                current_sum += ele
                mv_normalize.append(current_sum / total_mv)
            # normalized by exp(-mv/500)
            rand1, rand2 = np.random.rand(2)
            # random picked
            first = 1
            second = 1
            for count in range(len(mv_normalize) - 2):
                if (mv_normalize[count] < rand1 < mv_normalize[count + 1]):
                    first = int(count)
                if mv_normalize[count] < rand2 < mv_normalize[count + 1]:
                    second = int(count)
            length = len(samples[0])
            break_point = int(np.random.randint(1, length - 2))
            cross_over_sample.append(samples[first][0:break_point] + samples[second][break_point:])
            cross_over_sample.append(samples[second][0:break_point] + samples[first][break_point:])
            # crossover
        count += 1
        return cross_over_sample  # 30 cross_over_sample


def translate_structure(sam, central_wave, index_file):
    # translate phase thickness to real thickness
    material = []
    thickness = []
    material.append('incident')
    index_material = []
    index_material.append(np.real(index_file.loc[central_wave]['material1']))
    index_material.append(np.real(index_file.loc[central_wave]['material2']))
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material3']))
    except:
        pass
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material4']))
    except:
        pass
    count = 0
    while count < len(sam):
        if sam[count] == 1:
            material.extend(['material2', 'material1'])
            thickness.extend([central_wave * sam[count + 1] / 360 / index_material[1], \
                              central_wave * sam[count + 1] / 360 / index_material[0]])
        elif sam[count] == 2:
            material.extend(['material3', 'material1'])
            thickness.extend([central_wave * sam[count + 1] / 360 / index_material[2], \
                              central_wave * sam[count + 1] / 360 / index_material[0]])
        elif sam[count] == 3:
            material.extend(['material2', 'material3'])
            thickness.extend([central_wave * sam[count + 1] / 360 / index_material[1], \
                              central_wave * sam[count + 1] / 360 / index_material[2]])
        elif sam[count] == 4:
            material.extend(['material4', 'material1'])
            thickness.extend([central_wave * sam[count + 1] / 360 / index_material[3], \
                              central_wave * sam[count + 1] / 360 / index_material[0]])
        elif sam[count] == 5:
            material.extend(['material2', 'material4'])
            thickness.extend([central_wave * sam[count + 1] / 360 / index_material[1], \
                              central_wave * sam[count + 1] / 360 / index_material[3]])
        elif sam[count] == 6:
            material.extend(['material4', 'material3'])
            thickness.extend([central_wave * sam[count + 1] / 360 / index_material[3], \
                              central_wave * sam[count + 1] / 360 / index_material[2]])

        count += 2
    # print '#####', index_file
    if 'fixed_layer_index' in index_file:
        material.append('fixed_layer')
        thickness.append(1000)
    material.append('emergent')
    structure = [material, thickness]
    return structure  # number to name


def structure2csv(structure, tag, central_phase, phase_range, central_wave, index_file, material_count):
    # save good structures to csv file, no repeat file
    # gradient descent for
    try:
        f = open(''.join([tag, '.csv']), 'r')
        content = csv.reader(f)
        recorded_merit_value = []
        for row in content:
            recorded_merit_value.append(float(row[0]))
        f.close()
    except IOError:
        recorded_merit_value = []

    f = open(''.join([tag, '.csv']), 'a')
    fw = csv.writer(f)
    if (recorded_merit_value) and (structure[0] not in recorded_merit_value):
        fw.writerow([structure[0], structure[2][0], structure[2][1]])  # merit value
        old_min_mv = min(recorded_merit_value)
        new_mv = structure[0]
    elif not recorded_merit_value:
        fw.writerow([structure[0], structure[2][0], structure[2][1]])
    f.close()
    if (recorded_merit_value) and (structure[0] not in recorded_merit_value):
        data = read_csv_log(tag)
        mmean, rrange = frequency_analyze(data, central_wave, index_file, material_count)
        new_central_phase = central_phase - (central_phase - mmean) * abs(new_mv - old_min_mv) / old_min_mv
        # learning rate depend on how much the merit value decreases
        new_phase_range = phase_range - (phase_range - rrange) * abs(new_mv - old_min_mv) / old_min_mv
        if new_phase_range >= 45: new_phase_range = 45
        print 'updated central_phase and range are', new_central_phase, new_phase_range
        return new_central_phase, new_phase_range
    else:
        return central_phase, phase_range


def read_csv_log(tag):
    # return all data in real thickness
    # gradient descent is added
    filename = ''.join([tag, '.csv'])
    f = open(filename, 'r')
    content = csv.reader(f)
    merit_value = []
    material = []
    thickness = []
    for row in content:
        a = float(row[0])
        merit_value.append(a)
        comma_index = [i for i, ltr in enumerate(row[1]) if ltr == '\'']
        material_temp = []
        for count in range(len(comma_index) - 1):
            if (comma_index[count + 1] - comma_index[count]) > 5:
                start = comma_index[count] + 1
                end = comma_index[count + 1]
                material_temp.append(row[1][start:end])
        material.append(material_temp)

        comma_index2 = [i for i, ltr in enumerate(row[2]) if ltr == ',']
        thickness_temp = []
        valid = 1
        for count in range(len(comma_index2) - 1):
            if (comma_index2[count + 1] - comma_index2[count]) > 3:
                start = comma_index2[count] + 1
                end = comma_index2[count + 1]
                if valid == 1:
                    thickness_temp.append(float(row[2][1:start - 1]))
                    valid = 2
                thickness_temp.append(float(row[2][start:end]))
        thickness_temp.append(float(row[2][end + 1:-1]))
        thickness.append(thickness_temp)
    data = zip(merit_value, material, thickness)
    sorted(data, key=lambda x: x[0])
    for count in range(len(data) - 1):
        if data[count][0] == data[count + 1][0]:
            data[count] = []
    try:
        while 1:
            data.remove([])
    except ValueError:
        data = data[::-1]
        # print 'returned data is {}'.format(data)
        return data


def best_old_sample(data, central_wave, index_file, material_count=2):
    # input real thickness from read_csv_log
    # return phase thickness
    # padding layer won't bother

    index_material = []
    index_material.append(np.real(index_file.loc[central_wave]['material1']))
    index_material.append(np.real(index_file.loc[central_wave]['material2']))
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material3']))
    except KeyError:
        pass
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material4']))
    except KeyError:
        pass
    structure = []
    material_no = []
    try:
        material = data[0][1]
        real_thickness = data[0][2]
        phase_thickness = []
        for count in range(len(data[0][1]) - 1):
            if data[0][1][count] == 'material1':
                index = index_material[0]
            elif data[0][1][count] == 'material2':
                index = index_material[1]
            elif data[0][1][count] == 'material3':
                index = index_material[2]
            elif data[0][1][count] == 'material4':
                index = index_material[3]
            else:
                index = 0
            if index != 0:
                phase_thickness.append(data[0][2][count - 1] * index / central_wave * 360)
    except TypeError:
        material = data[1]
        real_thickness = data[2]
        phase_thickness = []
        for count in range(len(data[1]) - 1):
            if data[1][count] == 'material1':
                index = index_material[0]
            elif data[1][count] == 'material2':
                index = index_material[1]
            elif data[1][count] == 'material3':
                index = index_material[2]
            elif data[1][count] == 'material4':
                index = index_material[3]
            else:
                index = 0
            if index != 0:
                phase_thickness.append(data[2][count - 1] * index / central_wave * 360)
    # print 'data1 is ', data[1]
    record_material = material[1:-1]
    count = 0
    while count <= len(record_material) - 2:
        if record_material[count:count + 2] == ['material2', 'material1']:
            material_no.append(1)
        elif record_material[count:count + 2] == ['material3', 'material1']:
            material_no.append(2)
        elif record_material[count:count + 2] == ['material2', 'material3']:
            material_no.append(3)
        elif record_material[count:count + 2] == ['material4', 'material1']:
            material_no.append(4)
        elif record_material[count:count + 2] == ['material2', 'material4']:
            material_no.append(5)
        elif record_material[count:count + 2] == ['material4', 'material3']:
            material_no.append(6)
        count += 2
    count = 0
    count_for_phase = 0
    # print 'material_no', material_no, phase_thickness
    while count <= (len(material_no) - 1):
        structure.append(material_no[count])
        structure.append(phase_thickness[count_for_phase])
        count_for_phase += 2
        count += 1
    return structure, [material, structure]


def realThickness2phaseThickness(structure, central_wave, index_file, material_count):
    index_material = []
    index_material.append(np.real(index_file.loc[central_wave]['material1']))
    index_material.append(np.real(index_file.loc[central_wave]['material2']))
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material3']))
    except KeyError:
        pass
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material4']))
    except KeyError:
        pass
    phase_thickness = []
    for count in range(len(structure[0])):
        if structure[0][count] == 'material1':
            index = np.real(index_material[0])
        elif structure[0][count] == 'material2':
            index = np.real(index_material[1])
        elif structure[0][count] == 'material3':
            index = np.real(index_material[2])
        elif structure[0][count] == 'material4':
            index = np.real(index_material[3])
        else:
            index = 0
        if index != 0:
            phase_thickness.extend([structure[0][count], structure[1][count - 1] * index / central_wave * 360])

    old_structure = []
    mat_buf = []
    phase_buf = []
    for i in range(len(phase_thickness)):

        if i % 2 == 1 and phase_buf:
            # print '#',phase_buf
            # print phase_thickness[i]
            if abs(phase_thickness[i] - phase_buf[-1]) <= 0.15:
                # mat_buf.append(phase_thickness[i-1])
                # print mat_buf
                if mat_buf in [['material2', 'material1'], ['material1', 'material2']]:
                    old_structure.append(1)
                    old_structure.append(phase_buf[-1])
                    phase_buf, mat_buf = [], []
                elif mat_buf == ['material3', 'material1']:
                    old_structure.append(2)
                    old_structure.append(phase_buf[-1])
                    phase_buf, mat_buf = [], []
                elif mat_buf == ['material2', 'material3']:
                    old_structure.append(3)
                    old_structure.append(phase_buf[-1])
                    phase_buf, mat_buf = [], []
                elif mat_buf == ['material4', 'material1']:
                    old_structure.append(4)
                    old_structure.append(phase_buf[-1])
                    phase_buf, mat_buf = [], []
                elif mat_buf == ['material2', 'material4']:
                    old_structure.append(5)
                    old_structure.append(phase_buf[-1])
                    phase_buf, mat_buf = [], []
                elif mat_buf == ['material4', 'material3']:
                    old_structure.append(6)
                    old_structure.append(phase_buf[-1])
                    phase_buf, mat_buf = [], []
                else:
                    phase_buf, mat_buf = [], []
        if i % 2 == 0:
            mat_buf.append(phase_thickness[i])
        if i % 2 == 1:
            phase_buf.append(phase_thickness[i])
    return phase_thickness, old_structure


def frequency_analyze(data, central_wave, index_file, material_count=2):
    # return central phase and phase range
    print '#####', data
    index_material = []
    index_material.append(np.real(index_file.loc[central_wave]['material1']))
    index_material.append(np.real(index_file.loc[central_wave]['material2']))
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material3']))
    except KeyError:
        pass
    try:
        index_material.append(np.real(index_file.loc[central_wave]['material4']))
    except KeyError:
        pass
    phase_thickness = []
    for samples in data:
        for count in range(len(samples[1]) - 1):
            if samples[1][count] == 'material1':
                index = np.real(index_material[0])
            elif samples[1][count] == 'material2':
                index = np.real(index_material[1])
            elif samples[1][count] == 'material3':
                index = np.real(index_material[2])
            elif samples[1][count] == 'material4':
                index = np.real(index_material[3])
            else:
                index = 0
            if index != 0:
                phase_thickness.append(samples[2][count - 1] * index / central_wave * 360)
    frequency = {}
    # print 'phasethickness {}'.format(phase_thickness)
    for ele in phase_thickness:  # count frequencies
        if frequency.has_key(int(ele)):
            frequency[int(ele)] += 1
        else:
            frequency[int(ele)] = 1
    sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1))
    # print sorted_frequency [(87, 4), (99, 4), (105, 4), (97, 8), (81, 12), (85, 12), (95, 12), (106, 12), (86, 14)
    sum_weight = 0
    sum_angle = 0
    phases = []
    counts = []
    for phase, count in sorted_frequency:
        phases.append(phase)
        counts.append(count)
        sum_weight += count
        sum_angle += phase * count
    ran = max(phases) - min(phases)
    weight_mean = sum_angle / sum_weight
    return weight_mean, ran


# inputs: case, minWave, waveStep, maxWave, incident, emergent, material1, material2, material3=None, material4=None, fixedLayerIndex=None
def indexfile_format(case, minWave, waveStep, maxWave, incident, emergent, material1, material2, material3=None,
                     material4=None, fixedLayerIndex=None):
    # return index file in panda dataframe, and wavin
    nin, wavin = readindexfile(incident, minWave, waveStep, maxWave)
    ne, _ = readindexfile(emergent, minWave, waveStep, maxWave)
    nm1, _ = readindexfile(material1, minWave, waveStep, maxWave)
    nm2, _ = readindexfile(material2, minWave, waveStep, maxWave)
    if case >= 3:
        nm3, _ = readindexfile(material3, minWave, waveStep, maxWave)
    if case >= 4:
        nm4, _ = readindexfile(material4, minWave, waveStep, maxWave)
    if fixedLayerIndex is not None:
        total_count = int((-minWave + maxWave + waveStep) / waveStep)
        nfix = np.ones(total_count) * fixedLayerIndex
    indexdata = {'incident': nin,
                 'emergent': ne,
                 'material1': nm1,
                 'material2': nm2,
                 }
    # print len(nin), len(ne), len(nm1), len(nm2)
    indexfile = pd.DataFrame(indexdata)
    if wavin[-1]>maxWave: wavin = wavin[:-1]
    indexfile.index = wavin
    #print len(nfix), total_count
    if fixedLayerIndex is not None: indexfile['fixed_layer_index'] = nfix
    if case >= 3:
        indexfile['material3'] = nm3
    if case >= 4:
        indexfile['material4'] = nm4

    return indexfile, wavin


def readindexfile(filename, startwavelength, wavelengthstep, stopwavelength):  # back_up 5/30/2017
    # note: absorption coefficient k is disabled
    # this function will be used in index format
    # add linear mapping 5/30/2017
    filepath = "./indexfile/" + filename
    f = open(filepath, 'r')
    wavelength = []
    n = []  # refractive index
    k = []
    flag_k = 1
    for line in f.readlines():  # find the start of index file
        if re.match('[0-9.]{3,8}\t[0-9.]{1,15}\t[.-z]{1,8}', line) is not None:
            index_of_tab = [i for i, ltr in enumerate(line) if ltr == '\t']
            wavelength.append(line[0:index_of_tab[0]])
            # print 'line', line
            n.append(line[index_of_tab[0] + 1:index_of_tab[1]])
            k.append(line[index_of_tab[1] + 1:])
        elif re.match('[0-9.]{3,8}\t[0-9.]{1,15}', line) is not None:  # no k values in the index file
            index_of_tab = [i for i, ltr in enumerate(line) if ltr == '\t']
            wavelength.append(line[0:index_of_tab[0]])
            n.append(line[index_of_tab[0] + 1:])
            flag_k = 0
    if flag_k:
        k = [float(i) for i in k[1:]]
    wavelength = [float(i) for i in wavelength[1:]]  # wav from file
    n = [float(i) for i in n[1:]]

    # select_index = []
    indexTable = 0
    nin = []
    total_index = int((stopwavelength - startwavelength) / wavelengthstep)  # wav will be use in the panda frame
    while indexTable <= total_index:  # for every sampling point
        for index in range(len(wavelength) - 1):
            if (wavelength[index] <= startwavelength + wavelengthstep * indexTable) and \
                    (wavelength[index + 1] > startwavelength + wavelengthstep * indexTable):
                ratio = (-wavelength[index] + startwavelength + wavelengthstep * indexTable) / (
                wavelength[index + 1] - wavelength[index])
                # nin.append(n[index]+ratio*(n[index+1]-n[index]))
                if flag_k:
                    nin.append(n[index] + ratio * (n[index + 1] - n[index]) + 1j * (
                    k[index] + ratio * (k[index + 1] - k[index])))
                else:
                    nin.append(n[index] + ratio * (n[index + 1] - n[index]))
                # print 'nin', nin
                # print 'ratio', ratio

                continue
                # nin.append(complex(n[index], k[index]))
                # select_index.append(index)
        indexTable += 1

    wav_in = np.arange(startwavelength, stopwavelength + wavelengthstep, wavelengthstep)
    # print 'nin',len(nin), nin,
    return nin, wav_in



def getDatafromSQL():   # modify layer number in the cur.execute line
    # 6/21/2017
    conn = psycopg2.connect("dbname=optical_filter user=postgres password=nibaxing")
    cur = conn.cursor()
    # temp = cur.execute("select * from optimizedstructure1 where lt24 is not null and meritvalue < 0.4")
    # temp = cur.execute("select * from twomatframe where meritvalue < 1")
    temp = cur.execute("select * from optimizedstructure1 where meritvalue < 0.5138 and meritvalue > 0.5137")
    # temp = cur.execute(''' select * from firstbf where mv = (select min(mv) from firstbf) ''')
    rows = cur.fetchall()
    STRUCT = []
    # print rows
    for row in rows:
        temp = []
        temp.append(row[0][:row[0].index(' ')])  # material1's name
        temp.append(row[1][:row[1].index(' ')])  # material2's name
        #temp.extend([float(i) for i in row[5:15]+row[16:]])  # thickness, exclude sample id
        temp.extend([float(i) for i in row[3:]])  # thickness
        STRUCT.append(temp)
    print STRUCT
    return STRUCT

def multiOptimization(STRUCT):
    for st in STRUCT:
        material1 = st[0]
        material2 = st[1]
        print material1, material2
        struct = [['incident',  'material2', 'material1', 'material2', 'material1', 'material2',
                          'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
                          'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2',
                          'material1', 'material2', 'material1', 'material2','material1', 'emergent']]
        struct.append(st[2:])
        print struct
        a = inputArg(incidentLight='average')

        a.localMinimum(structure=struct, material1=material1, material2=material2)

def testPlot():
    a = inputArg()
    # this is the recipe generated at 7/8 with mv = 0.13
    #structure = [['incident', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material3', 'material4', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'emergent'], [118.70866169551846, 201.30289017340644, 110.55147553786725, 116.9618497109825, 75.75682726816278, 114.89421965317905, 64.48893764992467, 99.18843930635838, 72.72171002473175, 112.71676300578035, 63.024054893355896, 98.26589595375724, 72.52171002473176, 112.71676300578035, 63.68893764992469, 99.18843930635838, 72.72171002473175, 112.71676300578035, 72.25682726816298, 147.69421965317719, 109.41635829443612, 118.48439306358362, 84.43542034698812, 123.86473988439292, 27.0, 17.0, 79.47588932071311, 114.36447238111708, 69.60264797218136, 103.11743504543148, 80.23542034698836, 112.97034900396683, 78.36518586012608, 114.82328731539152, 67.7431169459062, 97.61155842258215, 65.32405489335584, 96.69980517688289, 69.74311694590608, 98.91155842258208, 67.91335143276855, 98.85862011115725, 109.23908920170297, 153.6996834124349, 75.9758893207133, 135.96447238111585, 114.29260650463809, 129.00560874106384, 83.47889618238283, 121.76444802822772]]
    # structure from GA
    #structure = [['incident', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'emergent'], [91.87053759041974, 129.8938798482544, 84.95448239953882, 151.88210224966588, 83.17889618238281, 120.06444802822779, 67.82405489335586, 95.19980517688315, 76.74077207728209, 122.3409415368296, 93.49260650463948, 118.10560874106389, 68.3377652156126, 97.14096588971935, 65.41335143276868, 89.45862011115742, 67.60799970247503, 92.08802757829457, 66.11335143276865, 93.65862011115746, 73.91635829443814, 57.45859575826781, 83.67889618238281, 114.6644480282277]]

    # this is the recipe generated at 7/11 with slightly different merit function, mv = 0.296
    #structure = [['incident', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'emergent'], [88.27588932071295, 125.16447238111682, 64.70264797218138, 106.61743504543139, 80.73542034698829, 109.27034900396664, 78.3651858601259, 118.72328731539163, 68.54311694590622, 97.61155842258206, 67.02405489335574, 93.79980517688297, 69.3431169459061, 100.41155842258213, 67.41335143276858, 83.75862011115733, 108.539089201703, 157.69968341243467, 76.67588932071327, 109.16447238111718, 102.19260650463876, 136.20560874106346, 83.77889618238281, 126.16444802822767, 110, 167.99999999999997, 109.51983288381038, 136.32543352601107, 86.66479566355447, 102.92080924855442, 79.98838304366494, 113.59421965317904, 73.46479566355524, 111.42080924855473, 70.74184027786733, 91.63352601156075, 80.08838304366493, 112.0942196531792, 68.61102243214262, 76.88843930635835, 113.55159872116745, 182.44971098265864, 79.40379196652731, 102.51676300578033, 84.980836580839, 135.32947976878597, 116.85882918678233, 98.92138728323701, 87.89656150091204, 126.34508670520235]]

    # 7/16 LDS
    # structure = [['incident', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'emergent'], [88.27588932071295, 125.16447238111682, 64.70264797218138, 106.61743504543139, 80.73542034698829, 109.27034900396664, 78.3651858601259, 118.72328731539163, 68.54311694590622, 97.61155842258206, 67.02405489335574, 93.79980517688297, 69.3431169459061, 100.41155842258213, 67.41335143276858, 83.75862011115733, 108.539089201703, 157.69968341243467, 76.67588932071327, 109.16447238111718, 102.19260650463876, 136.20560874106346, 83.77889618238281, 126.16444802822767, 110, 167.99999999999997, 109.51983288381038, 136.32543352601107, 86.66479566355447, 102.92080924855442, 79.98838304366494, 113.59421965317904, 73.46479566355524, 111.42080924855473, 70.74184027786733, 91.63352601156075, 80.08838304366493, 112.0942196531792, 68.61102243214262, 76.88843930635835, 113.55159872116745, 182.44971098265864, 79.40379196652731, 102.51676300578033, 84.980836580839, 135.32947976878597, 116.85882918678233, 98.92138728323701, 87.89656150091204, 126.34508670520235]]

    #7/17
    structure = [['incident', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'emergent'], [71.67588932071295, 123.36447238111684, 68.20264797218141, 87.81743504543152, 72.23542034698849, 118.47034900396687, 89.96518586012594, 145.52328731539095, 68.74311694590621, 87.41155842258215, 68.42405489335567, 95.49980517688286, 70.14311694590606, 93.01155842258224, 65.51335143276869, 86.95862011115726, 107.93908920170304, 156.09968341243476, 73.17588932071345, 111.66447238111702, 98.79260650463895, 138.40560874106333, 82.37889618238289, 137.76444802822718, 106.70000000000012, 184.09999999999908, 112.51983288381021, 120.12543352601139, 86.86479566355447, 117.82080924855411, 75.3883830436651, 115.194219653179, 73.16479566355525, 99.12080924855488, 68.24184027786745, 97.73352601156056, 78.28838304366504, 103.69421965317912, 65.21102243214268, 71.98843930635816, 109.35159872116758, 204.14971098265872, 71.60379196652742, 126.61676300578029, 81.080836580839, 169.82947976878563, 117.15882918678236, 22.92138728323704, 82.89656150091207, 146.84508670520194]]






    a.plotStructure(structure, angle=range(0,90,1), waveStep=1)




def testGA():
    a = inputArg(incidentLight='average')
    a.recipeGenerator_geneticAlgorithm(genNo=10, timeLimit=None, layerNo=10)


def testlocalM():
    a = inputArg(incidentLight='average')
    a.localMinimum()


def testWeight():
    a = inputArg(incidentLight='average')
    a.meritvalueCompare([['incident', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2',
                          'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
                          'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2',
                          'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
                          'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2',
                          'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1',
                          'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2',
                          'material1', 'material2', 'emergent'],
                         [141.69999999999925, 83.19999999999997, 116.79999999999947, 78.09999999999948,
                          115.39999999999968, 75.59999999999972, 119.19999999999945, 79.69999999999948,
                          133.09999999999945, 89.49999999999942, 138.1999999999991, 90.19999999999935,
                          124.39999999999976, 83.49999999999966, 110.8, 71.39999999999999, 108.79999999999995,
                          70.69999999999993, 106.69999999999982, 69.49999999999983, 108.79999999999988,
                          69.59999999999995, 121.79999999999987, 77.79999999999995, 128.2, 82.79999999999997,
                          114.89999999999986, 74.59999999999987, 120.29999999999998, 77.49999999999999,
                          123.19999999999996, 79.49999999999996, 111.89999999999986, 72.89999999999986,
                          107.39999999999999, 69.19999999999999, 107.39999999999999, 69.19999999999999,
                          104.99999999999999, 67.69999999999999, 109.39999999999999, 70.49999999999999,
                          109.19999999999997, 72.89999999999984, 126.59999999999953, 93.39999999999903,
                          154.59999999999846, 83.29999999999993, 140.59999999999948, 97.69999999999925]])


def testCoupling():
    a = inputArg(incidentLight='average')
    a.recipeGenerator_pureCoupling_test(layer=50)


# testCoupling()

# testGA()

def testCoupling():
    a = inputArg(incidentLight='average')
    a.recipeGenerator_pureCoupling_test(layer=50)

def generateFrame():
    '''
    generage 2-material combo thin film stacks
    :return:
    '''
    # a = inputArg(incidentLight='average')
    # a.recipeGenerator_geneticAlgorithm(genNo=200, timeLimit=None, layerNo=28, material1='SiO2.txt', material2='Ta2O5.txt' )
    # a = inputArg(incidentLight='average')
    # a.recipeGenerator_geneticAlgorithm(genNo=300, timeLimit=None, layerNo=24, material1='MgF2.txt', material2='ITO.txt')
    a = inputArg(incidentLight='average')
    a.recipeGenerator_geneticAlgorithm(genNo=100, timeLimit=None, layerNo=28, material1='MgF2.txt', material2='Ta2O5.txt' )



if __name__ == "__main__":
    # while True:
    #     generateFrame()
    # testPlot()
    # STRUCT = getDatafromSQL()
    # multiOptimization(STRUCT)

    a = inputArg(incidentLight='average')
    a.discrepancy_optimize([['incident', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material3', 'material1', 'material2', 'material1', 'material3', 'material1', 'material3', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material1', 'material3', 'material3', 'material1', 'material2', 'material1', 'material3', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material3', 'material1', 'material2', 'material1', 'material3', 'material1', 'fixed_layer', 'emergent'], [71.23241348531901, 134.87037335685656, 83.79495137326374, 170.87622562681645, 82.4407720772821, 101.14094153682973, 70.3217100247318, 113.12918829113056, 64.62940662364954, 80.07039770974643, 90.97039770974605, 95.07039770974575, 67.78893764992455, 132.57627433259518, 80.49395290692316, 82.39395290692292, 81.68805193118438, 60.988051931184536, 56.68593078825522, 105.27629868548519, 76.14077207728212, 113.34094153682969, 51.63710322256727, 82.31160712836117, 74.54612380757574, 118.01153406969252, 72.82706175502528, 85.89978082399415, 59.300000000000004, 57.799999999999926, 81.02336037406032, 89.66011560693617, 85.43542034698812, 106.66473988439324, 98.0586201111574, 100.40115606936429, 84.87354445208922, 128.9254335260118, 65.91335143276866, 106.40115606936376, 68.23776521561264, 94.31387283237012, 69.72706175502543, 108.04913294797689, 60.2103445710992, 93.81791907514429, 67.36217899845671, 104.02658959537588, 66.74311694590625, 108.0462427745664, 58.31034457109917, 157.61791907514237, 33.21745939832121, 82.75317919075178, 76.57588932071329, 111.27456647398827, 67.97039770974682, 119.79826589595315, 995.7]])

    #

#)  # SiO2, Ta2O5
    # a.couple2structure()
    # temp2 is the recipe generated based on the merit function at mid June
    # temp2 = [['incident', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material2', 'material3', 'material4', 'material3', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'material4', 'material1', 'emergent'], [82.74913066924522, 120.41150971680295, 69.13241348531902, 101.07037335685644, 72.72171002473176, 105.52918829113068, 68.80264797218142, 100.11743504543166, 66.01335143276866, 96.05862011115741, 72.25682726816297, 105.05271913541829, 62.29428938021831, 90.6468668654584, 68.33776521561262, 99.4409658897193, 63.2240548933559, 91.99980517688316, 66.94311694590624, 97.41155842258216, 64.61870316306228, 94.02921264402028, 73.45147553786936, 106.88212660255543, 176.0, 125.0, 102.43492580946179, 141.85491329479666, 91.08083658083858, 135.62947976878502, 101.65756519793892, 125.34913294797605, 96.05033473232453, 128.97745664739858, 110.52706334942464, 139.9971098265884, 84.52706334942611, 118.49710982658961, 72.15724920072961, 101.15606936416185, 81.43460981225199, 114.16184971098266, 67.51856889496841, 94.65317919075143, 84.01165442656377, 117.87456647398844, 66.5877510492437, 93.20809248554914, 91.22737934663672, 127.89017341040463]]

    # a.plotStructure(temp, waveStep=1)
#     a.plotStructure([['incident', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'material2', 'material1', 'emergent'], [81.8527678411975, 81.8527678411975, 76.24077207728212, 110.94094153682968, 75.76454543978613, 75.76454543978613, 61.84907074348253, 81.17629868548514, 76.24077207728212, 110.94094153682968, 55.78593078825521, 81.17629868548514, 70.6621789984566, 102.82331166828118, 66.01335143276866, 96.05862011115741, 66.94311694590624, 97.41155842258216, 78.56518586012606, 114.32328731539155, 77.63542034698851, 112.97034900396683, 73.91635829443814, 107.5585957582678]]
# , waveStep=10, minWave=400, maxWave=700, material1='SiO2.txt', material2='Ta2O5.txt')
    # 7/6

