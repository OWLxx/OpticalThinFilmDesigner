import numpy as np
import copy
from scipy.optimize import curve_fit
from lmfit import Parameters, minimize, fit_report
from src import structure
import sqlite3
import time

def curveFitting_scipy( y_data, struct, lowerbound, upperbound, method):
    # initial thickness is included in 
    waves = struct.waves
    def residual(x, l1 ,l2 , l3, l4, l5):
        # x is wavelength
        tempstruct = copy.deepcopy(struct)
        tempstruct.waves = x
        # print(tempstruct.waves)
        print(l1, l2, l3, l4, l5)
        for i, t in enumerate([l1, l2, l3, l4, l5]):
            tempstruct.layers[i].thickness = t
        tempstruct.initialize()
        return tempstruct.R[0, 0]
    popt, pcov = curve_fit(residual, waves, y_data, bounds=(lowerbound, upperbound), method=method)
    print('Final Structure: ', popt)
    return popt

def curveFitting_lmfit(y_data, struct, lowerbound, upperbound, method):
    y_data = np.array(y_data).reshape(len(struct.waves), len(struct.angles))
    paras = Parameters()
    no = len([i for i in struct.layers if i.coherent])
    for i, l in enumerate(struct.layers):
        if l.thickness<10000:
            paras.add('layer{}'.format(i), value=l.thickness, vary=~l.coherent,min = lowerbound[i],
                      max=upperbound[i],brute_step=2 )
        else:
            paras.add('layer{}'.format(i), value=l.thickness, vary=False)
    def residual(params, x, y):
        tempstruct = copy.deepcopy(struct)
        # tempstruct.waves = x
        vals = params.valuesdict()
        for i in range(no):
            tempstruct.layers[i].thickness = vals['layer{}'.format(i)]
        tempstruct.initialize()
        print(np.sum(np.abs(y-tempstruct.R)))
        return np.sum(np.abs(y-tempstruct.R))
    out = minimize(residual, paras, args=(struct.waves, y_data), method=method)
    print(fit_report(out))
    ret = []
    vals = out.params.valuesdict()
    print(vals)
    for i in range(len(vals)):
        ret.append(vals['layer{}'.format(i)])
    print(ret)
    return ret

