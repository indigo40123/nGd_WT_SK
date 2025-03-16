import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
import uproot3


class Plotter(ABC):
    """Abstract base class for plotting operations."""
    
    def __init__(self):
        """Initialize the Plotter."""
        pass
    
    @abstractmethod
    def create_plot(self):
        """Create plot. To be implemented by subclasses."""
        pass
    
    def show_plot(self):
        """Display the plot."""
        plt.show()
    
    def save_plot(self, filename):
        """
        Save the plot to a file.
        
        Args:
            filename (str): Output file path
        """
        plt.savefig(filename)


class EfficiencyDistancePlotter(Plotter):
    """Class for plotting efficiency vs distance."""
    
    def __init__(self, workdir):
        """
        Initialize the EfficiencyDistancePlotter.
        
        Args:
            workdir (str): Working directory path
        """
        super().__init__()
        self.workdir = workdir
    
    def create_plot(self, data_file="/Day7_9680.root"):
        """
        Create efficiency vs distance plot.
        
        Args:
            data_file (str): Data file path relative to workdir
            
        Returns:
            matplotlib.figure.Figure: The created plot
        """
        # Open the ROOT file
        nGd_1 = uproot3.open(self.workdir + data_file)
        
        # Extract data
        hprof = nGd_1['prof']
        cont = np.array(hprof.values)
        sumw = np.array(hprof._fBinEntries)[1:-1]
        err2 = np.array(hprof._fSumw2)[1:-1]
        
        h = cont/sumw
        s = np.sqrt(err2/sumw - h**2)
        err = s/np.sqrt(sumw)
        
        # Create plot
        x = np.linspace(700, 3400, 1000)
        x1 = np.linspace(1, 1, 1000)
        x2 = np.linspace(0, 0, 1000)
        
        plt.figure(1, figsize=(7, 6))
        plt.errorbar(
            hprof.edges[1:], h, yerr=err, xerr=75, fmt='o',
            markersize=1, elinewidth=1, label='$\pm 7$ Days', color='purple'
        )
        plt.fill_between(x, x1, x2, step="pre", alpha=0.2, color='gray')
        plt.text(900, .31, 'Fitting region: [700,3400]cm', fontsize=14)
        plt.xlim(400., 3600)
        plt.ylim(0.3, .45)
        plt.tick_params(direction='in', which='both', labelsize=13, length=10, width=2)
        plt.title('nGd WT, Day 9680', fontsize=14)
        plt.xlabel('Distance [cm]', fontsize=14, loc='right')
        plt.ylabel('$N_{eff}$ ', fontsize=14, loc='top')
        plt.tick_params(labelsize=14, direction='in', which='both', width=2)
        plt.tick_params(direction='in', which='major', length=10, width=2)
        plt.tick_params(direction='in', which='minor', length=5, width=2, color='black')
        plt.grid(b=None, which='major', axis='both')
        plt.locator_params(axis='x', nbins=10)
        plt.legend(loc='best')
        
        return plt.gcf()


class WTTrendPlotter(Plotter):
    """Class for plotting WT trend."""
    
    def __init__(self):
        """Initialize the WTTrendPlotter."""
        super().__init__()
    
    def create_plot(self, ngd_file="WTFit_pm7days.txt", ngd_yfix_file="WTFit_pm7days_yfix.txt",
                   mue_file="Fit14_30_Mue_day7.txt", mue_yfix_file="Fit14_30_Mue_day7_yfix.txt"):
        """
        Create WT trend plot.
        
        Args:
            ngd_file (str): nGd data file path
            ngd_yfix_file (str): nGd data file with fixed y-intercept path
            mue_file (str): Mue data file path
            mue_yfix_file (str): Mue data file with fixed y-intercept path
            
        Returns:
            matplotlib.figure.Figure: The created plot
        """
        # Read data files
        nGd_D7 = pd.read_csv(
            ngd_file, delimiter='\s+',
            names=['WT', 'serr', 'b', 'c', 'Day']
        )
        nGd_D7y = pd.read_csv(
            ngd_yfix_file, delimiter='\s+',
            names=['WT', 'serr', 'b', 'c', 'Day']
        )
        Mue_D7 = pd.read_csv(
            mue_file, delimiter='\s+',
            names=['WT', 'serr', 'b', 'c', 'Day']
        )
        Mue_D7y = pd.read_csv(
            mue_yfix_file, delimiter='\s+',
            names=['WT', 'serr', 'b', 'c', 'Day']
        )
        
        # Create plot
        x = np.linspace(9649, 9800, 1000)
        x1 = np.linspace(400, 400, 1000)
        x2 = np.linspace(0, 0, 1000)
        
        m_size = 1
        plt.figure(5, figsize=(8, 5))
        plt.errorbar(
            nGd_D7.Day, nGd_D7.WT/100, yerr=nGd_D7.serr/100,
            color='purple', ls='', marker='o', markersize=m_size,
            linewidth=0.5, elinewidth=0.2, label=r'nGd,'
        )
        plt.errorbar(
            nGd_D7y.Day, nGd_D7y.WT/100, yerr=nGd_D7y.serr/100,
            color='orange', ls='', marker='o', markersize=m_size,
            linewidth=0.5, elinewidth=0.2, label=r'nGd,y fix'
        )
        plt.errorbar(
            Mue_D7.Day, Mue_D7.WT/100, yerr=Mue_D7.serr/100,
            color='black', ls='', marker='o', markersize=m_size,
            linewidth=0.5, elinewidth=0.2, label=r'Mu_e'
        )
        plt.errorbar(
            Mue_D7y.Day, Mue_D7y.WT/100, yerr=Mue_D7y.serr/100,
            color='red', ls='', marker='o', markersize=m_size,
            linewidth=0.5, elinewidth=0.2, label=r'Mu_e,y fix'
        )
        plt.fill_between(x, x1, x2, step="pre", alpha=0.2, color='gray')
        plt.text(9710, 105, 'SK VII', fontsize=14)
        plt.ylim(100., 220)
        plt.xlim(8930., 9820)
        plt.tick_params(direction='in', which='both', labelsize=13, length=10, width=2)
        plt.grid(which='major', axis='both')
        plt.xlabel('Day', fontsize=14, loc='right')
        plt.ylabel('Attenuation length [m]', fontsize=14, loc='top')
        plt.legend(loc='upper right')
        
        return plt.gcf()
