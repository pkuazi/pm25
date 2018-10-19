#
# -*-coding:utf-8 -*-
#
# @Author: zhaojianghua
# @Date  : 2018-10-18 16:21
#

"""

""" 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# df = pd.DataFrame({
#     'year': range(1999, 2017),
#     'mean PM2.5 concentration': [11.91267225,11.48035477,13.99882589,14.41789359,17.20177551,15.12967781,17.7795941,18.37165132,18.67785942,18.21509548,17.82371541,17.9357578,16.87603286,16.116953,18.43550126,17.57089786,18.63404943,17.6520063],
#     'std': [11.38775358,10.90039253,12.56901329,12.85762553,15.08843101,13.91200415,16.46327858,17.78969294,18.76897192,16.88781358,16.97234442,17.1066143,15.96268857,15.01560981,17.46769329,16.59476764,17.80060634,14.93776759]})
#
fig, ax = plt.subplots()    # 1
#
# df.plot('year', 'mean PM2.5 concentration', yerr='std',kind='bar', ax=ax, color='red')   # 2


#
x = range(1999, 2017)
mean = [11.91267225,11.48035477,13.99882589,14.41789359,17.20177551,15.12967781,17.7795941,18.37165132,18.67785942,18.21509548,17.82371541,17.9357578,16.87603286,16.116953,18.43550126,17.57089786,18.63404943,17.6520063] # 10, not 9, so the fit isn't perfect
std = [11.38775358,10.90039253,12.56901329,12.85762553,15.08843101,13.91200415,16.46327858,17.78969294,18.76897192,16.88781358,16.97234442,17.1066143,15.96268857,15.01560981,17.46769329,16.59476764,17.80060634,14.93776759]
fit = np.polyfit(x,mean,1)
fit_fn = np.poly1d(fit)
# fit_fn is now a function which takes in x and returns an estimate for y

plt.plot(x,mean, 'yo', x, fit_fn(x), '--k',color='darkred')
plt.xlim(1998,2017)
# plt.bar(x, mean, std, color = 'red',error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))
plt.errorbar(x, mean, std, fmt='.k', lw=1)

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
        }
# plt.title('Damped exponential decay', fontdict=font)
# plt.text(2, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict=font)
# plt.xlabel('year', fontdict=font)
plt.ylabel('annual mean PM2.5(micrograms/cubic meter)', fontdict=font)

plt.show()


