import pandas as pd
import os, sys, time
import uproot3
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def WT_Plot():
    nGd_D7 =  pd.read_csv('WTFit_pm7days.txt',\
              delimiter= '\s+', names = ['WT','serr','b','c','Day'] )
    nGd_D7y = pd.read_csv('WTFit_pm7days_yfix.txt',\
              delimiter= '\s+', names = ['WT','serr','b','c','Day'] )

    Mue_D7 =  pd.read_csv('Fit14_30_Mue_day7.txt',\
              delimiter= '\s+', names = ['WT','serr','b','c','Day'] )
    Mue_D7y = pd.read_csv('Fit14_30_Mue_day7_yfix.txt',\
              delimiter= '\s+', names = ['WT','serr','b','c','Day'] )   

    x = np.linspace(9649,9800,1000)
    x1 = np.linspace(400,400,1000)
    x2 = np.linspace(0,0,1000)

    m_size = 1
    plt.figure(5,figsize=(8,5))
    plt.errorbar(nGd_D7.Day,nGd_D7.WT/100,yerr=nGd_D7.serr/100,color='purple',ls='',marker='o',markersize=m_size,linewidth=0.5,elinewidth=0.2,label=r'nGd,')
    plt.errorbar(nGd_D7y.Day,nGd_D7y.WT/100,yerr=nGd_D7y.serr/100,color='orange',ls='',marker='o',markersize=m_size,linewidth=0.5,elinewidth=0.2,label=r'nGd,y fix')
    plt.errorbar(Mue_D7.Day,Mue_D7.WT/100,yerr=Mue_D7.serr/100,color='black',ls='',marker='o',markersize=m_size,linewidth=0.5,elinewidth=0.2,label=r'Mu_e')
    plt.errorbar(Mue_D7y.Day,Mue_D7y.WT/100,yerr=Mue_D7y.serr/100,color='red',ls='',marker='o',markersize=m_size,linewidth=0.5,elinewidth=0.2,label=r'Mu_e,y fix')
    plt.fill_between(x, x1, x2,step="pre",alpha=0.2,color='gray')
    plt.text(9710,105, 'SK VII', fontsize=14)
    plt.ylim(100., 220)
    plt.xlim(8930., 9820)
    plt.tick_params(direction='in',which='both',labelsize=13, length=10, width=2)
    plt.grid(which='major', axis='both')
    plt.xlabel('Day',fontsize=14,loc='right')
    plt.ylabel('Attenuation length [m]',fontsize=14,loc='top')
    plt.legend(loc='upper right')
    plt.show()
