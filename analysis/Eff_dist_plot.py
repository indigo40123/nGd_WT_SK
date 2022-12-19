import uproot3
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def Eff_Dist_Plot(workdir):
    data_1 = '/Day7_9680.root'

    nGd_1 = uproot3.open(workdir+data_1)

    def data_handle (file):
        hprof = file['prof']
    
        cont = np.array(hprof.values)
        sumw = np.array(hprof._fBinEntries)[1:-1]
        err2 = np.array(hprof._fSumw2)[1:-1]
    
        h = cont/sumw
        s = np.sqrt(err2/sumw - h**2)
        err = s/np.sqrt(sumw)

        return hprof.edges, h, err 

    nGd1 = data_handle(nGd_1)
    x = np.linspace(700,3400,1000)
    x1 = np.linspace(1,1,1000)
    x2 = np.linspace(0,0,1000)

    plt.figure(1,figsize=(7,6))
    plt.errorbar(nGd1[0][1:],nGd1[1],yerr=nGd1[2],xerr=75,fmt ='o',markersize=1,elinewidth=1,label='$\pm 7$ Days',color='purple')
    plt.fill_between(x, x1, x2,step="pre",alpha=0.2,color='gray')
    plt.text(900,.31, 'Fitting region: [700,3400]cm', fontsize=14)
    plt.xlim(400., 3600)
    plt.ylim(0.3, .45)
    plt.tick_params(direction='in',which='both',labelsize=13, length=10, width=2)
    plt.title('nGd WT, Day 9680',fontsize=14)
    plt.xlabel('Distance [cm]',fontsize=14,loc='right')
    plt.ylabel('$N_{eff}$ ',fontsize=14,loc='top')
    plt.tick_params(labelsize=14,direction='in',which='both', width=2)
    plt.tick_params(direction='in',which='major', length=10, width=2)
    plt.tick_params(direction='in',which='minor', length=5, width=2, color='black')
    plt.grid(b=None, which='major', axis='both')
    plt.locator_params(axis='x', nbins=10)
    plt.legend(loc='best')
    plt.show()


