import pandas as pd
import math
import os, glob, time, subprocess

def Read_datapath():

    #Define data path
    workdir = '/disk02/usr7/licheng/nGd_gitlab/output' 

    # Get run number and Days
    data = pd.read_csv(\
           '/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat'\
           , delimiter= '\s+', names = ['run','a','b','c','d','e','f','day'] )

    # Make a list of files
    file_list = glob.glob('/disk02/usr7/licheng/nGd_gitlab/output/wt_0?????.root')
    file_list.sort()

    return(data, workdir, file_list)

def plus_minus_7day_merge(data, workdir, file_list):
    # Define output data name
    jobname = workdir + '/pm7days_merge.sh'

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

        # Break if the data is less then 7 days
        if ( (lastday-run_day) < 7):
            break
            
        # input day and get the run number and run name 
        def find_run(i):
            index = (data[data['day']==(run_day+i)].index)
            if (i<0):
                run_num = data.run[index].min()
            else: 
                run_num = data.run[index].max()
        
            run_name = workdir + '/wt_0' + str(run_num) + '.root'
            return run_num, run_name

        # Find the run number of -7 days 
        if (~math.isnan(find_run(-7)[0])):
            range_low = find_run(-7)
        else : 
            continue

        # Find the run number of +7 days
        if (~math.isnan(find_run(+7)[0])):
            range_high = find_run(+7)
        else: 
            continue
 
        # Check if low bound and high bound exist
        condition1 = (len(str(range_low[0]))+len(str(range_high[0])))==10
        condition2 = (range_low[1] in file_list)
        condition3 = (range_high[1] in file_list)
    
        # Check if this run is the last run in a day
        condition4 = (int(data.day[index]) != int(data.day[index+1]))    

        if (condition1 and condition2 and condition3 and condition4):
        
            # Print out the day and upper/lower bound days
            #print(run_day)
            #print(range_low[0],range_high[0])

            # Define merge file name
            f.write('hadd -f ' + workdir + '/Day7_' + str(run_day) + '.root ')

            # Loop to write the merge file list
            for i in range(int(range_low[0]),int(range_high[0])+1):
                # Check if the file exist
                if ((workdir + '/wt_0' + str(i) + '.root') in file_list):
                    # Write the file name 
                    f.write(workdir + '/wt_0' + str(i) + '.root ')
            # New line for next day
            f.write('\n ')

    f.close()
        
