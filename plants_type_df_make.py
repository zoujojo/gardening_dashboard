# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:21:41 2022

@author: zoujo
"""

import pandas as pd

pd.set_option('display.max_columns', None)

PLANT_dir = "C:/Users/zoujo/OneDrive/Desktop/plant/"

df = pd.read_pickle(PLANT_dir + "zone6_plants.pkl")

plants_perType = df.groupby("Plant Type").count().reset_index().iloc[:,0:2]
plants_perType = plants_perType.rename(columns={"Name": "Count"})

plants_perType.to_pickle(PLANT_dir + 'plant_type_count.pkl',  protocol = 4)
