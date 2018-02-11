import numpy as np
thickness = [ 103.51,  251.1  ,  97.98,  114.2 ,   34.75 , 131.5 ,  101.5 , 136.1 ,   78.47,
  134.6,    76.02,  105.7,    83.59,  117.3,    62.46,   94.54,   60.95,   91.,
   75.47,  106.4 ,   78.26,  115.2 ,   43.84,   69.48,   57.91,   84.91,   73.04,
  102.5,    63.69,   94.5,    46.47,   70.19,   46.04,   70.32,   53.1,    79.66,
   60.06,   86.15,   47.41,   66.79,   97.82,  139.2,    50.56,   79.61,   50.07,
   74.95,   94.88,  133.1,    64.64,   98.27,   86.18,  129.8 ,   87.3,   130.8,
  132.5,   178.7,    73.24,  175.8,    62.72,  152.1]


struct =['Al2O3.txt'] + ['Ta2O5.txt', 'SiO2.txt']*30 + ["YAG.txt"]
print(struct[0])
for i, t in enumerate(thickness):
    print('Layer ', i+1, '\t', struct[i+1],'\t', np.round(t, 5))

print('YAG')
