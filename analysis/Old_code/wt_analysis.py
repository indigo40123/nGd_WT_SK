import os, glob, time, subprocess
from single_day_merge import single_day_merge
from pm7days_merge import Read_datapath, plus_minus_7day_merge
from Fitting_linear import WT_fitting
from Fitting_yfixlinear import WT_fitting_yfix
from WT_trend_plot import WT_Plot
from Eff_dist_plot import Eff_Dist_Plot

# Read path and run-day reference file
run_day_ref = Read_datapath()[0]
workdir = Read_datapath()[1]
file_list = Read_datapath()[2]

# Generate Merge script
plus_minus_7day_merge(run_day_ref, workdir, file_list)
single_day_merge(run_day_ref, workdir, file_list)

# Merge the root file from per run to per day (It takes 5~10 minutes)
os.system('source ' + workdir + '/single_day_merge.sh')
os.system('source ' + workdir + '/pm7days_merge.sh')

# Fitting the WT trend
WT_fitting(workdir)
WT_fitting_yfix(workdir)

# Plot out the Effective hit v.s. distance
Eff_Dist_Plot(workdir)

# Plot out the WT trend 
WT_Plot()
