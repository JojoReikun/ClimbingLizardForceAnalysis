"""
Hfren geckos:
This module generates an average force profile for each foot for each individual for each direction.
Because there are multiple files per run needed to do so (corrected force file, force output, DLC output, morph data),
use the hfren_filename_matching_chart.csv to grab the right file for each.

The script loops through all the extracted force steps using the force output data, given there are cases with multiple
steps per video.

1st: iterate through force_output rows and read in all matching files
2nd: get the stride of focus and figure out matching force rows using the force collection parameters
3rd: normalize the stride (forces)

Saves an array of force values of a normalised length to a dict which contains the data for each direction, individual, and foot
There is one dict for each force axis and the foot dicts can contain multiple arrays (representing multiple strides with this combination)

4th: get all strides to the same length --> average force stride length (scipy.interpolate),
        build average force profile and get sd and plot

"""

### Imports:
import pandas as pd
import numpy as np
import os
import scipy.interpolate as interp
import matplotlib.pyplot as plt


### Set up:
force_sync_file_path = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\forceData_hfren\correctedForces\Gecko_forces_sync_output.csv'
filename_match_path = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\hfren_filename_matching_chart.csv'

# force collection parameters:
sample_rate = 10000
trigger = 9000
length = 10
framerate = 250
Cfact = sample_rate/framerate

interpolation_plots = False


def hfren_strideDynamics():
    force_sync_file = pd.read_csv(force_sync_file_path, skipinitialspace=True)
    filematch_file = pd.read_csv(filename_match_path, skipinitialspace=True)

    # strip whitespaces from column names:
    force_sync_file.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
    filematch_file.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names

    print(force_sync_file.head(), list(force_sync_file.columns))

    # find the average stride length:
    average_force_stride_length = round(np.nanmean(abs(force_sync_file['footfall_begin'] - force_sync_file['footfall_end'])*Cfact))
    print("\n\naverage_force_stride_length: ", average_force_stride_length, "\n")

    ### initiate result dictionaries (1 for each force axis) for interpolated force arrays:
    # format: dict_Fx = {'direction': {'individual': {'foot': [ [array1], [array2], ...] }}}
    res_dict_Fx = {'up': {
        'hfren11': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren13': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren14': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren16': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren17': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren18': {'FR': [], 'FL': [], 'HR': [], 'HL': []}
    },
        'down': {
            'hfren11': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren13': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren14': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren16': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren17': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren18': {'FR': [], 'FL': [], 'HR': [], 'HL': []}
        }}

    res_dict_Fy = {'up': {
        'hfren11': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren13': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren14': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren16': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren17': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren18': {'FR': [], 'FL': [], 'HR': [], 'HL': []}
    },
        'down': {
            'hfren11': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren13': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren14': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren16': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren17': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren18': {'FR': [], 'FL': [], 'HR': [], 'HL': []}
        }}

    res_dict_Fz = {'up': {
        'hfren11': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren13': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren14': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren16': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren17': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
        'hfren18': {'FR': [], 'FL': [], 'HR': [], 'HL': []}
    },
        'down': {
            'hfren11': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren13': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren14': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren16': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren17': {'FR': [], 'FL': [], 'HR': [], 'HL': []},
            'hfren18': {'FR': [], 'FL': [], 'HR': [], 'HL': []}
        }}


    for stride in range(force_sync_file.shape[0]):
        current_row = force_sync_file.loc[stride, ]
        print("\n\n==============================================================\n\n")
        print("current row: \n", current_row)

        current_file = current_row['filename']

        print(f"\n\n<---------- current file: {current_file} ---------->\n")

        stride_start = current_row['footfall_begin']
        stride_end = current_row['footfall_end']
        force_stride_start = int(stride_start*Cfact)
        force_stride_end = int(stride_end*Cfact)

        # get the matching corrected force file for the current file
        matching_names_row_index = filematch_file.index[filematch_file['force_sync_output_entry'] == current_file].tolist()
        if len(matching_names_row_index) != 0:
            print("matching_names_row_index: ", matching_names_row_index[0])
            matching_names_row = filematch_file.loc[matching_names_row_index[0], ]
            print("matching_names_row: ", matching_names_row)

            matching_corrected_force_path = matching_names_row['corrected_force_file_filepath']
            matching_corrected_force_file = matching_names_row['corrected_force_file']
            print("matching_corrected_force_path: ", matching_corrected_force_path)
            print("matching_corrected_force_file: ", matching_corrected_force_file)
            matching_corrected_force = os.path.join(matching_corrected_force_path, matching_corrected_force_file)
            print("matching_corrected_force: ", matching_corrected_force)

            df_corrected_forces = pd.read_csv(matching_corrected_force, sep=" ", header=None)
            df_corrected_forces.columns = ["frame", "Fx", "Fy", "Fz"]               # name columns
            #print("corrected force txt file: ", df_corrected_forces.head)

            df_corrected_forces["frame"] = df_corrected_forces["frame"].astype(int)        # convert frame numbers to int

            Fx_stride = df_corrected_forces.loc[force_stride_start:force_stride_end, "Fx"]
            Fy_stride = df_corrected_forces.loc[force_stride_start:force_stride_end, "Fy"]
            Fz_stride = df_corrected_forces.loc[force_stride_start:force_stride_end, "Fz"]

            # see: https://stackoverflow.com/questions/38064697/interpolating-a-numpy-array-to-fit-another-array
            #arr_ref --> shape(average_force_stride)
            arr_ref_length = average_force_stride_length
            for array, array_name in zip([np.array(Fx_stride), np.array(Fy_stride), np.array(Fz_stride)], ["Fx", "Fy", "Fz"]):
                # compress array
                array_interp = interp.interp1d(np.arange(array.size), array)
                array_new = array_interp(np.linspace(0, array.size - 1, arr_ref_length))
                print("length of original array: ", array.size)
                print("length of array compressed: ", array_new.size)

                if interpolation_plots == True:
                    xmin, xmax = 0, 1
                    fig, ax1 = plt.subplots(ncols=1)
                    ax1.plot(np.linspace(xmin, xmax, array.size), array, 'bo-',
                             np.linspace(xmin, xmax, array_new.size), array_new, 'rs')
                    ax1.set_title("red-interpolated")
                    plt.show()

                #################################################
                # all force data strides now have the same length
                #################################################

                # save interpolated force array to dict of respective force axis:
                direction = current_row['direction']
                individual = matching_names_row['individual']
                foot = current_row['foot']

                if array_name == "Fx":
                    res_dict_Fx[direction][individual][foot].append(array_new)
                elif array_name == "Fy":
                    res_dict_Fy[direction][individual][foot].append(array_new)
                elif array_name == "Fz":
                    res_dict_Fz[direction][individual][foot].append(array_new)

    # plot all strides for exemplary combination of direction, individual and foot:
    direction = "down"
    foot = "HL"
    individual = "hfren11"
    xmin1, xmax1 = 0, average_force_stride_length
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)
    for arr in res_dict_Fx[direction][individual][foot]:
        ax1.plot(np.linspace(xmin1, xmax1, arr.size), arr)
    for arr2 in res_dict_Fy[direction][individual][foot]:
        ax2.plot(np.linspace(xmin1, xmax1, arr2.size), arr2)
    for arr3 in res_dict_Fz[direction][individual][foot]:
        ax3.plot(np.linspace(xmin1, xmax1, arr3.size), arr3)
    plt.show()

    return