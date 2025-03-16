import numpy as np
from scipy.optimize import curve_fit
from abc import ABC, abstractmethod
import glob
import uproot3


class Fitter(ABC):
    """Abstract base class for fitting operations."""
    
    def __init__(self, workdir, output_file):
        """
        Initialize the Fitter.
        
        Args:
            workdir (str): Working directory path
            output_file (str): Output file path for fitting results
        """
        self.workdir = workdir
        self.output_file = output_file
        self.file_list = None
    
    def get_file_list(self):
        """
        Get list of files to process.
        
        Returns:
            list: Sorted list of files
        """
        self.file_list = glob.glob(f"{self.workdir}/Day7_????.root")
        self.file_list.sort()
        return self.file_list
    
    @abstractmethod
    def fit_function(self, x, *args):
        """Define the fitting function. To be implemented by subclasses."""
        pass
    
    @abstractmethod
    def perform_fitting(self):
        """Perform the fitting operation. To be implemented by subclasses."""
        pass


class LinearFitter(Fitter):
    """Class for linear fitting with two parameters."""
    
    def __init__(self, workdir, output_file="WTFit_pm7days.txt"):
        """Initialize the LinearFitter."""
        super().__init__(workdir, output_file)
    
    def fit_function(self, x, a, b):
        """
        Linear fitting function with two parameters.
        
        Args:
            x: Input data
            a: First parameter
            b: Second parameter (y-intercept)
            
        Returns:
            float: -x/a + b
        """
        return -x/a + b
    
    def perform_fitting(self):
        """
        Perform linear fitting on all files.
        
        Returns:
            str: Path to the output file with fitting results
        """
        self.get_file_list()
        
        with open(self.output_file, 'w') as f:
            for file_this in self.file_list:
                run_day = str(file_this[-9:-5])
                Odata = uproot3.open(file_this)
                hprof = Odata["prof"]
                
                cont = np.array(hprof.values)
                sumw = np.array(hprof._fBinEntries)[1:-1]
                err2 = np.array(hprof._fSumw2)[1:-1]
                
                for i in range(len(cont)):
                    if sumw[i] == 0:
                        sumw[i] = 1
                
                h = cont/sumw
                s = np.sqrt(err2/sumw - h**2)
                err = s/np.sqrt(sumw)
                
                for i in range(len(cont)):
                    if h[i] == 0:
                        h[i] = 1.001
                
                start = 0
                end = 20
                popt, pcov = curve_fit(
                    self.fit_function,
                    hprof.edges[start:end],
                    np.log(h[start:end]),
                    bounds=((-np.inf), (np.inf))
                )
                
                WT = popt[0]
                WT_err = np.sqrt(np.diag(pcov))[0]
                Y_incep = popt[1]
                Y_incep_err = np.sqrt(np.diag(pcov))[1]
                
                f.write(
                    f"{round(WT, 2)} {round(WT_err, 2)} "
                    f"{round(Y_incep, 5)} {round(Y_incep_err, 5)} "
                    f"{int(run_day)}\n"
                )
                
                print(f"Day_{run_day}")
                print(f"{round(WT, 2)} +/- {round(WT_err, 2)}")
                print(f"{round(Y_incep, 3)} +/- {round(Y_incep_err, 3)}\n")
        
        return self.output_file


class FixedYInterceptFitter(Fitter):
    """Class for linear fitting with fixed y-intercept."""
    
    def __init__(self, workdir, y_intercept=-0.8082, output_file="WTFit_pm7days_yfix.txt"):
        """
        Initialize the FixedYInterceptFitter.
        
        Args:
            workdir (str): Working directory path
            y_intercept (float): Fixed y-intercept value
            output_file (str): Output file path for fitting results
        """
        super().__init__(workdir, output_file)
        self.y_intercept = y_intercept
    
    def fit_function(self, x, a):
        """
        Linear fitting function with fixed y-intercept.
        
        Args:
            x: Input data
            a: Parameter
            
        Returns:
            float: -x/a + fixed_y_intercept
        """
        return -x/a + self.y_intercept
    
    def perform_fitting(self):
        """
        Perform linear fitting with fixed y-intercept on all files.
        
        Returns:
            str: Path to the output file with fitting results
        """
        self.get_file_list()
        
        with open(self.output_file, 'w') as f:
            for file_this in self.file_list:
                run_day = str(file_this[-9:-5])
                Odata = uproot3.open(file_this)
                hprof = Odata["prof"]
                
                cont = np.array(hprof.values)
                sumw = np.array(hprof._fBinEntries)[1:-1]
                err2 = np.array(hprof._fSumw2)[1:-1]
                
                h = cont/sumw
                s = np.sqrt(err2/sumw - h**2)
                err = s/np.sqrt(sumw)
                
                start = 0
                end = 20
                popt, pcov = curve_fit(
                    self.fit_function,
                    hprof.edges[start:end],
                    np.log(h[start:end]),
                    bounds=((-np.inf), (np.inf))
                )
                
                WT = popt[0]
                WT_err = np.sqrt(np.diag(pcov))[0]
                Y_incep = self.y_intercept
                Y_incep_err = 0
                
                f.write(
                    f"{round(WT, 2)} {round(WT_err, 2)} "
                    f"{round(Y_incep, 5)} {round(Y_incep_err, 5)} "
                    f"{int(run_day)}\n"
                )
                
                print(f"Day_{run_day}")
                print(f"{round(WT, 2)} +/- {round(WT_err, 2)}")
                print(f"{round(Y_incep, 3)} +/- {round(Y_incep_err, 3)}\n")
        
        return self.output_file
