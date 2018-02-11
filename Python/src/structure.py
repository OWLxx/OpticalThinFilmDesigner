import re
import numpy as np
import pandas as pd
import os
from src import transfermatrix as tfm
from lmfit import parameter
from collections import OrderedDict
import cmath
import tensorflow as tf
import numba
import time

class Layer(object):
    def __init__(self, material, thickness, layerNumber):
        self.mat = material
        self.no = layerNumber
        self.thickness = thickness
        self.coherent = True
        if thickness >= 100000:
            self.coherent = False


class Limitations(object):
    def __init__(self, constriant=None, material=None, defaultStructure = None, meritFunction=None, padding=False):
        if not constriant:
            self.constraint = {'minWave': 400,
                                      'maxWave': 700,
                                      'waveStep': 10,
                                      'angle':[0, 15, 30, 40, 50],
                                      'target':560
                                      }
        else:
            self.constraint = constriant
        if not material:
            material = ['air.txt','AlSiO2.txt', 'ITOa.txt', 'Willow.txt']
        self.material = material
        self.idxdic = {}
        for m in set(material):
            self.idxdic[m] = readFile(m, self.constraint)
        self.indices = []
        if defaultStructure:
            self.matArray = defaultStructure
            for m in defaultStructure:
                self.indices.append(self.idxdic[m])
        self.fmv = meritFunction
        self.padding = padding





class Struct(object):                # used for gradient related calculation
    def __init__(self, layers, limitations):
        '''
        Initialize struct object, which is composed by a list of layers
        :param layers: List[List, List]  corresponds to material and thickness
        '''
        self.SystemMatrixS = None
        self.SystemMatrixP = None
        self.derivative = None
        self.hessian = None
        self.meritValue = None
        self.R = None
        self.RS = None
        self.RP = None
        self.T = None
        self.limitations = limitations
        self.constraint = limitations.constraint

        minw = self.constraint['minWave']
        maxw = self.constraint['maxWave']
        stepw = self.constraint['waveStep']
        tarw = self.constraint['target']
        self.waves = np.arange(minw, maxw+stepw, stepw)

        self.angles = self.constraint['angle']
        self.idxdic = limitations.idxdic                            # indices of materials
        self.idx = limitations.indices
        if not self.idx:
            for m in layers[0]:
                self.idx.append(self.idxdic[m])
        self.rawStruct = layers
        # Generate Layer object
        self.layers = []                                                           # this is used in transfer matrix
        for i in range(len(layers[1])):
            curMat = layers[0][i+1]
            curthick = layers[1][i]
            no = i
            self.layers.append(Layer(curMat, curthick, no))
        self.initialize('new')


        # Local Search - Genetic algorithm will reconstruct Struct, instead, local search will update local search
    def initialize(self, type='new'):
        if type=='new':
            cur = tfm.transferMatrix(self)
        elif type=='first_order':
            cur = tfm.transferMatrix(self)
            cur.first_order()
            print(self.derivative)


    def meritValue(self, R, T):
        return self.limitations.meritFunction2(R,T)






