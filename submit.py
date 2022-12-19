#!/usr/bin/env python

import os, glob, time, subprocess

# Make a list of files
#file_list = glob.glob('/disk02/lowe8/sk6/sle/lomugd.08????.root')
#file_list.extend(glob.glob('/disk02/lowe9/sk6/sle/lomugd.08????.root'))
#file_list.extend(glob.glob('/disk03/lowe10/sk7/sle/lomugd.08????.root'))
file_list= (glob.glob('/disk03/lowe10/sk7/sle/lomugd.09????.root'))
file_list.sort()

# Loop for files
for file_this in file_list:

    # Get run number from filename
    run_this = int(file_this[-11:-5])
    print(run_this)

    # Make a script file
    f_script_name = 'script/watert_%06d.csh' % run_this
    f_script = open(f_script_name, 'w')
    f_script.write('#!/bin/csh -f\n\n')
    f_script.write('cd /disk02/usr7/licheng/nGd_gitlab\n')
    f_script.write('./bin/q_vs_dist output/wt_{0}.root {1}'.format('%06d' % run_this, file_this))
    f_script.close()

    # Submit a job
    os.system('pjsub -X -L rscgrp=all -j -o log/out.%06d.log %s' % (run_this, f_script_name))

    # Check number of running jobs
    while True:
        njobs = int(subprocess.check_output('pjstat | wc -l', shell=True).decode())-1
        if njobs > 500:
            print('Njobs=%d. Wait 10 sec ... run%d' % (njobs, run_this))
            time.sleep(10)
        else:
            break
