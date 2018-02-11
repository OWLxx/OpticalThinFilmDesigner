import numpy as np
import sqlite3

'''
Quick access SQLite by SQL query
tags:
'GA_Pairs30MatSiO2txtTa2O5txtTag2matTest'
'GA_Pairs30MatAl2O3txtSiO2txtYAGtxtTa2O5txtTag2matBWHole'
GA_Pairs30MatYAGtxtSiO2txtTa2O5txtAl2O3txtMgF2txtTag3matDichronic
'''
tag ='GA_Pairs20MatSitxtAl2O3txtInPtxtTag2matlaser'
conn = sqlite3.connect("thin_film_data.db")
c = conn.cursor()

query = 'Delete FROM {}'.format(tag)
c.execute(query)
print(c.fetchall())





conn.commit()