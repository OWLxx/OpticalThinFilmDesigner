import numpy as np
def meritFunction1(R):
    # R and T are m*n dimensional matrix, m is number of wavelength, n is number of angles
    # This function is for Dichronic filter designing
    #
    # minw = self.constraint['minWave']
    # maxw = self.constraint['maxWave']
    # stepw = self.constraint['waveStep']
    # angles = self.constraint['angle']
    pb_start, pb_end = 0, 5
    sb_start, sb_end = 7, 25
    try:
        R_pb_avg = np.average(R[pb_start:pb_end + 1, 0:2], axis=1)  # only the first two angle
        R_sb_avg = np.average(R[sb_start:sb_end + 1, :], axis=1)  # all the angle
    except:
        return 1

    R_pb = np.average(R_pb_avg)
    R_sb = np.average(R_sb_avg)
    RF = 0.725
    MV = 1 - 0.5 * (1 - RF) * (1 + R_sb) / (1 - RF * R_sb) * (1 - R_pb)
    print(R_pb, R_sb, MV)
    return MV


def meritFunction2(R, T=None):
    # this merit function is for Brewster Hole designing
    R_avg = np.average(np.average(R))
    return 1 - R_avg

def meritFunction3(R):
    # 0-89 deg, 1 angle
    m, n = R.shape      # m wavelength, n angles
    a = range(0, 90)
    waves = range(430, 651)
    angles = np.arange(0, 90, 1)
    angles = np.deg2rad(angles)
    weight = [np.sin(angles[i+1])-np.sin(angles[i]) for i in range(89)]
    R_pb = R[0:40, 0:15]
    R_sb = R[60:, :]
    R_pb_avg = np.mean(R_pb)
    R_sb_avg = 0
    print(m, n, len(weight))
    for i in range(n-1):
        R_sb_avg += np.mean(R_sb[:, i]) * weight[i]
    RF = 0.725
    MV = 1 - 0.5 * (1 - RF) * (1 + R_sb_avg) / (1 - RF * R_sb_avg) * (1 - R_pb_avg)
    print('Angle averaged Reflection', np.average(R_sb, axis=0))
    print(list(np.average(R_sb,  axis=1)))
    print(list(np.average(R_sb, axis=0)))

    print('Accurate dichroic MV is ', MV)
    print(R_sb_avg, R_pb_avg)

def meritFunction4(R):
    m, n = R.shape
    R_sb = np.mean(R[0:14, :])
    R_pb = np.mean(R[18:, :])
    print(R_pb, R_sb)
    #print((1.0-np.mean(R_sb) +np.mean(R_pb))/2.0)
    return (R_pb*1.2 - R_sb)/2.0