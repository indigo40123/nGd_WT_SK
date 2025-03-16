import os
import glob
import pandas as pd
import math
import uproot3
import numpy as np


class DataHandler:
    """Base class for handling data operations."""
    
    def __init__(self, workdir=None):
        """
        Initialize the DataHandler.
        
        Args:
            workdir (str): Working directory path
        """
        self.workdir = workdir
        self.data = None
        self.file_list = None
    
    def read_data(self):
        """Read data from source. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement read_data method")
    
    def process_data(self):
        """Process data. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement process_data method")


class RootDataHandler(DataHandler):
    """Handler for ROOT file data."""
    
    def __init__(self, workdir=None):
        """Initialize the RootDataHandler."""
        super().__init__(workdir)
    
    def open_root_file(self, file_path):
        """
        Open a ROOT file.
        
        Args:
            file_path (str): Path to the ROOT file
            
        Returns:
            uproot3.rootio.ROOTDirectory: Opened ROOT file
        """
        return uproot3.open(file_path)
    
    def extract_histogram_data(self, hprof):
        """
        Extract data from a histogram profile.
        
        Args:
            hprof: Histogram profile object
            
        Returns:
            tuple: (edges, h, err) - Edges, histogram values, and errors
        """
        cont = np.array(hprof.values)
        sumw = np.array(hprof._fBinEntries)[1:-1]
        err2 = np.array(hprof._fSumw2)[1:-1]
        
        # Handle zero values in sumw
        for i in range(len(sumw)):
            if sumw[i] == 0:
                sumw[i] = 1
        
        h = cont/sumw
        s = np.sqrt(err2/sumw - h**2)
        err = s/np.sqrt(sumw)
        
        # Handle zero values in h
        for i in range(len(h)):
            if h[i] == 0:
                h[i] = 1.001
                
        return hprof.edges, h, err


class RunDataHandler(DataHandler):
    """Handler for run data and file operations."""
    
    def __init__(self, workdir=None, runsum_path=None):
        """
        Initialize the RunDataHandler.
        
        Args:
            workdir (str): Working directory path
            runsum_path (str): Path to the runsum.dat file
        """
        super().__init__(workdir)
        self.runsum_path = runsum_path
    
    def read_data(self):
        """
        Read run data from runsum.dat and create file list.
        
        Returns:
            tuple: (data, workdir, file_list)
        """
        # Get run number and Days
        self.data = pd.read_csv(
            self.runsum_path,
            delimiter='\s+', 
            names=['run', 'a', 'b', 'c', 'd', 'e', 'f', 'day']
        )
        
        # Make a list of files
        self.file_list = glob.glob(f"{self.workdir}/wt_0?????.root")
        self.file_list.sort()
        
        return self.data, self.workdir, self.file_list
    
    def find_run_by_day(self, run_day, offset):
        """
        Find run number and name for a given day with offset.
        
        Args:
            run_day (int): Base run day
            offset (int): Day offset
            
        Returns:
            tuple: (run_num, run_name)
        """
        index = (self.data[self.data['day'] == (run_day + offset)].index)
        if offset < 0:
            run_num = self.data.run[index].min()
        else:
            run_num = self.data.run[index].max()
        
        run_name = f"{self.workdir}/wt_0{run_num}.root"
        return run_num, run_name
    
    def get_last_day(self):
        """
        Get the last day from file list.
        
        Returns:
            int: Last day
        """
        lastrun = int(self.file_list[-2][-11:-5])
        lastindex = self.data[self.data['run'] == lastrun].index
        return int(self.data.day[lastindex])
