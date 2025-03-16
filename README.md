# water_t_nGd

## General description

- This code analysis neutron captured Gd photon on water transparency.
- A text file of water transparency vs. day will be generated.

## Codes

`src/q_vs_dist.cc` 
:  Make charge vs. distance plot for each run
  - Select neutron events 
  - Selected those dense hit area (divide Cerenkov ring in 36 segments).
  - Calculate the charge and distance in each hit area.
    - Corrections are applied in the similar way as we do in calculation of Neff

`submit.py`  
:  Run `q_vs_dist.cc` for all runs

`src/wt_history.cc`  
:  Read output files from `q_vs_dist.cc` and output the text file of water transparency vs. day.
  - Merge data for calculating a running average. 
  - Fitting the charge vs. distance for the merged data for each day

`analysis/data_handler.py`
:  Classes for handling data operations.
   - `DataHandler`: Abstract base class for data handling
   - `RootDataHandler`: Handler for ROOT file data
   - `RunDataHandler`: Handler for run data and file operations

`analysis/merger.py`
:  Classes for merging operations.
   - `Merger`: Abstract base class for merging operations
   - `SingleDayMerger`: Class for merging files by single day
   - `PlusMinusSevenDayMerger`: Class for merging files with ±7 days range

`analysis/fitter.py`
:  Classes for fitting operations.
   - `Fitter`: Abstract base class for fitting operations
   - `LinearFitter`: Class for linear fitting with two parameters
   - `FixedYInterceptFitter`: Class for linear fitting with fixed y-intercept

`analysis/plotter.py`
:  Classes for plotting operations.
   - `Plotter`: Abstract base class for plotting operations
   - `EfficiencyDistancePlotter`: Class for plotting efficiency vs distance
   - `WTTrendPlotter`: Class for plotting WT trend

`analysis/analysis.py`
:  Main class for orchestrating the analysis workflow.
   - `WTAnalysis`: Main class that coordinates all operations

`analysis/run_analysis.py`
:  Script to run the analysis with command line arguments.

See `analysis/README.md` for detailed documentation on how to use the analysis code.


## How to use

1. Update bad run list called badsub.sk?.manual.local. It will be used by lfbadrun_local.F.
1. Update subroutines and parameters in `src/q_vs_dist.cc` to use the latest version. All relevant parameters can be found in the first 50 lines.
    - Fortran subroutines are decleared in `extern "C" {}`.
    - Parameters are decleared at the beginning of the `main()` function.
1. `make` to compile
1. Change the data directory path defined in the top part of `submit.py` 
1. Run `./submit.py` (This part takes ~2 hours.)
    - Output ROOT files will be generated in `data/` directory.
    - Log files of the jobs will be generated in `log/` directory.
1. Run `./bin/wt_history`
    - `wt_new.txt` will be generated.
1. Run `./analysis/wt_analysis.py` (This part takes ~15 minutes.)
    - `WTFit_yfix_result.txt` and relative figures will be generated.
