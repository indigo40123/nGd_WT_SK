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

`analysis/wt_analysis.py`
:  Summarized the analysis codes, generate text files and figures of water transparency vs. day.
  - This code will run the following python codes by sequence.

`analysis/single_day_merge.py`
:  Merge the file from per run into per day.
   - Input the files that generate from `q_vs_dist.cc`, and output `Day_XXXX.root` files. 
   - Run numbers and corresponding days are reference from `/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat`. 
   - Generate `output/single_days_merge.sh` script. 
   
`analysis/pm7days_merge.py`
:  Merge the file from per run into plus minus 7 day (total 15 days).
   - Input the files that generate from `q_vs_dist.cc`, and output `Day7_XXXX.root` files.
   - Generate `output/pm7days_merge.sh` script. 

`analysis/Eff_dist_plot.py`
:  Plot the Effective hit versus distance plot.
   - Input the Root file and generate figure with python package uproot3 and matplotlib.
    
`analysis/Fitting_linear.py`
:  A fitting code for effective hit versus distance plot.
   - Input the ROOT file and output water tranrparency fitting result in text file. 
   - Linear fitting is done with python package scipy.optimize.curve_fit

`analysis/Fitting_yfixlinear.py`
:  A y-axis fixed fitting version of the Effective hit versus distance plot.
   - Fixed y-intercept value, -0.8082, is chosen from `Fitting_linear.py`.

`analysis/WT_trend_plot.py`
:  Plot the Water transparency plot for SV-V, VI and VII period.
   - Read the text file from `Fitting_yfixlinear.py` or `wt_history.cc`
   - Output water tranrparency trend figure.
   - Michel electrons water tranrparency results are prepared for comparision.


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
