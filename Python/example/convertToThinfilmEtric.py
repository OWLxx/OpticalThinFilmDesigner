import numpy as np
'''
This script will convert a thin film recipe into FilmEtric URL. Copy the printed URL and open it in Browser
'''
example = 'https://www.filmetrics.com/reflectance-calculator?wmin=1300&wmax=1340&wstep=1&angle=0&pol=mixed&units=nm&mmat=InP&mat[]=Al2O3&d[]=121.1&mat[]=Si&d[]=61&mat[]=Al2O3&d[]=145.2&mat[]=Si&d[]=72.61&smat=InP&sptype=r'
minwave = str(1300)
maxwave = str(1340)

thickness = [174.4, 87.21, 125.5, 62.8, 132.5, 66.29, 139.1, 69.59, 163.5, 81.78]
mat = ['Si', 'Al2O3']
ans = ''
for i, t in enumerate(thickness):
    ans += '&mat[]={}'.format(mat[(i+1)%2])
    ans += '&d[]={}'.format(np.around(t, 3))
print(ans)
ans = 'https://www.filmetrics.com/reflectance-calculator?wmin=1300&wmax=1340&wstep=1&angle=0&pol=mixed&units=nm&mmat=InP' + ans
ans += '&smat=InP&sptype=r'
print(ans)