class QuickStruct(object):   # quick merit value, for dichronic coating
    def __init__(self, limits, thickness, phase=True):
        self.constraint = limits.constraint

        minw = limits.constraint['minWave']
        maxw = limits.constraint['maxWave']
        stepw = limits.constraint['waveStep']
        tarw = limits.constraint['target']
        self.angle = limits.constraint['angle']
        self.indices = limits.indices
        self.idxdic = limits.idxdic
        self.waves = np.arange(minw, maxw + stepw, stepw)

        targetIndex = int((tarw - minw) / stepw)
        # print(self.indices)
        if phase:        # if true, the input is phase thickness ,with length = layerNumber/2
            tck = []
            for i in range(len(thickness)):
                curIndex = [self.indices[i*2+1][targetIndex],  self.indices[i*2+2][targetIndex]]
                curPhaseThickness = thickness[i]
                for refractiveIndex in curIndex:
                    realThickness = np.deg2rad(curPhaseThickness) * tarw / 2 / np.pi / refractiveIndex
                    tck.append(np.abs(realThickness))
            self.thickness = tck
        else:
            self.thickness = thickness
        if limits.padding==True:
            self.thickness = np.array(list(self.thickness) + [1000.0])

        m = len(self.waves)  # number of wavelength
        n = len(self.angle)
        self.m = m
        self.n = n
        self.R = np.array([[0.] * n for i in range(m)])
        angleIndex = OrderedDict()
        self.angleIndex = {j: i for i, j in enumerate(self.angle)}

        for ang in self.angle:    # different angle
            i_angle = self.angleIndex[ang]
            for i_wave in range(len(self.waves)):  # different waves
                TSmatrix, TPmatrix, theta_list = self.tmatrix_method(i_wave,ang , self.indices)
                P = self.pmatrix_method(i_wave, self.waves[i_wave], self.indices,self.thickness, theta_list, i_angle)
                System_matrix = self.system_matrix(TSmatrix, TPmatrix, P, i_wave, i_angle)

                r, _, _, _ = self.rta_calculation(System_matrix)
                self.R[i_wave][i_angle] = r
        self.MV = limits.fmv(self.R)





    def tmatrix_method(self, i_wave, ang, nkindex):
        #input arg:  index of wave,     current angle,     material index (n, k)
        #output arg:  T matrix for s polarization, T matrix for p polarization, angles in different layer
        length = len(nkindex)
        TS = []
        TP = []
        layer_num = 0
        thetai = np.deg2rad(ang)
        thetaList = []
        while layer_num < length - 1:
            # print 'indexlist', self.indexlist
            # print 'layernumber', layer_num, 'count', count
            n1 = nkindex[layer_num][i_wave]
            n2 = nkindex[layer_num + 1][i_wave]
            thetat = np.conj(cmath.asin(n1 / n2 * np.sin(thetai)))  # Snell's law
            thetaList.append(thetat)  # for theta in P matrix
            ts = 2 * n1 * np.conj(cmath.cos(thetai)) / \
                 (n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            tp = 2 * n1 * np.conj(cmath.cos(thetai)) / \
                 (n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            rs = (n1 * np.conj(cmath.cos(thetai)) - n2 * np.conj(cmath.cos(thetat))) / \
                 (n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            rp = (n2 * np.conj(cmath.cos(thetai)) - n1 * np.conj(cmath.cos(thetat))) / \
                 (n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            thetai = thetat  # update theta for next interface
            TS.append([[1 / ts, rs / ts], [rs / ts, 1 / ts]])
            TP.append([[1 / tp, rp / tp], [rp / tp, 1 / tp]])
            layer_num += 1
        return TS, TP, thetaList

    def pmatrix_method(self, i_wave, wave, nkindex,thickness, theta_list, i_angle, mark=True):
        length = len(nkindex)
        P = []
        layer_num = 1  # skip incident
        while layer_num < length - 1:  # skip emergent
            n = nkindex[layer_num][i_wave]
            tck = thickness[layer_num - 1]
            theta = theta_list[layer_num - 1]
            p = [[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
                  [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]]
            P.append(p)
            layer_num += 1
        return P


    def system_matrix(self, TS, TP, P, i_wave, i_angle, mark=True):
        ss = self.matrix_multiplicate(TS, P, i_wave, i_angle, type='S', mark=mark)
        sp= self.matrix_multiplicate(TP, P, i_wave, i_angle, type='P', mark=mark)

        return (ss, sp)


    def matrix_multiplicate(self, T, P, i_wave, i_angle, type=None, mark=True):
        # helper function of system_matrix
        # S is forward transfer matrix
        # SB is backward transfer matrix
        count = 0
        S = np.identity(2)
        while count < len(T):
            T[count] = np.array(T[count]).reshape([2,2])
            # print(S, T)
            S = S.dot(T[count])
            if count < len(T) - 1:
                P[count] = np.array(P[count]).reshape([2,2])
                S = S.dot(P[count])
            count += 1

        return S

    def rta_calculation(self, system_matrix):
        ss, sp = system_matrix    # forward calculation
        RS = np.absolute(ss[1][0] / ss[0][0]) ** 2
        RP = np.absolute(sp[1][0] / sp[0][0]) ** 2
        TS = 1 / np.absolute(ss[0][0]) ** 2
        TP = np.absolute(np.linalg.det(sp) / sp[0][0]) ** 2
        if RS > 1: RS = 1
        if RP > 1: RP = 1
        R = (RS + RP) / 2.
        T = (TS + TP) / 2.
        return R, T, RS, RP



def readFile(filename, constrains):
    cur_path = os.path.dirname(__file__)
    filepath = os.path.relpath('..\\indexfile\\{}'.format(filename), cur_path)
    # filepath = "./indexfile/" + filename
    f = open(filepath, 'r')
    dataInFile = {}
    for line in f.readlines():
        if re.match('[0-9.]{3,15}\t[0-9.]{1,15}\t[.-z]{1,15}', line) is not None:
            curWave, curn, curk = line.split('\t')
            dataInFile[float(curWave)] = [float(curn), float(curk)]
        elif re.match('[0-9.]{3,15}\t[0-9.]{1,15}', line) is not None:        # no k values in the index file
            curWave, curn = line.split('\t')
            dataInFile[float(curWave)] = [float(curn), 0]
    targetWave = np.arange(constrains['minWave'], constrains['maxWave']+constrains['waveStep'], constrains['waveStep'])
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
            if np.absolute(dataInFile[fileWave[count]][1] ) < 0.01:
                output.append(np.absolute(complex(*dataInFile[fileWave[count]])))
            else:
                output.append(complex(*dataInFile[fileWave[count]]))
        else:
            # print(targetWave[i], preWave, preN,dataInFile[fileWave[count]] )
            ratio = (targetWave[i] - preWave) / (fileWave[count] - preWave)  # pickup linear point
            ntemp = (1-ratio)*preN[0] + ratio*dataInFile[fileWave[count]][0]
            ktemp = (1-ratio)*preN[1] + ratio*dataInFile[fileWave[count]][1]
            if np.absolute(ktemp)<0.01:
                 ktemp = 0
            output.append(complex(ntemp, ktemp))
    return output

class StructJacobian(object):   # quick merit value, for dichronic coating
    def __init__(self, limits, thickness):
        self.constraint = limits.constraint
        minw = limits.constraint['minWave']
        maxw = limits.constraint['maxWave']
        stepw = limits.constraint['waveStep']
        tarw = limits.constraint['target']
        self.angle = limits.constraint['angle']
        self.indices = limits.indices
        self.idxdic = limits.idxdic
        self.waves = np.arange(minw, maxw + stepw, stepw)
        self.thickness = thickness
        startTime = time.time()
        targetIndex = int((tarw - minw) / stepw)
        m = len(self.waves)  # number of wavelength
        n = len(self.angle)
        self.m = m
        self.n = n
        self.SS = [[None]*n for _ in range(m)]        # each is a 2by2 matrix
        self.SSpre = [[None]*n for _ in range(m)]     # each is a list of 2by2 matrix
        self.SSafter = [[None]*n for _ in range(m)]   # each is a list of 2by2 matrix
        self.SP = [[None] * n for _ in range(m)]  # each is a 2by2 matrix
        self.SPpre = [[None] * n for _ in range(m)]  # each is a list of 2by2 matrix
        self.SPafter = [[None] * n for _ in range(m)]  # each is a list of 2by2 matrix
        self.P = [[None]*n for _ in range(m)]        # each is a list of 2by2 matrix

        self.R = np.array([[0.] * n for i in range(m)])
        angleIndex = OrderedDict()
        self.angleIndex = {j: i for i, j in enumerate(self.angle)}

        for ang in self.angle:    # different angle
            i_angle = self.angleIndex[ang]
            for i_wave in range(len(self.waves)):  # different waves
                TSmatrix, TPmatrix, theta_list = self.tmatrix_method(i_wave,ang , self.indices)
                P = self.pmatrix_method(i_wave, self.waves[i_wave], self.indices,self.thickness, theta_list, i_angle)
                System_matrix, sspre, sppre = self.system_matrix(TSmatrix, TPmatrix, P, i_wave, i_angle)
                r, _, _, _ = self.rta_calculation(System_matrix)
                self.R[i_wave][i_angle] = r
                self.P[i_wave][i_angle] = P
                self.SS[i_wave][i_angle], self.SP[i_wave][i_angle] = System_matrix
                self.SSpre[i_wave][i_angle] = sspre[:-1]
                self.SPpre[i_wave][i_angle] = sppre[:-1]
                self.SSafter[i_wave][i_angle] = []
                self.SPafter[i_wave][i_angle] = []
                for i_s in range(len(sspre)-1):
                    # print('#', self.SS[i_wave][i_angle], self.SP[i_wave][i_angle])
                    try:
                        self.SSafter[i_wave][i_angle].append(np.linalg.inv(self.SSpre[i_wave][i_angle][i_s]).dot(np.linalg.inv(self.P[i_wave][i_angle][i_s])).dot(self.SS[i_wave][i_angle]))
                        # print(i_s)
                    except:
                        print(self.SSpre[i_wave][i_angle][i_s])
                        print(self.P[i_wave][i_angle][i_s])
                        print(self.SS[i_wave][i_angle])
                        print(list(self.thickness))
                        print(i_wave, i_angle, i_s)
                        print('#################SINGULAR####################')
                        self.SSafter[i_wave][i_angle].append(np.identity(2))
                    self.SPafter[i_wave][i_angle].append(np.linalg.inv(self.SPpre[i_wave][i_angle][i_s]).dot(np.linalg.inv(self.P[i_wave][i_angle][i_s])).dot(self.SP[i_wave][i_angle]))

        self.Jacobian = []
        self.MV = limits.fmv(self.R)
        # calculate gradient
        layers = len(self.SSpre[0][0])
        for l in range(layers):
            Rplus = np.array([[0.] * n for i in range(m)])
            Rminus = np.array([[0.] * n for i in range(m)])
            for ang in self.angle:  # different angle
                i_angle = self.angleIndex[ang]
                for i_wave in range(len(self.waves)):  # different waves
                    TSmatrix, TPmatrix, theta_list = self.tmatrix_method(i_wave, ang, self.indices)
                    Pplus, Pminus = self.dual_pmatrix_method(i_wave, self.waves[i_wave], self.indices, self.thickness, theta_list,
                                            i_angle, l)

                    System_plus = [np.array(Pplus).dot(self.SSpre[i_wave][i_angle][l]).dot(self.SSafter[i_wave][i_angle][l]),
                                   np.array(Pplus).dot(self.SPpre[i_wave][i_angle][l]).dot(self.SPafter[i_wave][i_angle][l])]
                    # print(self.SP[i_wave][i_angle], System_plus[1])     # IT MATCHES NOW
                    # print('##############')
                    System_minus = [np.array(Pminus).dot(self.SSpre[i_wave][i_angle][l]).dot(self.SSafter[i_wave][i_angle][l]),
                                    np.array(Pminus).dot(self.SPpre[i_wave][i_angle][l]).dot(self.SPafter[i_wave][i_angle][l])]

                    rplus, _, _, _ = self.rta_calculation(System_plus)
                    rminus, _, _, _ = self.rta_calculation(System_minus)
                    Rplus[i_wave][i_angle] = rplus
                    Rminus[i_wave][i_angle] = rminus
            mvp = limits.fmv(Rplus)
            mvm = limits.fmv(Rminus)
            if mvp>self.MV>mvm:
                self.Jacobian.append(mvm - self.MV)   # thickness decrease
            elif mvm>self.MV>mvp:
                self.Jacobian.append(self.MV-mvp)    # thickness increase
            elif self.MV<=mvm and self.MV<=mvp:       # already at local minimum
                self.Jacobian.append(0)
            else:
                self.Jacobian.append(mvm-mvp)         # > 0,thickness increase   <0 decrase
        print('Run time', time.time() - startTime)





    def tmatrix_method(self, i_wave, ang, nkindex):
        #input arg:  index of wave,     current angle,     material index (n, k)
        #output arg:  T matrix for s polarization, T matrix for p polarization, angles in different layer
        length = len(nkindex)
        TS = []
        TP = []
        layer_num = 0
        thetai = np.deg2rad(ang)
        thetaList = []
        while layer_num < length - 1:
            # print 'indexlist', self.indexlist
            # print 'layernumber', layer_num, 'count', count
            n1 = nkindex[layer_num][i_wave]
            n2 = nkindex[layer_num + 1][i_wave]
            thetat = np.conj(cmath.asin(n1 / n2 * np.sin(thetai)))  # Snell's law
            thetaList.append(thetat)  # for theta in P matrix
            ts = 2 * n1 * np.conj(cmath.cos(thetai)) / \
                 (n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            tp = 2 * n1 * np.conj(cmath.cos(thetai)) / \
                 (n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            rs = (n1 * np.conj(cmath.cos(thetai)) - n2 * np.conj(cmath.cos(thetat))) / \
                 (n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            rp = (n2 * np.conj(cmath.cos(thetai)) - n1 * np.conj(cmath.cos(thetat))) / \
                 (n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            thetai = thetat  # update theta for next interface
            TS.append([[1 / ts, rs / ts], [rs / ts, 1 / ts]])
            TP.append([[1 / tp, rp / tp], [rp / tp, 1 / tp]])
            layer_num += 1
        return TS, TP, thetaList

    def pmatrix_method(self, i_wave, wave, nkindex,thickness, theta_list, i_angle, mark=True):
        length = len(nkindex)
        P = []
        layer_num = 1  # skip incident
        while layer_num < length - 1:  # skip emergent
            n = nkindex[layer_num][i_wave]
            tck = thickness[layer_num - 1]
            theta = theta_list[layer_num - 1]
            p = [[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
                  [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]]
            P.append(p)
            layer_num += 1
        return P


    def system_matrix(self, TS, TP, P, i_wave, i_angle, mark=True):
        ss, spre = self.matrix_multiplicate(TS, P, i_wave, i_angle, type='S', mark=mark)
        sp, sppre= self.matrix_multiplicate(TP, P, i_wave, i_angle, type='P', mark=mark)
        return (ss, sp), spre, sppre


    def matrix_multiplicate(self, T, P, i_wave, i_angle, type=None, mark=None):
        # helper function of system_matrix
        # S is forward transfer matrix
        # SB is backward transfer matrix
        count = 0
        Spre = []
        S = np.identity(2)
        while count < len(T):
            T[count] = np.array(T[count]).reshape([2,2])
            # print(S, T)
            S = S.dot(T[count])
            Spre.append(S)
            if count < len(T) - 1:
                P[count] = np.array(P[count]).reshape([2,2])
                S = S.dot(P[count])
            count += 1
        return S, Spre

    def rta_calculation(self, system_matrix):
        ss, sp = system_matrix    # forward calculation
        RS = np.absolute(ss[1][0] / ss[0][0]) ** 2
        RP = np.absolute(sp[1][0] / sp[0][0]) ** 2
        TS = 1 / np.absolute(ss[0][0]) ** 2
        TP = np.absolute(np.linalg.det(sp) / sp[0][0]) ** 2
        if RS > 1: RS = 1
        if RP > 1: RP = 1
        R = (RS + RP) / 2.
        T = (TS + TP) / 2.
        return R, T, RS, RP

    def dual_pmatrix_method(self, i_wave, wave, nkindex,thickness, theta_list, i_angle, layer_num):
        length = len(nkindex)
        layer_num += 1          # fixed the incident layer
        n = nkindex[layer_num][i_wave]
        tck = thickness[layer_num - 1] + 0.3
        theta = theta_list[layer_num - 1]
        p1 = [[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
              [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]]
        tck = thickness[layer_num - 1] - 0.3
        p2 = [[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
              [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]]

        return np.array(p1), np.array(p2)

class PlotStruct(object):   # quick merit value, for dichronic coating
    def __init__(self, limits, thickness, phase=True):
        self.constraint = limits.constraint

        minw = limits.constraint['minWave']
        maxw = limits.constraint['maxWave']
        stepw = limits.constraint['waveStep']
        tarw = limits.constraint['target']
        self.angle = limits.constraint['angle']
        self.indices = limits.indices
        self.idxdic = limits.idxdic
        self.waves = np.arange(minw, maxw + stepw, stepw)

        targetIndex = int((tarw - minw) / stepw)
        if phase:        # if true, the input is phase thickness ,with length = layerNumber/2
            tck = []
            for i in range(len(thickness)):
                curIndex = [self.indices[i*2+1][targetIndex],  self.indices[i*2+2][targetIndex]]
                curPhaseThickness = thickness[i]
                for refractiveIndex in curIndex:
                    realThickness = np.deg2rad(curPhaseThickness) * tarw / 2 / np.pi / refractiveIndex
                    tck.append(np.abs(realThickness))
            self.thickness = tck
        else:
            self.thickness = thickness
        if limits.padding==True:
            self.thickness = np.array(list(self.thickness) + [1000.0])

        m = len(self.waves)  # number of wavelength
        n = len(self.angle)
        self.m = m
        self.n = n
        self.R = np.array([[0.] * n for i in range(m)])
        self.RS = np.array([[0.] * n for i in range(m)])
        self.RP = np.array([[0.] * n for i in range(m)])
        self.T = np.array([[0.] * n for i in range(m)])
        angleIndex = OrderedDict()
        self.angleIndex = {j: i for i, j in enumerate(self.angle)}

        for ang in self.angle:    # different angle
            i_angle = self.angleIndex[ang]
            for i_wave in range(len(self.waves)):  # different waves
                TSmatrix, TPmatrix, theta_list = self.tmatrix_method(i_wave,ang , self.indices)
                P = self.pmatrix_method(i_wave, self.waves[i_wave], self.indices,self.thickness, theta_list, i_angle)
                System_matrix = self.system_matrix(TSmatrix, TPmatrix, P, i_wave, i_angle)
                r, t, rs, rp = self.rta_calculation(System_matrix)
                self.R[i_wave][i_angle] = r
                self.T[i_wave][i_angle] = t
                self.RS[i_wave][i_angle] = rs
                self.RP[i_wave][i_angle] = rp
        self.MV = limits.fmv(self.R)





    def tmatrix_method(self, i_wave, ang, nkindex):
        #input arg:  index of wave,     current angle,     material index (n, k)
        #output arg:  T matrix for s polarization, T matrix for p polarization, angles in different layer
        length = len(nkindex)
        TS = []
        TP = []
        layer_num = 0
        thetai = np.deg2rad(ang)
        thetaList = []
        while layer_num < length - 1:
            # print 'indexlist', self.indexlist
            # print 'layernumber', layer_num, 'count', count
            n1 = nkindex[layer_num][i_wave]
            n2 = nkindex[layer_num + 1][i_wave]
            thetat = np.conj(cmath.asin(n1 / n2 * np.sin(thetai)))  # Snell's law
            thetaList.append(thetat)  # for theta in P matrix
            ts = 2 * n1 * np.conj(cmath.cos(thetai)) / \
                 (n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            tp = 2 * n1 * np.conj(cmath.cos(thetai)) / \
                 (n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            rs = (n1 * np.conj(cmath.cos(thetai)) - n2 * np.conj(cmath.cos(thetat))) / \
                 (n1 * np.conj(cmath.cos(thetai)) + n2 * np.conj(cmath.cos(thetat)))
            rp = (n2 * np.conj(cmath.cos(thetai)) - n1 * np.conj(cmath.cos(thetat))) / \
                 (n1 * np.conj(cmath.cos(thetat)) + n2 * np.conj(cmath.cos(thetai)))
            thetai = thetat  # update theta for next interface
            TS.append([[1 / ts, rs / ts], [rs / ts, 1 / ts]])
            TP.append([[1 / tp, rp / tp], [rp / tp, 1 / tp]])
            layer_num += 1
        return TS, TP, thetaList

    def pmatrix_method(self, i_wave, wave, nkindex,thickness, theta_list, i_angle, mark=True):
        length = len(nkindex)
        P = []
        layer_num = 1  # skip incident
        while layer_num < length - 1:  # skip emergent
            n = nkindex[layer_num][i_wave]
            tck = thickness[layer_num - 1]
            theta = theta_list[layer_num - 1]
            p = [[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
                  [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]]
            P.append(p)
            layer_num += 1
        return P


    def system_matrix(self, TS, TP, P, i_wave, i_angle, mark=True):
        ss = self.matrix_multiplicate(TS, P, i_wave, i_angle, type='S', mark=mark)
        sp= self.matrix_multiplicate(TP, P, i_wave, i_angle, type='P', mark=mark)

        return (ss, sp)


    def matrix_multiplicate(self, T, P, i_wave, i_angle, type=None, mark=True):
        # helper function of system_matrix
        # S is forward transfer matrix
        # SB is backward transfer matrix
        count = 0
        S = np.identity(2)
        while count < len(T):
            T[count] = np.array(T[count]).reshape([2,2])
            # print(S, T)
            S = S.dot(T[count])
            if count < len(T) - 1:
                P[count] = np.array(P[count]).reshape([2,2])
                S = S.dot(P[count])
            count += 1

        return S

    def rta_calculation(self, system_matrix):
        ss, sp = system_matrix    # forward calculation
        RS = np.absolute(ss[1][0] / ss[0][0]) ** 2
        RP = np.absolute(sp[1][0] / sp[0][0]) ** 2
        TS = 1 / np.absolute(ss[0][0]) ** 2
        TP = np.absolute(np.linalg.det(sp) / sp[0][0]) ** 2
        if RS > 1: RS = 1
        if RP > 1: RP = 1
        R = (RS + RP) / 2.
        T = (TS + TP) / 2.
        return R, T, RS, RP

