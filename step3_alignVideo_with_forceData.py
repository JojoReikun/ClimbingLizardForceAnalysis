"""
STEP 3:
This step uses the data frame from step 2 (e.g.: "Gecko01_forceAnalysis_calib.csv"), which includes frame count and frame
rate of each video, and aligns the videos with the respective force data...

Requires: folder with all force data .txt files which are names in the same way as it's saved in the data frame:
--> e.g.: gdub2_down_23.txt

All force data files for the geckos are stored in folder: forceData_geckos

TODO:

- read in the data frame from step2 if it exists
- loop through all rows:
    - get frame count and frame rate of video
    - get number of force data rows per frame of video --> sampling rate force/video frame rate
    - e.g.: gdub2_up_22
        video length: 405
        video frame rate: 250
        if foot fall at frame 180 --> this corresponds to force row:
        90000 - (405-180)*(10000/250) = 81000
        the footfall at frame 180 in the video file should be equivalent to row 81000 in the force data file

    - get max, min, mean forces from footfall area
    - plot (also plot vectors over video?)
"""

#### IMPORTS:
import os
from glob import glob
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sn
import math

import auxiliaryfunctions


def read_in_data():
    #### DEFINE FILE LOCATIONS AND NAMES:
    destfolder = current_path = os.getcwd()

    tempdir = auxiliaryfunctions.open_gui_to_select_folder(
        'STEP3: Please select a directory containing lizard videos (e.g.: "ClimbingLizardVideos_2020/Gecko02/video_analysis")')
    # e.g. tempdir = "C:/Users/JojoS/Documents/phd/ClimbingRobot_XGen4/ClimbingLizardsVideos_2020/Gecko01/videos_analysis"

    # assumes that videos are in video_analysis inside the folder for the Group [-2]:
    foldername = auxiliaryfunctions.splitall(tempdir)[-2]
    # print("foldername: ", foldername)   # e.g. Dragon03

    force_analysis_file = "{}_forceAnalysis_calib.csv".format(foldername)

    force_file_folder = auxiliaryfunctions.open_gui_to_select_folder(
        'Please select the folder containing all the .txt force data files')

    ### read in the data frame from step2:
    # looks for and reads in "*_forceAnalysis_calib.csv" file in tempdir folder:
    df_force_analysis_calib = pd.read_csv(os.path.join(tempdir, force_analysis_file))

    df_force_analysis_calib.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
    data_rows_count = df_force_analysis_calib.shape[0]  # number of rows already excluded the header

    ### make list with all available force data files:
    force_files = glob(os.path.join(force_file_folder, '*.txt'))

    return df_force_analysis_calib, data_rows_count, force_files, force_file_folder


