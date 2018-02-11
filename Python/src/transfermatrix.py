import numpy as np
import cmath
import pandas as pd
from collections import OrderedDict

class transferMatrix(object):
    def __init__(self, struct):
        self.struct = struct
        angle = struct.angles
        self.waveIndex = OrderedDict()
        self.waveIndex = {j:i for i,j in enumerate(struct.waves)}
        self.waves = struct.waves
        self.angleIndex = OrderedDict()
        self.angleIndex = {j:i for i,j in enumerate(angle)}
        m = len(struct.waves)     # number of wavelength
        n = len(angle)
        self.m = m
        self.n = n
        # print(m, n)
        self.struct.SystemMatrixS = [[0.] * n for i in range(m)]
        self.struct.SystemMatrixP = [[0.] * n for i in range(m)]
        self.struct.R = np.array([[0.] * n for i in range(m)])
        self.struct.T = np.array([[0.] * n for i in range(m)])
        self.struct.RS = np.array([[0.] * n for i in range(m)])
        self.struct.RP = np.array([[0.] * n for i in range(m)])
        self.epsilon = 1

        self.nkindex = struct.idx
        indexLookup = struct.idxdic
        for i, layer in enumerate(struct.layers):
            layer.SS_pre = [[0.] * n for i in range(m)]
            layer.SP_pre = [[0.] * n for i in range(m)]
            layer.P = [[0.] * n for i in range(m)]
            layer.SS_after = [[0.] * n for i in range(m)]
            layer.SP_after = [[0.] * n for i in range(m)]

        self.main()                                 # calculate RTA
        struct.meritFunction(self.struct.R, self.struct.T)
        l = self.struct.layers[0]

    def run(self, type):
        if type == 'new':
            self.main()
            self.struct.meritFunction(self.struct.R, self.struct.T)
        elif type == 'first_order':
            self.first_order()


    def main(self):
        # list index
        nkindex = self.nkindex
        thickness = [i.thickness for i in self.struct.layers]
        coherence = True
        if any(i>100000 for i in thickness):
            coherence = False
        angle = self.struct.constraint['angle']
        waves = self.waves

        for ang in angle:    # different angle
            i_angle = self.angleIndex[ang]
            for i_wave in range(len(waves)):  # different waves
                TSmatrix, TPmatrix, theta_list = self.tmatrix_method(i_wave,ang , nkindex)
                if coherence:
                    P = self.pmatrix_method(i_wave, waves[i_wave], nkindex,thickness, theta_list, i_angle)
                    System_matrix = self.system_matrix(TSmatrix, TPmatrix, P, i_wave, i_angle)
                    r, t, rs, rp = self.rta_calculation(System_matrix)
                else:
                    P = self.pmatrix_method_incoherent(i_wave, waves[i_wave], nkindex,thickness, theta_list, i_angle)
                    System_matrix = self.system_matrix_incoherent(TSmatrix, TPmatrix, P, i_wave, i_angle)
                    r, t, rs, rp = self.rta_calculation_incoherent(System_matrix)
                self.struct.R[i_wave][i_angle] = r
                self.struct.RS[i_wave][i_angle] = rs
                self.struct.RP[i_wave][i_angle] = rp
                self.struct.T[i_wave][i_angle] = t
        self.struct.meritValue = self.struct.meritFunction(self.struct.R, self.struct.T)


    def first_order(self):
        layers = self.struct.layers
        ret = [0] * len(layers)
        m, n = self.m, self.n
        for i, layer in enumerate(layers):
            P_cur = layer.P
            ss_pre = layer.SS_pre
            sp_pre = layer.SP_pre
            SS = self.struct.SystemMatrixS
            SP = self.struct.SystemMatrixP
            R_new_plus = np.array([[0] * n for i in range(m)])
            T_new_plus = np.array([[0] * n for i in range(m)])
            R_new_minus = np.array([[0] * n for i in range(m)])
            T_new_minus = np.array([[0] * n for i in range(m)])

            for i_wave in range(m):
                for i_angle in range(n):
                    p_cur = layer.P[i_wave][i_angle]
                    sss_pre = ss_pre[i_wave][i_angle]
                    ssp_pre = sp_pre[i_wave][i_angle]
                    ss = SS[i_wave][i_angle]
                    sp = SP[i_wave][i_angle]



                    p_plus, p_minus = self.quickPmatrix(layer, i_wave, i_angle)
                    sss_after = np.dot(np.dot(np.linalg.inv(p_cur), sss_pre), ss)
                    ssp_after = np.dot(np.dot(np.linalg.inv(p_cur), ssp_pre), sp)
                    layer.SS_after[i_wave][i_angle] = sss_after
                    layer.SP_after[i_wave][i_angle] = ssp_after

                    ss_new_plus = sss_pre * p_plus * sss_after
                    ss_new_minus = sss_pre * p_minus * sss_after
                    sp_new_plus = ssp_pre * p_plus * ssp_after
                    sp_new_minus = ssp_pre * p_minus * ssp_after

                    R_new_plus[i_wave][i_angle], T_new_plus[i_wave][i_angle],_, _ = \
                                                    self.rta_calculation([ss_new_plus, sp_new_plus])
                    R_new_minus[i_wave][i_angle], T_new_minus[i_wave][i_angle],_, _ = \
                                                    self.rta_calculation([ss_new_minus, sp_new_minus])
            mv1 = self.struct.meritFunction(R_new_plus, T_new_plus)
            mv2 = self.struct.meritFunction(R_new_minus, T_new_minus)
            ret[i] = (mv1-mv2) / (2*self.epsilon)
        self.struct.derivative = ret
        return ret

    def second_order(self):
        layers = self.struct.layers
        ret = np.array([[0] * len(layers) for i in range(len(layers))])
        m, n = self.m, self.n
        nkindex = self.nkindex
        angle = self.struct.constraint['angle']
        waves = self.waves
        for i, layer1 in enumerate(layers):
            for j, layer2 in enumerate(layers):
                thickness = [i.thickness for i in self.struct.layers]
                thickness_1 = thickness[:]
                thickness_2 = thickness[:]
                thickness_3 = thickness[:]
                thickness_4 = thickness[:]
                thickness_1[i] += self.epsilon
                thickness_1[j] += self.epsilon
                thickness_2[i] += self.epsilon
                thickness_2[j] -= self.epsilon
                thickness_3[i] -= self.epsilon
                thickness_3[j] += self.epsilon
                thickness_4[i] -= self.epsilon
                thickness_4[j] -= self.epsilon
                thickness_temp = [thickness_1, thickness_2, thickness_3, thickness_4]
                R = np.zeros((4, m, n))
                T = np.zeros((4, m, n))
                for k in range(4):              # 4 different thickness
                    thickness =thickness_temp[k]
                    for ang in angle:
                        i_angle = self.angleIndex[ang]
                        for i_wave in range(len(waves)):  # different waves

                            TSmatrix, TPmatrix, theta_list = self.tmatrix_method(i_wave,ang , nkindex)
                            P = self.pmatrix_method(i_wave, waves[i_wave], nkindex,thickness, theta_list, i_angle, mark=False)
                            System_matrix = self.system_matrix(TSmatrix, TPmatrix, P, i_wave, i_angle, mark=False)
                            R[k][i_wave][i_angle], T[k][i_wave][i_angle], _, _ = self.rta_calculation(System_matrix)
                mv1 = self.struct.meritFunction(R[0, :, :], T[0, :, :])
                mv2 = self.struct.meritFunction(R[1, :, :], T[1, :, :])
                mv3 = self.struct.meritFunction(R[2, :, :], T[2, :, :])
                mv4 = self.struct.meritFunction(R[3, :, :], T[3, :, :])
                ret[i,j] = ((mv1 - mv2) / (2 * self.epsilon) - (mv3 - mv4) / (2 * self.epsilon)) / (2 * self.epsilon)
        self.struct.hessian = ret







    def quickPmatrix(self, layer, i_wave, i_angle):
        n = self.struct.indices[layer.mat][i_wave]                  # n is refractive index here
        theta = np.deg2rad(self.struct.constraint['angle'][i_angle])
        wave = self.waves[i_wave]
        tck = layer.thickness
        tck += self.epsilon
        p1 =  np.array([[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
                  [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]])
        tck -= 2 * self.epsilon
        p2 = np.array([[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
                  [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]])
        return p1, p2





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
            # print(nkindex)
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
            if mark:
                self.struct.layers[layer_num-1].P[i_wave][i_angle] = p
            P.append(p)
            layer_num += 1
        return P

    def pmatrix_method_incoherent(self, i_wave, wave, nkindex,thickness, theta_list, i_angle, mark=True):
        length = len(nkindex)
        P = [[], [], []]
        layer_num = 1  # skip incident
        while layer_num < length - 1:  # skip emergent
            n = nkindex[layer_num][i_wave]
            tck = thickness[layer_num - 1]
            theta = theta_list[layer_num - 1]
            if tck > 100000:
                p1 = [[np.exp(-1j * 0 * np.pi), 0],
                      [0, np.exp(1j * 0 * np.pi)]]
                p2 = [[np.exp(-1j * 2/3 * np.pi), 0],
                      [0, np.exp(1j * 2/3 * np.pi)]]
                p3 = [[np.exp(-1j * 4/3 * np.pi), 0],
                      [0, np.exp(1j * 4/3 * np.pi)]]
            else:
                p1 = [[np.exp(-2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave), 0],
                  [0, np.exp(2 * np.pi * n * tck * 1j * cmath.cos(theta) / wave)]]
                p2 = p1[:]
                p3 = p1[:]
            P[0].append(p1)
            P[1].append(p2)
            P[2].append(p3)
            layer_num += 1
        return P

    def system_matrix(self, TS, TP, P, i_wave, i_angle, mark=True):
        ss = self.matrix_multiplicate(TS, P, i_wave, i_angle, type='S', mark=mark)
        sp= self.matrix_multiplicate(TP, P, i_wave, i_angle, type='P', mark=mark)
        if mark:
            self.struct.SystemMatrixS[i_wave][i_angle] = ss
            self.struct.SystemMatrixP[i_wave][i_angle] = sp
        return (ss, sp)

    def system_matrix_incoherent(self, TS, TP, P, i_wave, i_angle, mark=True):
        p1, p2, p3 = P
        ss1 = self.matrix_multiplicate(TS, p1, i_wave, i_angle, type='S', mark=mark)
        ss2 = self.matrix_multiplicate(TS, p2, i_wave, i_angle, type='S', mark=mark)
        ss3 = self.matrix_multiplicate(TS, p3, i_wave, i_angle, type='S', mark=mark)
        sp1 = self.matrix_multiplicate(TP, p1, i_wave, i_angle, type='P', mark=mark)
        sp2 = self.matrix_multiplicate(TP, p2, i_wave, i_angle, type='P', mark=mark)
        sp3 = self.matrix_multiplicate(TP, p3, i_wave, i_angle, type='P', mark=mark)
        ss = [ss1, ss2, ss3]
        sp = [sp1, sp2, sp3]
        if mark:
            self.struct.SystemMatrixS[i_wave][i_angle] = ss
            self.struct.SystemMatrixP[i_wave][i_angle] = sp
        return (ss, sp)

    def matrix_multiplicate(self, T, P, i_wave, i_angle, type=None, mark=True):
        # helper function of system_matrix
        # S is forward transfer matrix
        # SB is backward transfer matrix
        count = 0
        S = np.identity(2)
        while count < len(T):
            T[count] = np.array(T[count])
            T[count].reshape(2, 2)
            S = np.dot(S, T[count])
            if mark and count<len(T)-1:
                if type=='S':
                    self.struct.layers[count].SS_pre[i_wave][i_angle] = S
                elif type=='P':
                    self.struct.layers[count].SP_pre[i_wave][i_angle] = S
            if count < len(T) - 1:
                P[count] = np.array(P[count])
                P[count].reshape(2, 2)
                S = np.dot(S, P[count])
            count += 1
        return S

    def rta_calculation(self, system_matrix):
        ss, sp = system_matrix    # forward calculation
        # ssb = np.linalg.inv(ss)   # backward calculation
        # spb = np.linalg.inv(sp)

        RS = np.absolute(ss[1][0] / ss[0][0]) ** 2
        RP = np.absolute(sp[1][0] / sp[0][0]) ** 2
        # RSB = np.absolute(ssb[1][0] / ssb[0][0]) ** 2
        # RPB = np.absolute(spb[1][0] / spb[0][0]) ** 2

        TS = 1 / np.absolute(ss[0][0]) ** 2
        TP = np.absolute(np.linalg.det(sp) / sp[0][0]) ** 2
        # TSB = 1 / np.absolute(ssb[0][0]) ** 2
        # TPB = np.absolute(np.linalg.det(spb) / spb[0][0]) ** 2
        if RS > 1: RS = 1
        if RP > 1: RP = 1
        # if RSB > 1: RSB = 1
        # if RPB > 1: RPB = 1
        R = (RS + RP) / 2.
        # RB = (RSB + RPB) / 2.
        T = (TS + TP) / 2.
        # TB = (TSB + TPB) / 2.
        # A = 1 - R - T
        return R, T, RS, RP

    def rta_calculation_incoherent(self, system_matrix):
        ss, sp = system_matrix    # forward calculation
        ss1, ss2, ss3 = ss
        sp1, sp2, sp3 = sp

        RS1 = np.absolute(ss1[1][0] / ss1[0][0]) ** 2
        RS2 = np.absolute(ss2[1][0] / ss2[0][0]) ** 2
        RS3 = np.absolute(ss3[1][0] / ss3[0][0]) ** 2
        RP1 = np.absolute(sp1[1][0] / sp1[0][0]) ** 2
        RP2 = np.absolute(sp2[1][0] / sp2[0][0]) ** 2
        RP3 = np.absolute(sp3[1][0] / sp3[0][0]) ** 2

        TS1 = 1 / np.absolute(ss1[0][0]) ** 2
        TS2 = 1 / np.absolute(ss2[0][0]) ** 2
        TS3 = 1 / np.absolute(ss3[0][0]) ** 2
        TP1 = np.absolute(np.linalg.det(sp1) / sp1[0][0]) ** 2
        TP2 = np.absolute(np.linalg.det(sp2) / sp2[0][0]) ** 2
        TP3 = np.absolute(np.linalg.det(sp3) / sp3[0][0]) ** 2

        RS = (RS1 + RS2 + RS3) / 3
        RP = (RP1 + RP2 + RP3) / 3
        TS = (TS1 + TS2 + TS3) / 3
        TP = (TP1 + TP2 + TP3) / 3

        R = (RS + RP) / 2.
        T = (TS + TP) / 2.

        return R, T, RS, RP