class geneticAlgorithm(object):         # find candidate strutures with relatively heavy constraint
    def __init__(self, limitation, tag):
        self.loops = 1500
        self.noPairs = int(len(limitation.matArray)/2 - 1)
        self.batchSize = 100
        self.candidateSize = 1
        incident = 'Al2O3.txt'
        emergent = 'YAG.txt'
        self.idxdic = limitation.idxdic
        self.constraint = limitation.constraint
        self.indices = limitation.indices
        self.limitation = limitation



        conn = sqlite3.connect("thin_film_data.db")
        c = conn.cursor()
        tableName = 'GA_Pairs{}Mat{}Tag{}'.format(self.noPairs, ''.join(set(limitation.matArray)), tag)
        tableName = ''.join([i for i in tableName if i!='.'])
        print(tableName)
        query = 'CREATE TABLE if not exists {} (id INTEGER)'.format(tableName)
        c.execute(query)

        for l in range(self.noPairs*2):
            try:
                c.execute('''ALTER TABLE {} ADD COLUMN Pair{} NUMERIC '''.format(tableName, l))
            except:
                pass
        self.history = []
        for row in c.execute('''SELECT * FROM {}'''.format(tableName)):
            self.history.append(row)
        # TO DO  convert data in database into initia generation

        #
        tableName = 'Candidate_Pairs{}Mat{}Tag{}'.format(self.noPairs, ''.join(set(limitation.matArray)), tag)
        tableName = ''.join([i for i in tableName if i != '.'])
        self.tableName = tableName
        query = '''CREATE TABLE if not exists {}(MV NUMERIC)'''.format(tableName)
        c.execute(query)
        for l in range(self.noPairs*2):
            try:
                c.execute('''ALTER TABLE {} ADD COLUMN Layer{} NUMERIC '''.format(tableName, l))
            except:
                pass

        for i in range(self.candidateSize):
            self.main(c, conn)

        c.execute('''SELECT * from {}'''.format(tableName))
        print(c.fetchall())
        conn.commit()
        conn.close()



    def main(self, c, conn):
        generationNumber = 0
        lastgeneration = []

        while generationNumber < self.loops:
            kept = min(24, 5+generationNumber)
            # 1. Pad last generation to batch size
            for i in range(self.batchSize - len(lastgeneration)):
                lastgeneration.append(np.random.normal(loc=90, scale=15, size=(self.noPairs)))
            # 2.1 Evaluate the sample
            curResult = []
            for sam in lastgeneration:
                t = time.time()
                curphase = sam
                cursample = structure.QuickStruct(self.limitation, curphase, phase=True)
                curMV = cursample.MV
                curResult.append([curMV, sam])

            # 2.2 Pick good samples
            curResult.sort(key=lambda x:x[0])
            curResult = curResult[:kept]
            lastgeneration = [s[1] for s in curResult]
            print('Current iteration {}, best merit value {}'.format(generationNumber, curResult[0] ))
            tempsample = structure.QuickStruct(self.limitation, lastgeneration[0], phase=True)
            print('Current thickness is', tempsample.thickness)

            # 3.Implement crossover and mutation operation
            crossoverPosition = np.random.randint(1, self.noPairs-1, size=(kept))
            mutationPosition = np.random.randint(0, self.noPairs-1, size=(kept))
            mutationPosition2 = np.random.randint(0, self.noPairs - 1, size=(kept))
            for i in range(kept):
                bp = crossoverPosition[i]          # break point
                bp2 = mutationPosition[i]
                bp3 = mutationPosition2[i]
                if not i:
                    lastgeneration.append(list(lastgeneration[0][:bp]) + list(lastgeneration[-1][bp:]))
                    lastgeneration.append(list(lastgeneration[-1][:bp]) + list(lastgeneration[0][bp:]))
                else:
                    lastgeneration.append(list(lastgeneration[i][:bp]) + list(lastgeneration[i-1][bp:]))
                    lastgeneration.append(list(lastgeneration[i-1][:bp]) + list(lastgeneration[i][bp:]))
                lastgeneration.append(list(lastgeneration[i][:bp2]) + list(np.random.normal(
                        loc=90, scale=15, size=(1))) + list(lastgeneration[i][bp2+1:]))
                lastgeneration.append(list(lastgeneration[i][:bp3]) + list(np.random.normal(
                    loc=90, scale=15, size=(1))) + list(lastgeneration[i][bp3 + 1:]))
            print('Current generation {}'.format(generationNumber))
            generationNumber += 1

        # Save data
        curphase = lastgeneration[0]
        bestSample = structure.QuickStruct(self.limitation, curphase, phase=True)
        bestMV = bestSample.MV
        thickness = bestSample.thickness
        strthickness = ','.join([str(t)[:5] for t in thickness])
        strthickness = '{}'.format(bestMV) + ',' + strthickness
        strthickness = '(' + strthickness + ')'
        print(strthickness)
        print(bestMV)
        print(self.limitation.matArray)
        print('thickness', thickness)
        print('##########################')
        query = '''INSERT INTO {} VALUES {}'''.format(self.tableName, strthickness)
        print('#', query)
        c.execute(query)
        conn.commit()

