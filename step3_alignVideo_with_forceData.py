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
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import os
from glob import glob
import numpy as np
import pandas as pd
from scipy import signal
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import seaborn as sn
import math
import errno

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

    return df_force_analysis_calib, data_rows_count, force_files, force_file_folder, foldername, tempdir


def extract_force_data_for_steps():
    # TODO: if there are multiple steps for 1 video it doesn't get the data!!! FIX
    # read in the dataframe from step2, containing footfalls and filenames etc.
    df_force_analysis_calib, data_rows_count, force_files, force_file_folder, foldername, tempdir = read_in_data()

    # add columns for extracted force data to this file:
    df_force_analysis_calib_forces = df_force_analysis_calib.reindex(columns=df_force_analysis_calib.columns.tolist()
                                                                             + ["MeanX", "MeanY", "MeanZ", "MinX",
                                                                                "MinY",
                                                                                "MinZ", "MaxX", "MaxY", "MaxZ"])

    # iterate through the rows to handle lizard step by step
    for row in range(data_rows_count):
        # extract current row:
        current_row = df_force_analysis_calib.loc[row,]
        print("\n\n Progress: \n", row + 1, "/", data_rows_count)

        current_video_file = current_row["file"]
        current_force_file = current_row["force_file"]
        foot_on_forceplate = current_row["foot"]
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

        print("current force file: ", current_force_file)

        if footfall_exists:
            # check if force file for the current_row exists:
            if os.path.join(force_file_folder, current_force_file) in force_files:
                force_file_exists = True
                print("force file {} exists: ".format(current_force_file), force_file_exists)
            else:
                force_file_exists = False
                print("force file for: {} doesn't exist!".format(current_force_file))

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
                footfall_begin_noBuffer = footfall_begin
                footfall_end_noBuffer = footfall_end
                footfall_length = footfall_end - footfall_begin
                footfall_length_perc = 100 * (footfall_length / video_frame_count)

                ### only use the foot falls which are shorter than 15% of the entire video!
                # This should filter steps where the gecko stops on the forceplate
                if footfall_length_perc < 50.0:

                    # print("footfall_begin original: ", footfall_begin_noBuffer,
                    #      "\nfootfall_end original: ", footfall_end_noBuffer)

                    # convert original begin and end to force data row so these can be plotted as vertical lines:
                    forceRow_footfall_begin_noBuffer = auxiliaryfunctions.convert_videoframe_to_forcerow(
                        video_frame_count,
                        video_frame_rate,
                        force_sampling_rate, trigger,
                        force_sampling_time_s,
                        footfall_begin_noBuffer)
                    forceRow_footfall_end_noBuffer = auxiliaryfunctions.convert_videoframe_to_forcerow(
                        video_frame_count,
                        video_frame_rate,
                        force_sampling_rate, trigger,
                        force_sampling_time_s,
                        footfall_end_noBuffer)

                    # print("forceRow_begin original: ", forceRow_footfall_begin_noBuffer,
                    #      "\nforceRow_end original: ", forceRow_footfall_end_noBuffer)

                    # set a 30% buffer in video frames to be added to either side of the footfall to make sure entire step is included
                    buffer = np.round(0.3 * footfall_length, 0)
                    footfall_begin = footfall_begin - buffer
                    footfall_end = footfall_end + buffer
                    footfall_length = footfall_end - footfall_begin

                    if footfall_begin > 0 and footfall_end > 0 and footfall_length > 5:

                        # print("footfall_begin: ", footfall_begin,
                        #      "\nfootfall_end: ", footfall_end)

                        # convert these footfall frames to force data rows
                        forceRow_footfall_begin = auxiliaryfunctions.convert_videoframe_to_forcerow(video_frame_count,
                                                                                                    video_frame_rate,
                                                                                                    force_sampling_rate,
                                                                                                    trigger,
                                                                                                    force_sampling_time_s,
                                                                                                    footfall_begin)
                        forceRow_footfall_end = auxiliaryfunctions.convert_videoframe_to_forcerow(video_frame_count,
                                                                                                  video_frame_rate,
                                                                                                  force_sampling_rate,
                                                                                                  trigger,
                                                                                                  force_sampling_time_s,
                                                                                                  footfall_end)
                        print("forceRow_footfall_begin: ", forceRow_footfall_begin,
                              "\nforceRow_footfall_end: ", forceRow_footfall_end)

                        # check if any of the returned force rows is nan, if so don't proceed:
                        checklist = [math.isnan(forceRow_footfall_begin_noBuffer),
                                     math.isnan(forceRow_footfall_end_noBuffer),
                                     math.isnan(forceRow_footfall_begin), math.isnan(forceRow_footfall_end)]

                        print("checklist: ", checklist)

                        if all(checklist) == False:
                            # read in force data from .txt file
                            df_forces = pd.read_csv(os.path.join(force_file_folder, current_force_file),
                                                    delimiter='\t', names=['Fx', 'Fy', 'Fz', 'Tx', 'Ty', 'Tz'])
                            print(df_forces.head())

                            #### smoothing and extraction of Mins, Means, Maxs, and integrals
                            dict_forces_summary = do_all_the_force_data_extraction_and_stuff(forceRow_footfall_begin,
                                                                                             forceRow_footfall_end,
                                                                                             df_forces,
                                                                                             current_force_file,
                                                                                             forceRow_footfall_begin_noBuffer,
                                                                                             forceRow_footfall_end_noBuffer,
                                                                                             foot_on_forceplate,
                                                                                             tempdir)

                            # writing the dict_forces_summary to the df_forceAnalysis_calib:
                            print("filling in extracted force data...")
                            index_current_force_file = df_force_analysis_calib.index[
                                df_force_analysis_calib["force_file"] == current_force_file].tolist()[0]
                            for force_element, force_value in dict_forces_summary.items():
                                # print("force_element: ", force_element,
                                #      "force_value: ", force_value)
                                df_force_analysis_calib_forces.loc[
                                    index_current_force_file, force_element] = force_value

                            # print("\nfilled in force data: \n", df_force_analysis_calib_forces.head(20))

                            # create force vector overlay of normalized forces over lizard videos --> needs angle of force,
                            # display z force as circle on foot with alpha changing according to normalized Fz

                else:
                    print("very long step, likely paused on FP, proceed to next...")

        else:
            print("next row")

    # save df_force_analysis_calib_forces as csv
    auxiliaryfunctions.write_df_to_csv(tempdir, "{}_forceAnalysis_calib_forces.csv".format(foldername),
                                       df_force_analysis_calib_forces)


