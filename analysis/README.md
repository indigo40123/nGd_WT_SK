# WT Analysis Code

This directory contains a refactored version of the WT analysis code, where the old version is at \Old_code.

## Code Structure

The refactored code is organized into the following modules:

- `data_handler.py`: Classes for handling data operations
  - `DataHandler`: Abstract base class for data handling
  - `RootDataHandler`: Handler for ROOT file data
  - `RunDataHandler`: Handler for run data and file operations

- `merger.py`: Classes for merging operations
  - `Merger`: Abstract base class for merging operations
  - `SingleDayMerger`: Class for merging files by single day
  - `PlusMinusSevenDayMerger`: Class for merging files with ±7 days range

- `fitter.py`: Classes for fitting operations
  - `Fitter`: Abstract base class for fitting operations
  - `LinearFitter`: Class for linear fitting with two parameters
  - `FixedYInterceptFitter`: Class for linear fitting with fixed y-intercept

- `plotter.py`: Classes for plotting operations
  - `Plotter`: Abstract base class for plotting operations
  - `EfficiencyDistancePlotter`: Class for plotting efficiency vs distance
  - `WTTrendPlotter`: Class for plotting WT trend

- `analysis.py`: Main class for orchestrating the analysis workflow
  - `WTAnalysis`: Main class that coordinates all operations

- `run_analysis.py`: Script to run the analysis with command line arguments

## How to Use

### Running the Full Analysis

To run the full analysis with default parameters:

```bash
python -m analysis.refactored.run_analysis
```

To specify custom paths:

```bash
python -m analysis.refactored.run_analysis /path/to/workdir /path/to/runsum.dat
```

### Using Individual Components

You can also use individual components of the refactored code in your own scripts:

```python
from analysis.refactored.data_handler import RunDataHandler
from analysis.refactored.merger import SingleDayMerger
from analysis.refactored.fitter import LinearFitter
from analysis.refactored.plotter import WTTrendPlotter

# Initialize data handler
data_handler = RunDataHandler(workdir, runsum_path)
data, workdir, file_list = data_handler.read_data()

# Create and run merger
merger = SingleDayMerger(data, workdir, file_list)
merger.create_merge_script()
merger.execute_merge_script()

# Perform fitting
fitter = LinearFitter(workdir)
fitter.perform_fitting()

# Create plot
plotter = WTTrendPlotter()
plotter.create_plot()
plotter.show_plot()
```

### Using the WTAnalysis Class

The `WTAnalysis` class provides a convenient way to run the entire analysis workflow:

```python
from analysis.refactored.analysis import WTAnalysis

# Create analysis object
analysis = WTAnalysis(workdir, runsum_path)

# Run full analysis
analysis.run_analysis()

# Or run individual steps
analysis.setup()
analysis.merge_files()
analysis.perform_fitting()
analysis.create_plots()
```
## Dependencies

The refactored code has the same dependencies as the original code:
- uproot3
- numpy
- pandas
- scipy
- matplotlib

## Old codes

The original code is located at /Old_code which includes :
`wt_analysis.py`
:  Summarized the analysis codes, generate text files and figures of water transparency vs. day.
  - This code will run the following python codes by sequence.

`single_day_merge.py`
:  Merge the file from per run into per day.
   - Input the files that generate from `q_vs_dist.cc`, and output `Day_XXXX.root` files. 
   - Run numbers and corresponding days are reference from `/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat`. 
   - Generate `output/single_days_merge.sh` script. 
   
`pm7days_merge.py`
:  Merge the file from per run into plus minus 7 day (total 15 days).
   - Input the files that generate from `q_vs_dist.cc`, and output `Day7_XXXX.root` files.
   - Generate `output/pm7days_merge.sh` script. 

`Eff_dist_plot.py`
:  Plot the Effective hit versus distance plot.
   - Input the Root file and generate figure with python package uproot3 and matplotlib.
    
`Fitting_linear.py`
:  A fitting code for effective hit versus distance plot.
   - Input the ROOT file and output water tranrparency fitting result in text file. 
   - Linear fitting is done with python package scipy.optimize.curve_fit

`Fitting_yfixlinear.py`
:  A y-axis fixed fitting version of the Effective hit versus distance plot.
   - Fixed y-intercept value, -0.8082, is chosen from `Fitting_linear.py`.

`WT_trend_plot.py`
:  Plot the Water transparency plot for SV-V, VI and VII period.
   - Read the text file from `Fitting_yfixlinear.py` or `wt_history.cc`
   - Output water tranrparency trend figure.
   - Michel electrons water tranrparency results are prepared for comparision.
