#!/usr/bin/env python3
"""
Script to run the refactored WT analysis.
This script demonstrates how to use the refactored OOP-based code.
"""

import os
import sys
from analysis.refactored.analysis import WTAnalysis


def main():
    """Main function to run the analysis with command line arguments."""
    # Get command line arguments or use defaults
    if len(sys.argv) > 1:
        workdir = sys.argv[1]
    else:
        workdir = '/disk02/usr7/licheng/nGd_gitlab/output'
    
    if len(sys.argv) > 2:
        runsum_path = sys.argv[2]
    else:
        runsum_path = '/usr/local/sklib_gcc8/skofl-trunk/const/lowe/runsum.dat'
    
    # Print configuration
    print(f"Running WT analysis with:")
    print(f"  Working directory: {workdir}")
    print(f"  Runsum path: {runsum_path}")
    
    # Create analysis object
    analysis = WTAnalysis(workdir, runsum_path)
    
    # Run full analysis
    print("\nRunning full analysis workflow...")
    analysis.run_analysis()
    
    # Alternatively, run individual steps
    # print("\nRunning individual steps...")
    # analysis.setup()
    # analysis.merge_files()
    # analysis.perform_fitting()
    # analysis.create_plots()
    
    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