def do_all_the_force_data_extraction_and_stuff(forceRow_footfall_begin, forceRow_footfall_end, df_forces,
                                               current_force_file,
                                               forceRow_footfall_begin_noBuffer, forceRow_footfall_end_noBuffer,
                                               foot_on_forceplate, tempdir):
    """
    This function handles plotting of raw and smoothed force data for the footfall as well as the extraction of Min, Mean and Max values.
    It returns a dictionary with these extracted values for the current footfall.
    :param forceRow_footfall_begin: force row equivalent to footfall begin frame of video including the buffer
    :param forceRow_footfall_end: force row equivalent to footfall end frame of video including the buffer
    :param df_forces: the raw force data for the current file
    :param current_force_file: the name of the current force data file
    :param forceRow_footfall_begin_noBuffer: force row equivalent to original footfall begin frame of video
    :param forceRow_footfall_end_noBuffer: force row equivalent to original footfall end frame of video
    :return: dictionary containing Min, Mean and Max for Fx, Fy, Fz
    """
    # print("df force data shape: ", df_forces.shape)

    x_col = 0
    y_col = 1
    z_col = 2

    testplot = False
    save_figures = False

    #### get the bsaeline offset for the three forces:
    Fx_baselineOffset = np.nanmean(df_forces.iloc[5000:10000, x_col])
    Fy_baselineOffset = np.nanmean(df_forces.iloc[5000:10000, y_col])
    Fz_baselineOffset = np.nanmean(df_forces.iloc[5000:10000, z_col])

    print("force data baselines:,"
          "\nFx offset: ", Fx_baselineOffset,
          "\nFy offset: ", Fy_baselineOffset,
          "\nFz offset: ", Fz_baselineOffset)

    #### extract original footfall and footfall with buffer range from force data:
    # with buffer
    Fx_footfall = df_forces.iloc[forceRow_footfall_begin:forceRow_footfall_end, x_col]
    Fy_footfall = df_forces.iloc[forceRow_footfall_begin:forceRow_footfall_end, y_col]
    Fz_footfall = df_forces.iloc[forceRow_footfall_begin:forceRow_footfall_end, z_col]

    # original
    Fx_footfall_noBuffer = df_forces.iloc[forceRow_footfall_begin_noBuffer:forceRow_footfall_end_noBuffer, x_col]
    Fy_footfall_noBuffer = df_forces.iloc[forceRow_footfall_begin_noBuffer:forceRow_footfall_end_noBuffer, y_col]
    Fz_footfall_noBuffer = df_forces.iloc[forceRow_footfall_begin_noBuffer:forceRow_footfall_end_noBuffer, z_col]

    # print("Fx footfall before baselining: \n", Fx_footfall[1:5])
    #### baseline the extracted force data arrays:
    Fx_footfall = baseline_forces(Fx_footfall, Fx_baselineOffset)
    Fy_footfall = baseline_forces(Fy_footfall, Fy_baselineOffset)
    Fz_footfall = baseline_forces(Fz_footfall, Fz_baselineOffset)

    Fx_footfall_noBuffer = baseline_forces(Fx_footfall_noBuffer, Fx_baselineOffset)
    Fy_footfall_noBuffer = baseline_forces(Fy_footfall_noBuffer, Fy_baselineOffset)
    Fz_footfall_noBuffer = baseline_forces(Fz_footfall_noBuffer, Fz_baselineOffset)

    # print("Fx footfall after baselining: \n", Fx_footfall[1:5])

    #### smooth force data:
    # Butterworth filter
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)  # order, cut-off frequency

    # lowpass filter for foot motion
    print("smoothing force data...")
    print("length of vectors:"
          f"\n Fx: {len(Fx_footfall)},"
          f"\n Fy: {len(Fy_footfall)},"
          f"\n Fz: {len(Fz_footfall)}")
    Fx_footfall_smoothed = signal.filtfilt(b, a, Fx_footfall)
    Fy_footfall_smoothed = signal.filtfilt(b, a, Fy_footfall)
    Fz_footfall_smoothed = signal.filtfilt(b, a, Fz_footfall)

    x_values = range(forceRow_footfall_begin, forceRow_footfall_end)

    print(f"forceRow_begin: {forceRow_footfall_begin},\n"
          f"forceRow_end: {forceRow_footfall_end}")

    print(f"length of Fx: {len(Fx_footfall)},\n"
          f"length of x values: {len(x_values)}")

    if testplot == True:
        print("plotting...")
        #### let's do a testplot:
        sn.lineplot(x_values, Fx_footfall, color='grey', label="Fx raw")
        sn.lineplot(x_values, Fx_footfall_smoothed, color='black', label="Fx smoothed")
        sn.lineplot(x_values, Fy_footfall, color='lightgreen', label="Fy raw")
        sn.lineplot(x_values, Fy_footfall_smoothed, color='darkgreen', label="Fy smoothed")
        sn.lineplot(x_values, Fz_footfall, color='lightblue', label="Fz raw")
        sn.lineplot(x_values, Fz_footfall_smoothed, color='darkblue', label="Fz smoothed")
        plt.hlines(xmin=forceRow_footfall_begin, xmax=forceRow_footfall_end, y=0, linewidth=0.8)
        plt.vlines(ymin=min(Fz_footfall_smoothed), ymax=max(Fz_footfall_smoothed), x=forceRow_footfall_begin_noBuffer)
        plt.vlines(ymin=min(Fz_footfall_smoothed), ymax=max(Fz_footfall_smoothed), x=forceRow_footfall_end_noBuffer)

        plt.title(current_force_file + " - " + foot_on_forceplate)
        plt.legend()
        plt.xlabel('force frames')
        plt.ylabel('Force in N')

        # save figures:
        if save_figures == True:
            try:
                os.makedirs(os.path.join(tempdir, "force_plots"))
                print(f"folder for saving the plots created: {tempdir}")
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            plt.savefig(os.path.join(tempdir, "force_plots", f"{current_force_file} - {foot_on_forceplate}.jpg"))
            plt.close()
        else:
            plt.show()

    ### Extract mins, mean, max and integral from the smoothed force data between original range (noBuffer)
    # create an empty dataframe to store:
    # MeanX, MeanY, MeanZ, IntegralX, IntegralY, IntegralZ, MinX, MinY, MinZ, MaxX, MaxY, MaxZ
    # for now leave integrals as the issue exists that force curves cross 0 within footfall...
    dict_keys = ["MeanX", "MeanY", "MeanZ", "MinX", "MinY", "MinZ", "MaxX", "MaxY", "MaxZ"]
    dict_forces_summary = {new_key: [] for new_key in dict_keys}  # initializes empty dict with above keys
    dict_forces_summary["MeanX"] = round(np.nanmean(Fx_footfall_noBuffer), 3)
    dict_forces_summary["MeanY"] = round(np.nanmean(Fy_footfall_noBuffer), 3)
    dict_forces_summary["MeanZ"] = round(np.nanmean(Fz_footfall_noBuffer), 3)
    dict_forces_summary["MinX"] = np.nanmin(Fx_footfall_noBuffer)
    dict_forces_summary["MinY"] = np.nanmin(Fy_footfall_noBuffer)
    dict_forces_summary["MinZ"] = np.nanmin(Fz_footfall_noBuffer)
    dict_forces_summary["MaxX"] = np.nanmax(Fx_footfall_noBuffer)
    dict_forces_summary["MaxY"] = np.nanmax(Fy_footfall_noBuffer)
    dict_forces_summary["MaxZ"] = np.nanmax(Fz_footfall_noBuffer)

    # return this and write these column entries to appropriate row (current force file) in the df_force_analysis_calib dataframe

    return dict_forces_summary


def baseline_forces(force_array, force_base):
    """
    This function takes a list with force values and the offset value for this force and returns the baselined list.
    :param force_array:
    :param force_base: value of force offset averaged from beginning of force track.
    Calculated in do_all_the_force_data_extraction_and_stuff()
    :return: baselined force array
    """
    force_array_baselined = [round(x - force_base, 5) for x in force_array]

    return force_array_baselined
