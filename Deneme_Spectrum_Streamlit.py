# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 22:22:57 2021

@author: hakan
"""

import numpy as np
import pandas as pd
from pandas import read_excel
from numpy import arange
import matplotlib.pyplot as plt
#import plotly as py
#import plotly.graph_objs as go


def soilType_func(soilType, ss, s1):
    if soilType == "ZA":
        Fs = 0.8
    elif soilType == "ZB":
        Fs = 0.9
    elif soilType == "ZC":
        if ss >= 0.25 and ss <=0.5:
            Fs = 1.3
        elif ss > 0.5 and ss <=0.75:
            Fs = 1.3+(ss-0.5)*(-0.1)/0.25
        elif ss > 0.75:
            Fs = 1.2
    elif soilType == "ZD":
        if ss <= 0.25:
            Fs = 1.6
        elif ss >0.25 and ss <=0.50:
            Fs = 1.6 + (ss-0.25) * (-0.2)/0.25
        elif ss > 0.50 and ss <= 0.75:
            Fs = 1.4 + (ss - 0.50) * (-0.2) / 0.25
        elif ss > 0.75 and ss <= 1.00:
            Fs = 1.2 + (ss - 0.75) * (-0.1) / 0.25
        elif ss > 1.00 and ss <= 1.25:
            Fs = 1.1 + (ss - 1.00) * (-0.1) / 0.25
        elif ss > 1.25:
            Fs = 1.0
    elif soilType == "ZE":
        if ss <= 0.25:
            Fs = 2.4
        elif ss > 0.25 and ss <= 0.50:
            Fs = 2.4 + (ss - 0.25) * (-0.7) / 0.25
        elif ss > 0.50 and ss <= 0.75:
            Fs = 1.7 + (ss - 0.50) * (-0.4) / 0.25
        elif ss > 0.75 and ss <= 1.00:
            Fs = 1.3 + (ss - 0.75) * (-0.2) / 0.25
        elif ss > 1.00 and ss <= 1.25:
            Fs = 1.1 + (ss - 1.00) * (-0.2) / 0.25
        elif ss > 1.25 and ss <=1.5:
            Fs = 0.9 + (ss - 1.25) * (-0.1) / 0.25
        elif ss > 1.5:
            Fs = 0.8
    Fs = float(format(Fs, ".2f"))
    print(Fs)
    
    if soilType == "ZA":
        F1 = 0.8
    elif soilType == "ZB":
        F1 = 0.8
    elif soilType == "ZC":
        if s1 <= 0.50:
            F1 = 1.5
        elif s1 > 0.5 and s1 <= 0.60:
            F1 = 1.5 + (s1 - 0.1) * (-0.1) / 0.10
        elif s1 > 0.60:
            F1 = 1.4
    elif soilType == "ZD":
        if s1 <= 0.10:
            F1 = 2.4
        elif s1 > 0.10 and s1 <= 0.20:
            F1 = 2.4 + (s1 - 0.10) * (-0.2) / 0.10
        elif s1 > 0.20 and s1 <= 0.30:
            F1 = 2.2 + (s1 - 0.20) * (-0.2) / 0.10
        elif s1 > 0.30 and s1 <= 0.40:
            F1 = 2.0 + (s1 - 0.30) * (-0.1) / 0.10
        elif s1 > 0.40 and s1 <= 0.50:
            F1 = 1.9 + (s1 - 0.40) * (-0.1) / 0.10
        elif s1 > 0.50 and s1 <= 0.60:
            F1 = 1.8 + (s1 - 0.50) * (-0.1) / 0.10
        elif s1 > 0.60:
            F1 = 1.7
    elif soilType == "ZE":
        if s1 <= 0.10:
            F1 = 4.2
        elif s1 > 0.10 and s1 <= 0.20:
            F1 = 4.2 + (s1 - 0.10) * (-0.9) / 0.10
        elif s1 > 0.20 and s1 <= 0.30:
            F1 = 3.3 + (s1 - 0.20) * (-0.5) / 0.10
        elif s1 > 0.30 and s1 <= 0.40:
            F1 = 2.8 + (s1 - 0.30) * (-0.4) / 0.10
        elif s1 > 0.40 and s1 <= 0.50:
            F1 = 2.4 + (s1 - 0.40) * (-0.2) / 0.10
        elif s1 > 0.50 and s1 <= 0.60:
            F1 = 2.2 + (s1 - 0.50) * (-0.2) / 0.10
        elif s1 > 0.60:
            F1 = 2.0
    F1 = float(format(F1, ".2f"))
    print(F1)
    
    sDs = ss*Fs
    sD1 = s1*F1
      
    return sDs, sD1, F1, Fs

