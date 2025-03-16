import pandas as pd
import os, glob, time, subprocess

def Read_datapath():

    #Define data path
    testdir = 'output'
    workdir = '/disk02/usr7/licheng/nGd_gitlab/' + testdir

    # Get run number and Days
    data = pd.read_csv(\
           '/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat'\
           , delimiter= '\s+', names = ['run','a','b','c','d','e','f','day'] )

    # Make a list of files
    file_list = glob.glob('/disk02/usr7/licheng/nGd_gitlab/output/wt_0?????.root')
    file_list.sort()

    return(data, workdir, file_list)

def single_day_merge(data, workdir, file_list):
    # Initialize the day
    today = -1
    jobname = workdir + '/single_day_merge.sh'

    # Make a script file
    f = open(jobname,'w')
    f.write('#!/bin/bash\n')
    f.write('cd %s \n' %(workdir))
    f.write('date\n')

    # Get the last day
    lastrun = int(file_list[-2][-11:-5])
    lastindex = data[data['run']==lastrun].index
    lastday = int(data.day[lastindex])

    for file_this in file_list:
        # Get run number from filename
        run_number = int(file_this[-11:-5])
        index = data[data['run']==run_number].index
        # Get the day that corresponding to run number
        run_day = int(data.day[index])
        # Skip last day
        if (run_day == lastday):
            break
        run_day1 = int(data.day[index+1])
    
        # If this day is a new day, add a merge file name at the beginning
        if (today != run_day):
            today = run_day
            f.write('hadd -f ' + workdir + '/Day_' + str(today) + '.root ')
        # if next run is a new day, write this run and add new line
        if (today != run_day1):
            f.write(workdir + '/wt_0' + str(run_number) + '.root ' + '\n')
        # if next run is same day, write this run without adding new line
        if (today == run_day1):
            f.write(workdir + '/wt_0' + str(run_number) + '.root ')

    f.close()
        

    


