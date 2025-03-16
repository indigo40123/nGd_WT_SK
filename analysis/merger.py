import os
import math
from abc import ABC, abstractmethod


class Merger(ABC):
    """Abstract base class for merging operations."""
    
    def __init__(self, data, workdir, file_list):
        """
        Initialize the Merger.
        
        Args:
            data (pandas.DataFrame): Run data
            workdir (str): Working directory path
            file_list (list): List of files
        """
        self.data = data
        self.workdir = workdir
        self.file_list = file_list
        self.script_path = None
    
    @abstractmethod
    def create_merge_script(self):
        """Create merge script. To be implemented by subclasses."""
        pass
    
    def execute_merge_script(self):
        """
        Execute the merge script.
        
        Returns:
            int: Return code from system command
        """
        if self.script_path:
            return os.system(f'source {self.script_path}')
        else:
            raise ValueError("Script path not set. Call create_merge_script first.")


class SingleDayMerger(Merger):
    """Class for merging files by single day."""
    
    def __init__(self, data, workdir, file_list):
        """Initialize the SingleDayMerger."""
        super().__init__(data, workdir, file_list)
        self.script_path = f"{workdir}/single_day_merge.sh"
    
    def create_merge_script(self):
        """
        Create script for merging files by single day.
        
        Returns:
            str: Path to the created script
        """
        # Initialize the day
        today = -1
        
        # Make a script file
        with open(self.script_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'cd {self.workdir} \n')
            f.write('date\n')
            
            # Get the last day
            lastrun = int(self.file_list[-2][-11:-5])
            lastindex = self.data[self.data['run'] == lastrun].index
            lastday = int(self.data.day[lastindex])
            
            for file_this in self.file_list:
                # Get run number from filename
                run_number = int(file_this[-11:-5])
                index = self.data[self.data['run'] == run_number].index
                # Get the day that corresponding to run number
                run_day = int(self.data.day[index])
                # Skip last day
                if run_day == lastday:
                    break
                run_day1 = int(self.data.day[index+1])
                
                # If this day is a new day, add a merge file name at the beginning
                if today != run_day:
                    today = run_day
                    f.write(f'hadd -f {self.workdir}/Day_{today}.root ')
                # if next run is a new day, write this run and add new line
                if today != run_day1:
                    f.write(f'{self.workdir}/wt_0{run_number}.root \n')
                # if next run is same day, write this run without adding new line
                if today == run_day1:
                    f.write(f'{self.workdir}/wt_0{run_number}.root ')
        
        return self.script_path


class PlusMinusSevenDayMerger(Merger):
    """Class for merging files with ±7 days range."""
    
    def __init__(self, data, workdir, file_list):
        """Initialize the PlusMinusSevenDayMerger."""
        super().__init__(data, workdir, file_list)
        self.script_path = f"{workdir}/pm7days_merge.sh"
    
    def create_merge_script(self):
        """
        Create script for merging files with ±7 days range.
        
        Returns:
            str: Path to the created script
        """
        # Make a script file
        with open(self.script_path, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'cd {self.workdir} \n')
            f.write('date\n')
            
            # Get the last day
            lastrun = int(self.file_list[-2][-11:-5])
            lastindex = self.data[self.data['run'] == lastrun].index
            lastday = int(self.data.day[lastindex])
            
            for file_this in self.file_list:
                # Get run number from filename
                run_number = int(file_this[-11:-5])
                index = self.data[self.data['run'] == run_number].index
                
                # Get the day that corresponding to run number
                run_day = int(self.data.day[index])
                
                # Break if the data is less then 7 days
                if (lastday - run_day) < 7:
                    break
                
                # Find the run number of -7 days and +7 days
                range_low = None
                range_high = None
                
                # Find the run number of -7 days
                try:
                    minus_seven_index = (self.data[self.data['day'] == (run_day - 7)].index)
                    if not minus_seven_index.empty:
                        minus_seven_run = self.data.run[minus_seven_index].min()
                        minus_seven_name = f"{self.workdir}/wt_0{minus_seven_run}.root"
                        range_low = (minus_seven_run, minus_seven_name)
                except Exception:
                    continue
                
                # Find the run number of +7 days
                try:
                    plus_seven_index = (self.data[self.data['day'] == (run_day + 7)].index)
                    if not plus_seven_index.empty:
                        plus_seven_run = self.data.run[plus_seven_index].max()
                        plus_seven_name = f"{self.workdir}/wt_0{plus_seven_run}.root"
                        range_high = (plus_seven_run, plus_seven_name)
                except Exception:
                    continue
                
                # Check if low bound and high bound exist
                if range_low and range_high:
                    condition1 = (len(str(range_low[0])) + len(str(range_high[0]))) == 10
                    condition2 = (range_low[1] in self.file_list)
                    condition3 = (range_high[1] in self.file_list)
                    
                    # Check if this run is the last run in a day
                    condition4 = (int(self.data.day[index]) != int(self.data.day[index+1]))
                    
                    if condition1 and condition2 and condition3 and condition4:
                        # Define merge file name
                        f.write(f'hadd -f {self.workdir}/Day7_{run_day}.root ')
                        
                        # Loop to write the merge file list
                        for i in range(int(range_low[0]), int(range_high[0]) + 1):
                            # Check if the file exist
                            file_path = f"{self.workdir}/wt_0{i}.root"
                            if file_path in self.file_list:
                                # Write the file name
                                f.write(f"{file_path} ")
                        # New line for next day
                        f.write('\n ')
        
        return self.script_path
