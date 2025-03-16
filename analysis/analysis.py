import os
from analysis.refactored.data_handler import RunDataHandler
from analysis.refactored.merger import SingleDayMerger, PlusMinusSevenDayMerger
from analysis.refactored.fitter import LinearFitter, FixedYInterceptFitter
from analysis.refactored.plotter import EfficiencyDistancePlotter, WTTrendPlotter


class WTAnalysis:
    """Main class for WT analysis workflow."""
    
    def __init__(self, workdir=None, runsum_path=None):
        """
        Initialize the WTAnalysis.
        
        Args:
            workdir (str): Working directory path
            runsum_path (str): Path to the runsum.dat file
        """
        self.workdir = workdir
        self.runsum_path = runsum_path
        self.data_handler = None
        self.data = None
        self.file_list = None
    
    def setup(self):
        """
        Set up the analysis by initializing data handler and reading data.
        
        Returns:
            WTAnalysis: Self for method chaining
        """
        self.data_handler = RunDataHandler(self.workdir, self.runsum_path)
        self.data, self.workdir, self.file_list = self.data_handler.read_data()
        return self
    
    def merge_files(self):
        """
        Merge files using both single day and ±7 days methods.
        
        Returns:
            WTAnalysis: Self for method chaining
        """
        # Create and execute single day merger
        single_day_merger = SingleDayMerger(self.data, self.workdir, self.file_list)
        single_day_merger.create_merge_script()
        single_day_merger.execute_merge_script()
        
        # Create and execute ±7 days merger
        pm7_merger = PlusMinusSevenDayMerger(self.data, self.workdir, self.file_list)
        pm7_merger.create_merge_script()
        pm7_merger.execute_merge_script()
        
        return self
    
    def perform_fitting(self):
        """
        Perform fitting using both linear and fixed y-intercept methods.
        
        Returns:
            WTAnalysis: Self for method chaining
        """
        # Perform linear fitting
        linear_fitter = LinearFitter(self.workdir)
        linear_fitter.perform_fitting()
        
        # Perform fixed y-intercept fitting
        fixed_y_fitter = FixedYInterceptFitter(self.workdir)
        fixed_y_fitter.perform_fitting()
        
        return self
    
    def create_plots(self):
        """
        Create efficiency-distance and WT trend plots.
        
        Returns:
            WTAnalysis: Self for method chaining
        """
        # Create efficiency-distance plot
        eff_dist_plotter = EfficiencyDistancePlotter(self.workdir)
        eff_dist_plotter.create_plot()
        eff_dist_plotter.show_plot()
        
        # Create WT trend plot
        wt_trend_plotter = WTTrendPlotter()
        wt_trend_plotter.create_plot()
        wt_trend_plotter.show_plot()
        
        return self
    
    def run_analysis(self):
        """
        Run the complete analysis workflow.
        
        Returns:
            WTAnalysis: Self for method chaining
        """
        return (self
                .setup()
                .merge_files()
                .perform_fitting()
                .create_plots())


def main():
    """Main function to run the analysis."""
    # Define paths
    workdir = '/disk02/usr7/licheng/nGd_gitlab/output'
    runsum_path = '/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat'
    
    # Create and run analysis
    analysis = WTAnalysis(workdir, runsum_path)
    analysis.run_analysis()


if __name__ == "__main__":
    main()
