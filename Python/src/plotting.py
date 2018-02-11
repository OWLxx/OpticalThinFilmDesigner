from matplotlib import pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
import sqlite3
from matplotlib import cm

def quickplot(R, waves, angles):
    R = np.array(R).reshape((len(waves), len(angles)))
    m, n = R.shape
    plt.figure(1)
    lgd = []
    for i in range(n):
        a, = plt.plot(waves, R[:, i], label='ang {}'.format(angles[i]))
        lgd.append(a)
        plt.legend(handles=lgd)
    plt.xlabel('Wavelength (nm)')
    plt.grid(True)
    plt.show()

def comparetwo(R1, R2, waves, angles):
    print(waves)
    R1 = np.array(R1).reshape((len(waves), len(angles)))
    R2 = np.array(R2).reshape((len(waves), len(angles)))
    m, n = R1.shape

    for i in range(len(angles)):
        plt.figure(int(i/4)+1)
        plt.subplot(2, 2, i%4+1)
        a1, = plt.plot(waves, R1[:,i], label='first')
        a2, = plt.plot(waves, R2[:,i], label='second')
        lgd = [a1, a2]
        plt.legend(handles=lgd)
        plt.xlabel('Wavelength (nm)')
        plt.grid(True)
    plt.show()

def compare3(R1, R2, R3, waves, angles):
    print('##########', waves, angles)
    R1 = np.array(R1).reshape((len(waves), len(angles)))
    R2 = np.array(R2).reshape((len(waves), len(angles)))
    R3 = np.array(R3).reshape((len(waves), len(angles)))
    m, n = R1.shape
    if n == 1:
        plt.figure(1)
        a1, = plt.plot(waves, R1[:, 0], label='first')
        a2, = plt.plot(waves, R2[:, 0], label='second')
        a3, = plt.plot(waves, R3[:], label='third')
        lgd = [a1, a2, a3]
        plt.legend(handles=lgd)
        plt.xlabel('Wavelength (nm)')
        plt.grid(True)
        plt.show()
    else:
        print(R1)
        for i in range(len(angles)):
            plt.figure(int(i/4)+1)
            plt.subplot(2, 2, i%4+1)
            a1, = plt.plot(waves, R1[:,i], label='first')
            a2, = plt.plot(waves, R2[:,i], label='second')
            a3, = plt.plot(waves, R3[:,i], label='third')
            lgd = [a1, a2, a3]
            plt.legend(handles=lgd)
            plt.xlabel('Wavelength (nm)')
            plt.grid(True)
        plt.show()

def surfaceplot(R, RS=None, RP=None, waves=None, angles=None):
    m, n = R.shape
    print(m, n, len(waves), len(angles), '################')
    conn = sqlite3.connect("thin_film_data.db")
    c = conn.cursor()
    query = '''DROP TABLE IF EXISTS R_Data'''
    c.execute(query)
    query = '''CREATE TABLE if not exists R_Data(Angle0 NUMERIC)'''
    c.execute(query)
    for i in range(1, n):
        c.execute('''ALTER TABLE R_Data ADD COLUMN Angle{} NUMERIC '''.format(i))
    for i in range(m):
        query = '''INSERT INTO R_Data VALUES({})'''.format(','.join([str(k) for k in R[i, :]]))
        c.execute(query)
    if RS[0][0] != None:
        query = '''DROP TABLE IF EXISTS RS_Data'''
        c.execute(query)
        query = '''CREATE TABLE if not exists RS_Data(Angle0 NUMERIC)'''
        c.execute(query)
        for i in range(1, n):
            c.execute('''ALTER TABLE RS_Data ADD COLUMN Angle{} NUMERIC '''.format(i))
        for i in range(m):
            query = '''INSERT INTO RS_Data VALUES({})'''.format(','.join([str(k) for k in RS[i, :]]))
            c.execute(query)
    if RP[0][0]!= None:
        query = '''DROP TABLE IF EXISTS RP_Data'''
        c.execute(query)
        query = '''CREATE TABLE if not exists RP_Data(Angle0 NUMERIC)'''
        c.execute(query)
        for i in range(1, n):
            c.execute('''ALTER TABLE RP_Data ADD COLUMN Angle{} NUMERIC '''.format(i))
        for i in range(m):
            query = '''INSERT INTO RP_Data VALUES({})'''.format(','.join([str(k) for k in RP[i, :]]))
            c.execute(query)
    conn.commit()

    # print np.shape(R)   shape is 12L, 226L
    wav = np.array(waves)
    angle = np.array(angles)
    angle, wav = np.meshgrid(angle, wav)
    print('#########', angle.shape, wav.shape)

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