class localminimum(object):
    def __init__(self, limits, thickness=None, tag=None):
        self.delta = 0.5
        self.learningRate = 1
        self.indices = limits.indices
        self.constraint = limits.constraint
        self.limits = limits
        noPairs = int((len(limits.indices)-2)/2)
        material = limits.material
        print(material)

        if not tag:          # optimize single thickness array
            self.sample = [thickness]

        elif tag:             # optimize frames inside database
            conn = sqlite3.connect("thin_film_data.db")
            c = conn.cursor()
            tableName = 'Vectorization1D_Pairs{}Mat{}Tag{}'.format(noPairs, ''.join(material), tag)
            tableName = ''.join([i for i in tableName if i!='.'])
            print(tableName)
            query = 'CREATE TABLE if not exists {} (MV NUMERIC)'.format(tableName)
            c.execute(query)
            for l in range(noPairs*2):
                try:
                    c.execute('''ALTER TABLE {} ADD COLUMN Pair{} NUMERIC '''.format(tableName, l))
                except:
                    pass
            # load data which need to be optimized
            tag = 'GA_'+ tableName.split('_')[1]
            query = 'SELECT DISTINCT * FROM {}'.format(tag)
            c.execute(query)
            data = c.fetchall()
            sample = []
            for s in data:
                sample.append(list(s[1:]))
            print(sample)
            self.sample = sample

    def Ndimensional(self, N='auto', method='TopN', iterations=30, delta='auto'):
        # method could be top N and pick by probability
        for sam in self.sample:
            mvlist = []
            curIteration = 0
            curThickness = np.array(sam[:])
            while curIteration < iterations:
                curSample = structure.StructJacobian(self.limits, curThickness)
                curMV = curSample.MV
                print('current cost {}, current thicknss{}'.format(curMV, list(curThickness)))
                mvlist.append(curMV)
                jacobian = curSample.Jacobian
                print('jacobian', jacobian)
                # select layers to update
                sortjacobian = sorted(enumerate(jacobian), key=lambda x:abs(x[1]))[::-1]
                if method=='TopN':
                    selectedLayers = sortjacobian[:N]
                elif method=='Probability':
                    totalGradient = sum([abs(i) for i in sortjacobian])
                    selectedLayers = []
                    for no, grad in enumerate(sortjacobian):
                        if np.random.rand() < np.abs(grad) * N:
                            selectedLayers.append([no, grad])
                    if not selectedLayers:
                        selectedLayers.append(jacobian[0])
                # update layers thickness by ratio of gradient, normalize the largest update to 1nm
                selectedIndex = [i[0] for i in selectedLayers]
                normalizeFactor = delta / sortjacobian[0][1]
                deltaThickness = []
                for i in range(len(jacobian)):
                    if i in selectedIndex:
                        deltaThickness.append(jacobian[i])
                    else:
                        deltaThickness.append(0.0)
                deltaThickness = np.array(deltaThickness) * normalizeFactor
                print(list(deltaThickness))
                curThickness = curThickness + deltaThickness
                curIteration += 1
            print('Finished, thickness', list(curThickness))
            print('Cost data', mvlist)
            return mvlist

    def Ndimensionalauto(self, iterations=30):
        # method could be top N and pick by probability

        for sam in self.sample:
            mvlist = []
            curIteration = 0
            curThickness = np.array(sam[:])
            N = [1, 2, 3, 5, 10]
            delta = [0.1, 0.2, 0.3, 0.5, 1.0]
            probability = np.array([[1.0] * 5 for _ in range(5)])
            while curIteration < iterations:
                curSample = structure.StructJacobian(self.limits, curThickness)
                curMV = curSample.MV
                print('current cost {}, current thicknss{}'.format(curMV, list(curThickness)))
                mvlist.append(curMV)
                jacobian = curSample.Jacobian
                print('jacobian', jacobian)
                # select layers to update
                sortjacobian = sorted(enumerate(jacobian), key=lambda x:abs(x[1]))[::-1]
                print('sortedJacobian', sortjacobian)
                iterMV = curMV
                tempThickness = curThickness[:]
                nextThickness = []
                selectIJ = [(0, 0)]
                for i in range(5):
                    for j in range(5):
                        if np.random.random() < probability[i][j]:
                            curN = N[i]
                            curDelta = delta[j]
                            selectedLayers = sortjacobian[:curN]
                            selectedIndex = [i[0] for i in selectedLayers]
                            normalizeFactor = curDelta / sortjacobian[0][1]
                            deltaThickness = []
                            for ii in range(len(jacobian)):
                                if ii in selectedIndex:
                                    deltaThickness.append(jacobian[ii])
                                else:
                                    deltaThickness.append(0.0)
                            deltaThickness = np.array(deltaThickness) * normalizeFactor
                            tempThickness = curThickness + deltaThickness
                            tempStruct = structure.QuickStruct(self.limits, tempThickness, phase=False)
                            tempMV = tempStruct.MV
                            if i==0 and j==0:
                                nextThickness = tempThickness[:]
                            if tempMV <= iterMV:
                                iterMV = tempMV
                                nextThickness =tempThickness[:]
                                selectIJ = [(i, j)]
                curThickness = nextThickness[:]
                # update probability
                i, j = selectIJ[0]
                probability[i][j] = max(1.1, probability[i][j]*1.1)
                for x,y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0<= x+i < 5 and 0<= y+j < 5:
                        probability[x+i][y+j] *= 1.0526
                probability = probability * 0.95          # decay
                probability[0][2] = 1
                print("iteration {}, currentThickness {}".format(curIteration, curThickness))
                print("selected N, delta", N[i], delta[j])
                print(probability)
                # update layers thickness by ratio of gradient, normalize the largest update to 1nm
                curIteration += 1
            print('Finished, thickness', list(curThickness))
            print('Cost data', mvlist)
            return mvlist

    def quickConverge(self, timeOut=50000):
        delta = 0.2
        for sam in self.sample:
            startTime = time.time()
            mvlist = []
            curThickness = np.array(sam[:])
            while time.time()-startTime < timeOut:
                curSample = structure.QuickStruct(self.limits, curThickness, phase=False)
                curMV = curSample.MV
                mvlist.append(curMV)
                for i_t in range(len(curThickness)):
                    curThicknessPlus = curThickness[:]
                    curThicknessPlus[i_t] += delta
                    curSamplePlus = structure.QuickStruct(self.limits, curThicknessPlus, phase=False)
                    curMVPlus = curSamplePlus.MV
                    if curMVPlus < curMV:
                        curThickness[i_t] += delta
                        mvlist.append(curMVPlus)
                        curMV = curMVPlus
                    else:
                        curThicknessMinus = curThickness[:]
                        curThicknessMinus[i_t] -= delta
                        curSampleMinus = structure.QuickStruct(self.limits, curThicknessMinus, phase=False)
                        curMVMinus = curSampleMinus.MV
                        if curMVMinus < curMV:
                            curMV = curMVMinus
                            curThickness[i_t] -= delta
                            mvlist.append(curMVMinus)
                print('Current thickness', list(curThickness))
                print('curMV', curMV)
                print('mvList', mvlist)
            return mvlist







    def vectorization1D(self, iterations):
        for sam in self.sample:
            mvlist = []
            curSample = structure.QuickStruct(self.limits, sam, phase=False)
            sam_init = sam[:]
            MV_init = curSample.MV

            sam_pre = sam[:]
            MV_pre = 1

            iter = 0
            while iter < iterations:
                iter += 1
                gradient = []
                for i in range(len(sam_pre)):
                    curPlus = sam_pre[:]
                    curPlus[i] += self.delta
                    samplePlus = structure.QuickStruct(self.limits, curPlus, phase=False)
                    mvPlus = samplePlus.MV

                    curMinus = sam_pre[:]
                    curMinus[i] -= self.delta
                    sampleMinus = structure.QuickStruct(self.limits, curMinus, phase=False)
                    mvMinus = sampleMinus.MV
                    gradient.append( min((mvPlus-mvMinus)/(2*self.delta) * 800 , 1.))
                sam_cur = sam_pre[:]
                sam_cur = np.array(sam_cur) - np.array(gradient) * self.learningRate * 2 * self.delta
                curSample = structure.QuickStruct(self.limits, sam_cur, phase=False)
                MV_cur = curSample.MV
                print('Gradient', gradient)
                print('Current Structure', list(sam_cur))
                print('Previous MV is', MV_pre,  'Current MV is', MV_cur)
                mvlist.append(MV_cur)

                sam_pre = sam_cur[:]
                MV_pre = MV_cur
            print('Finished Current Sample, mv list is', mvlist)

    def LDS(self, x):                           # a local 2D search algorithm
        def pairOptimize(ti1, ti2, thickness):

            rta = structure.QuickStruct(self.matArray, thickness, self.constraint, self.indices, self.indexdic, phase=False)
            mv_curmax = rta.meritFunction()
            print( 'Inputed material\'s index is {}'.format(mv_curmax))
            mv_pre = 1  # initialize
            overall_iter = 0
            while (overall_iter == 0 or mv_pre > mv_curmax) and overall_iter <= 20:
                print( 'last merit value is {}, overall iteration is {}, current mv is {}'.format(mv_pre, overall_iter,
                                                                                           mv_curmax))
                print('current structure is {}'.format([thickness]))
                mv_pre = mv_curmax
                inner_iter = 0
                mv_pre_inner = 1  # initialize
                while (inner_iter == 0 or mv_pre_inner > mv_curmax) and inner_iter <= 50:
                    mv_pre_inner = mv_curmax
                    for thickindex in [ti1, ti2]:
                        # determine directions
                        thickness_temp = thickness[:]
                        thickness_temp[thickindex] += 0.2
                        rta = structure.QuickStruct(self.matArray, thickness_temp, self.constraint, self.indices, self.indexdic, phase=False)
                        mv_positive = rta.meritFunction()
                        thickness_temp[thickindex] -= 0.4
                        rta = structure.QuickStruct(self.matArray, thickness_temp, self.constraint, self.indices, self.indexdic, phase=False)
                        mv_negative = rta.meritFunction()
                        thickness_temp[thickindex] += 0.2
                        # optimize
                        if mv_positive >= mv_pre_inner and mv_negative >= mv_pre_inner:
                            continue  # early stop
                        else:
                            sign = (-1, 1)[mv_positive < mv_negative]
                            initial_step = step = 0.2
                            mv_pre_singlelayer = 1
                            temp_count = 0
                            while mv_curmax < mv_pre_singlelayer or step > initial_step:  # only end with the smallest increasement
                                if mv_curmax == mv_pre_singlelayer or temp_count == 0:
                                    step = initial_step
                                else:
                                    step = step * 2  # exponentially growth
                                mv_pre_singlelayer = mv_curmax  # record mv of last optimization

                                thickness_temp = thickness[:]
                                thickness_temp[thickindex] += sign * step


                                rta = structure.QuickStruct(self.matArray, thickness_temp, self.constraint, self.indices, self.indexdic, phase=False)
                                mv_current = rta.meritFunction()
                                if mv_current < mv_curmax:  # if mv is better, update thickness and mv_curmax
                                    mv_curmax = mv_current
                                    thickness = thickness_temp[:]
                                    print('thickness updated, {}, the inside count{}, current mv is {}'.format(thickness,
                                                                                                         temp_count,
                                                                                                         mv_curmax))
                                # else, nothing happends, last time. In next iteration, step would become initial_step.
                                # if still nothing happends, this iteration would end
                                temp_count += 1
                    inner_iter += 1
                overall_iter += 1
            return thickness[ti1], thickness[ti2]
        thickness = x
        for ti1 in reversed(range(0, len(thickness), 2)):
            for ti2 in range(1, len(thickness), 2):
                if ti1 != ti2:
                    print('#######', ti1, ti2, thickness)
                    t1, t2 = pairOptimize(ti1, ti2, thickness)
                    thickness[ti1], thickness[ti2] = t1, t2

        def ros(self, x):
            curSample = structure.QuickStruct(self.matArray, x, self.constraint, self.indices, self.indexdic, phase=False)
            MV = curSample.meritFunction()
            return MV

        def gradient(self, x):
            gradient = []
            for i in range(len(x)):
                curPlus = x[:]
                curPlus[i] += self.delta
                samplePlus = structure.QuickStruct(self.matArray, curPlus, self.constraint, self.indices, self.indexdic,
                                                   phase=False)
                mvPlus = samplePlus.meritFunction()

                curMinus = x[:]
                curMinus[i] -= self.delta
                sampleMinus = structure.QuickStruct(self.matArray, curMinus, self.constraint, self.indices,
                                                    self.indexdic,
                                                    phase=False)
                mvMinus = sampleMinus.meritFunction()
                gradient.append(min((mvPlus - mvMinus) / (2 * self.delta) * 400, 1.))
            return gradient













