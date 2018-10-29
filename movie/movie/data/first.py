'''
Created on 2018年9月6日

@author: swz
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

moviesvv = pd.read_excel(r"wyzc-data.xlsx",sheet_name=0)
#moviesvv.head(-1)