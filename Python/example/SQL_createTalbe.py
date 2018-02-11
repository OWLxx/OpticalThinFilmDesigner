import numpy as np
import sqlite3

conn = sqlite3.connect("thin_film_data.db")
c = conn.cursor()
tag = 'GA_Pairs29MatYAGtxtSiO2txtTa2O5txtAl2O3txtMgF2txt19txtTag3matDichronic'
query = 'CREATE TABLE if not exists {} (id INTEGER)'.format(tag)
c.execute(query)

for l in range(58):
    try:
        c.execute('''ALTER TABLE {} ADD COLUMN Pair{} NUMERIC '''.format(tag, l))
    except:
        pass
conn.commit()
conn.close()