def extract_force_data_for_steps():
    # read in the dataframe from step2, containing footfalls and filenames etc.
    df_force_analysis_calib, data_rows_count, force_files, force_file_folder = read_in_data()

    # iterate through the rows to handle lizard step by step
    for row in range(data_rows_count):
        # extract current row:
        current_row = df_force_analysis_calib.loc[row, ]
        print("\n\n Progress: \n", row, "/", data_rows_count)

        current_video_file = current_row["file"]
        current_force_file = current_row["force_file"]
        print("File: ", current_video_file)

        ### check if there is a valid footfall entered:
        check_columns = ["footfall_begin", "footfall_end"]
        checked = []
        for col in check_columns:
            if math.isnan(current_row[col]):
                checked.append(False)
                print("no values found for {}, proceeding to next...".format(col))
            else:
                checked.append(True)

        print("checked: ", checked)
        if all(checked) == False:
            footfall_exists = False

        else:
            footfall_exists = True
            print("footfall_exists, proceed...")


        print("current force file: ", current_force_file,
              "\nforce files: \n", force_files)

        if footfall_exists:
            # check if force file for the current_row exists:
            if os.path.join(force_file_folder, current_force_file) in force_files:
                force_file_exists = True
            else:
                force_file_exists = False
            print("force file exists: ", force_file_exists)

            if force_file_exists:
                #### Now we can align the data and extract the values :)
                # get all the info about the lizard video:
                video_frame_count = current_row["video_frame_count"]
                video_frame_rate = current_row["framerate"]
                force_sampling_rate = 10000.0
                trigger = 9000.0
                force_sampling_time_s = 10.0

                footfall_begin = current_row["footfall_begin"]
                footfall_end = current_row["footfall_end"]
                footfall_length = footfall_end - footfall_begin

                # set a 10% buffer in video frames to be added to either side of the footfall to make sure entire step is included
                buffer = np.round(0.1 * footfall_length, 0)
                footfall_begin = footfall_begin - buffer
                footfall_end = footfall_end + buffer

                # convert these footfall frames to force data rows
                forceRow_footfall_begin = convert_videoframe_to_forcerow(video_frame_count, video_frame_rate, force_sampling_rate, trigger, force_sampling_time_s, footfall_begin)
                forceRow_footfall_end = convert_videoframe_to_forcerow(video_frame_count, video_frame_rate, force_sampling_rate, trigger, force_sampling_time_s, footfall_end)
                print("forceRow_footfall_begin: ", forceRow_footfall_begin,
                      "\nforceRow_footfall_end: ", forceRow_footfall_end)

                # read in force data from .txt file
                df_forces = pd.read_csv(os.path.join(force_file_folder, current_force_file),
                                        delimiter='\t', names=['Fx', 'Fy', 'Fz', 'Tx', 'Ty', 'Tz'])
                print(df_forces.head())

                # smoothing??
                do_all_the_force_data_extraction_and_stuff(forceRow_footfall_begin, forceRow_footfall_end, df_forces, current_force_file)

                # extract Mins, Means, and Maxs from within the forceRow range

                # calculate the integral from within the forceRow range

        else:
            print("next row")


def convert_videoframe_to_forcerow(video_frame_count, video_frame_rate, force_sampling_rate, trigger, force_sampling_time_s, video_frame):
    forceRow = (trigger*force_sampling_time_s) - ( (video_frame_count-video_frame) * (force_sampling_rate/video_frame_rate) )

    return int(forceRow)


def do_all_the_force_data_extraction_and_stuff(forceRow_footfall_begin, forceRow_footfall_end, df_forces, current_force_file):
    print("df force data shape: ", df_forces.shape)

    testplot = True

    #### smooth force data:
    Fx_footfall = df_forces.iloc[forceRow_footfall_begin:forceRow_footfall_end, 1]
    Fy_footfall = df_forces.iloc[forceRow_footfall_begin:forceRow_footfall_end, 2]
    Fz_footfall = df_forces.iloc[forceRow_footfall_begin:forceRow_footfall_end, 3]

    print("force data for footfall:\n,"
          "Fx: ", Fx_footfall,
          "\nFy: ", Fy_footfall,
          "\nFz: ", Fz_footfall)

    # Butterworth filter
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False) # order, cut-off frequ

    # lowpass filter for foot motion
    print("smoothing force data...")
    Fx_footfall_smoothed = signal.filtfilt(b, a, Fx_footfall)
    Fy_footfall_smoothed = signal.filtfilt(b, a, Fy_footfall)
    Fz_footfall_smoothed = signal.filtfilt(b, a, Fz_footfall)

    x_values = range(forceRow_footfall_begin, forceRow_footfall_end)

    if testplot == True:
        print("plotting...")
        #### let's do a testplot:
        sn.lineplot(x_values, Fx_footfall, color='grey')
        sn.lineplot(x_values, Fx_footfall_smoothed, color='black')
        sn.lineplot(x_values, Fy_footfall, color='lightgreen')
        sn.lineplot(x_values, Fy_footfall_smoothed, color='darkgreen')
        sn.lineplot(x_values, Fz_footfall, color='lightblue')
        sn.lineplot(x_values, Fz_footfall_smoothed, color='darkblue')
        plt.hlines(xmin=forceRow_footfall_begin, xmax=forceRow_footfall_end, linewidth=0.8)

        plt.title(current_force_file)

        plt.show()

    return



