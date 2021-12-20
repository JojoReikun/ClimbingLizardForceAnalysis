"""
!! FOLDER PATHS AND FILE NAMES ARE ALL HARDCODED ATM!!

This module will calculate the toppling moments over the time of a stride of lizards 
(currently made for hfren for Lizard Paper) up vs down. 

Because we only have one foot at a time for forces BUT for dynamic analysis we would need "live" data for fore and pair
hind foot at the same time, average force curve profiles for one individual for each foot were calculated.
(in hfren_strideDynamics.py)

TODO: export average force profiles as data arrays to be accessible to this module.

For the calculations the following things are needed:
- Forces for the stride (average force profiles)
- Length between the fore and hind foot attached (add to DOKA)
- height of the BCOM compared to wall
- mass of lizards
"""

#### IMPORTS:
from glob import glob
import pandas as pd
import numpy as np
import os

bodymasses_dict = {"hfren11": 2.75,
                   "hfren13": 3.25,
                   "hfren14": 3.87,
                   "hfren16": 3.47,
                   "hfren17": 2.30,
                   "hfren18": 3.53}     # grams

h = 0.004  # m
g = 9.81   # m/s^2


def loop_encode(i):
    # get utf-8 encoded version of the string
    cell_value = 'stance000{}'.format(i).encode()
    # print("-----> stance phase cell value :", cell_value)
    return cell_value


def calc_toppling_moment(g, h, forceZ_FR_i, forceZ_FL_i, forceZ_HR_i, forceZ_HL_i, length_FL_i, length_FR_i, individual, foot):
    # calculates the toppling moment around the hindfoot, assuming only a 2D view of the scene
    # and assuming the tail is not a contact point on the wall.
    if foot == "FL":
        Fn_z_i = forceZ_FL_i
        length = length_FL_i
    elif foot == "FR":
        Fn_z_i = forceZ_FR_i
        length = length_FR_i

    m = bodymasses_dict[individual]/1000    # to get mass in kg
    moment = h * m * g + Fn_z_i * length

    return moment


def hfren_climbing_moments():
    #### DEFINE FILE LOCATIONS AND NAMES:
    # file naming: e.g. hfren11_down_03_hflipDLC_resnet50_lizardpaper21GJun15shuffle1_500000.csv
    doka_hfren_folder = r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardDLCAnalysis\lizardanalysis\lizardpaper21-js-hfren-2021-06-28\analysis-results'
    doka_files_list = glob(os.path.join(doka_hfren_folder, "*.csv"))

    force_file_folder = r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardForceAnalysis_2020\forceData_hfren\correctedForces\average_force_profiles'
    # filenaming = e.g. avg_force_down_hfren11_FR.csv

    # go through DLC result files of lizards to iterate through all strides
    for doka_file in doka_files_list:
        # read in the DOKA data
        kin_data = pd.read_csv(doka_file)
        kin_data.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
        data_rows_count = kin_data.shape[0]  # number of rows

        filename = doka_file.rsplit(os.sep, 1)[1]
        print("\n------> current file: ", filename)
        print(kin_data.head())
        individual = filename.split("_", 1)[0]
        direction = filename.split("_", 2)[1]
        print("individual: ", individual, "direction: ", direction)

        active_columns = {"stepphase_FL": "FL",
                          "stepphase_FR": "FR"}
        max_step_count = 1000

        # find matching averaged foot force profiles for individual:
        force_profile_FR = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_FR.csv"))
        force_profile_FL = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_FL.csv"))
        force_profile_HR = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_HR.csv"))
        force_profile_HL = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_HL.csv"))

        # only z axis forces (normal forces) are needed for topplling moments:
        force_profile_FR["avg_Fz"]
        force_profile_FL["avg_Fz"]
        force_profile_HR["avg_Fz"]
        force_profile_HL["avg_Fz"]

        force_array_length = len(force_profile_FR)

        for col, foot in active_columns.items():
            col = col.strip('')
            for i in range(1, max_step_count):
                stance_moments = []
                stance_counter = loop_encode(i)
                kin_data_stance_section = kin_data[kin_data[col] == stance_counter]
                # TODO: FIX! kin_data_stance_section is always empty...
                print("kin_data_stance_section: ", kin_data_stance_section)

                print(f"col: {col}, foot: {foot}, stance counter: {stance_counter}")

                if len(kin_data_stance_section) == 0:   # could change this to a filter for stance sections > 5 too
                    print("stance section is length 0... break")
                    break

                else:
                    df_stance_section_indices = list(kin_data_stance_section.index.values)  # list of stance indices
                    stance_length = len(df_stance_section_indices)
                    print("stance_length: ", stance_length)

                    ####### CALCULATE THE TOPPLING MOMENTS:
                    # depending on the stancelength, that many equally spread data points of the force data will be used
                    force_array_interval = round(force_array_length / stance_length) - 1
                    force_profile_FR_points = [force_profile_FR[n*force_array_interval] for n in range(stance_length)]
                    force_profile_FL_points = [force_profile_FL[n*force_array_interval] for n in range(stance_length)]
                    force_profile_HR_points = [force_profile_HR[n*force_array_interval] for n in range(stance_length)]
                    force_profile_HL_points = [force_profile_HL[n*force_array_interval] for n in range(stance_length)]

                    for i in range(stance_length):
                        toppling_moment = calc_toppling_moment(g, h, force_profile_FR_points[i], force_profile_FL_points[i],
                                             force_profile_HR_points[i], force_profile_HL_points[i],
                                             kin_data_stance_section["dyn_footpair_height_FL"][i],
                                             kin_data_stance_section["dyn_footpair_height_FR"][i], individual, foot)

                        stance_moments.append(toppling_moment)

                    print(f" moments: {stance_moments}")

    return