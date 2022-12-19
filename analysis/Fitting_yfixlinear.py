import os, glob, time, subprocess
import uproot3
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def WT_fitting_yfix(workdir):
    file_list = glob.glob(workdir + '/Day7_????.root')
    file_list.sort()

    f = open('WTFit_pm7days_yfix.txt','w')
    for file_this in file_list:

        run_day = str(file_this[-9:-5])
        Odata = uproot3.open(file_this)
        hprof = Odata["prof"]

        cont = np.array(hprof.values)
        sumw = np.array(hprof._fBinEntries)[1:-1]
        err2 = np.array(hprof._fSumw2)[1:-1]
    
        h = cont/sumw
        s = np.sqrt(err2/sumw - h**2)
        err = s/np.sqrt(sumw)  
    
        def func(x, a):
            return -x/a - 0.8082
        start = 0
        end = 20
        popt, pcov = curve_fit(func, hprof.edges[start:end],\
                                     np.log(h[start:end]),\
                                     bounds=((-np.inf),(np.inf)))
        WT = popt[0]
        WT_err = np.sqrt(np.diag(pcov))[0]
        Y_incep = -0.8082
        Y_incep_err = 0
        f.write( str(round(WT,2)) + ' ' + str(round(WT_err,2)) + ' ' + \
                 str(round(Y_incep,5)) + ' ' + str(round(Y_incep_err,5)) + ' ' + \
                 str(int(run_day)) + '\n')
        print('Day_' + str(file_this[-9:-5]))
        print(str(round(WT,2)) + ' +/- ' + str(round(WT_err,2) ))
        print(str(round(Y_incep,3)) + ' +/- ' + str(round(Y_incep_err,3) ), '\n')
    
    f.close()
