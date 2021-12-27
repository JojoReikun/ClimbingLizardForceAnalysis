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
    --> optional: smooth average force curves

"""

### Imports:
import pandas as pd
import numpy as np
import os
import scipy.interpolate as interp
import matplotlib.pyplot as plt
from scipy import signal


### Set up:
# lab workstation:
force_sync_file_path = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\forceData_hfren\correctedForces\Gecko_forces_sync_output.csv'
filename_match_path = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\hfren_filename_matching_chart.csv'

# force collection parameters:
sample_rate = 10000
trigger = 9000
length = 10
framerate = 250
Cfact = sample_rate/framerate

interpolation_plots = False
smooth_forces = True


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
                print(f"\n ----- current force axis: {array_name} -----\n")

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

    # average all strides for each foot to get average force profile and standard deviation:
    avg_dict_Fx = {'up': {
        'hfren11': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren13': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren14': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren16': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren17': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren18': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}}
    },
        'down': {
        'hfren11': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren13': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren14': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren16': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren17': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
        'hfren18': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}}
        }}

    avg_dict_Fy = {'up': {
        'hfren11': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren13': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren14': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren16': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren17': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren18': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}}
    },
        'down': {
            'hfren11': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren13': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren14': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren16': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren17': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren18': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}}
        }}

    avg_dict_Fz = {'up': {
        'hfren11': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren13': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren14': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren16': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren17': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}},
        'hfren18': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []}, 'HR': {'average': [], 'sd': []},
                    'HL': {'average': [], 'sd': []}}
    },
        'down': {
            'hfren11': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren13': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren14': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren16': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren17': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}},
            'hfren18': {'FR': {'average': [], 'sd': []}, 'FL': {'average': [], 'sd': []},
                        'HR': {'average': [], 'sd': []}, 'HL': {'average': [], 'sd': []}}
        }}


    #print(res_dict_Fx[direction][individual][foot])

    for res_dict, avg_dict in zip([res_dict_Fx, res_dict_Fy, res_dict_Fz], [avg_dict_Fx, avg_dict_Fy, avg_dict_Fz]):
        for direction in res_dict.keys():
            for individual in res_dict[direction].keys():
                for foot in res_dict[direction][individual].keys():
                    for i in range(average_force_stride_length):
                        list_of_values_i = []
                        #print("length of res_dict_Fx[direction][individual][foot]: ", len(res_dict[direction][individual][foot]))
                        for n in range(len(res_dict[direction][individual][foot])):
                            # get the i-th value of each stride n and add it to the list
                            list_of_values_i.append(res_dict[direction][individual][foot][n][i])

                        #print("list of values i: ", list_of_values_i)
                        avg_dict[direction][individual][foot]["average"].append(np.nanmean(list_of_values_i))
                        avg_dict[direction][individual][foot]["sd"].append(np.std(list_of_values_i))

    # plot resultant average force profile:
    directions = ['up', 'down']
    individuals = ['hfren11', 'hfren13', 'hfren14', 'hfren16', 'hfren17', 'hfren18']
    feet = ['FR', 'FL', 'HR', 'HL']

    # smooth average force profiles
    if smooth_forces == True:
        print("smoothing... ")
        wl = 51
        for direction in directions:
            for individual in individuals:
                for foot in feet:
                    x = np.linspace(xmin1, xmax1, average_force_stride_length)
                    b, a = signal.butter(3, 0.03, btype='lowpass', analog=False)
                    # lowpass filter for foot motion
                    # avg_dict_Fx[direction][individual][foot]["average_smoothed"] = signal.filtfilt(b, a, avg_dict_Fx[direction][
                    #     individual][foot]["average"])
                    # avg_dict_Fy[direction][individual][foot]["average_smoothed"] = signal.filtfilt(b, a, avg_dict_Fx[direction][
                    #     individual][foot]["average"])
                    # avg_dict_Fz[direction][individual][foot]["average_smoothed"] = signal.filtfilt(b, a, avg_dict_Fx[direction][
                    #     individual][foot]["average"])

                    avg_dict_Fx[direction][individual][foot]["average_smoothed"] = signal.savgol_filter(avg_dict_Fx[
                        direction][individual][foot]["average"], wl, 3)
                    avg_dict_Fy[direction][individual][foot]["average_smoothed"] = signal.savgol_filter(avg_dict_Fx[
                        direction][individual][foot]["average"], wl, 3)
                    avg_dict_Fz[direction][individual][foot]["average_smoothed"] = signal.savgol_filter(avg_dict_Fx[
                        direction][individual][foot]["average"], wl, 3)

    print("plotting...")
    for direction in directions:
        for individual in individuals:
            for foot in feet:
                # TODO: If smooth true, add smoothed line to plot as well!
                fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)
                ax1.plot(np.linspace(xmin1, xmax1, average_force_stride_length),
                         avg_dict_Fx[direction][individual][foot]["average"], lw=2)
                ax1.fill_between(np.linspace(xmin1, xmax1, average_force_stride_length),
                                 np.subtract(avg_dict_Fx[direction][individual][foot]["average"],
                                             avg_dict_Fx[direction][individual][foot]["sd"]),
                                 np.add(avg_dict_Fx[direction][individual][foot]["average"],
                                        avg_dict_Fx[direction][individual][foot]["sd"]),
                                 facecolor='gray', alpha=0.5)
                if smooth_forces == True:
                     ax1.plot(np.linspace(xmin1, xmax1, average_force_stride_length),
                     avg_dict_Fx[direction][individual][foot]["average_smoothed"], lw=1, c="red")
                ax2.plot(np.linspace(xmin1, xmax1, average_force_stride_length),
                         avg_dict_Fy[direction][individual][foot]["average"], lw=2)
                ax2.fill_between(np.linspace(xmin1, xmax1, average_force_stride_length),
                                 np.subtract(avg_dict_Fy[direction][individual][foot]["average"],
                                             avg_dict_Fy[direction][individual][foot]["sd"]),
                                 np.add(avg_dict_Fy[direction][individual][foot]["average"],
                                        avg_dict_Fy[direction][individual][foot]["sd"]),
                                 facecolor='gray', alpha=0.5)
                if smooth_forces == True:
                     ax2.plot(np.linspace(xmin1, xmax1, average_force_stride_length),
                     avg_dict_Fy[direction][individual][foot]["average_smoothed"], lw=1, c="red")
                ax3.plot(np.linspace(xmin1, xmax1, average_force_stride_length),
                         avg_dict_Fz[direction][individual][foot]["average"], lw=2)
                ax3.fill_between(np.linspace(xmin1, xmax1, average_force_stride_length),
                                 np.subtract(avg_dict_Fz[direction][individual][foot]["average"],
                                             avg_dict_Fz[direction][individual][foot]["sd"]),
                                 np.add(avg_dict_Fz[direction][individual][foot]["average"],
                                        avg_dict_Fz[direction][individual][foot]["sd"]),
                                 facecolor='gray', alpha=0.5)
                if smooth_forces == True:
                     ax3.plot(np.linspace(xmin1, xmax1, average_force_stride_length),
                     avg_dict_Fz[direction][individual][foot]["average_smoothed"], lw=1, c="red")
                fig.suptitle(f"{direction} - {individual} - {foot}")

                # save plots:
                save_dir = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\forceData_hfren\correctedForces\average_force_profiles'
                #plt.savefig(os.path.join(save_dir, f"averageForces_{direction}_{individual}_{foot}.jpg"))
                #plt.close()
                plt.show()

                # save dictionaries of avg_Fx, avg_Fy, and avg_Fz as csv files
                # as avg_forces_{direction}_{individual}_{foot}.csv with frame, Fx, Fy, Fz
                if smooth_forces == True:
                    # TODO: export smooth forces
                    pass
                else:
                    frame = range(len(avg_dict_Fx[direction][individual][foot]["average"]))
                    Fx = avg_dict_Fx[direction][individual][foot]["average"]
                    Fy = avg_dict_Fy[direction][individual][foot]["average"]
                    Fz = avg_dict_Fz[direction][individual][foot]["average"]
                    save_dict = {"frame": frame,
                                 "avg_Fx": Fx,
                                 "avg_Fy": Fy,
                                 "avg_Fz": Fz}
                    df = pd.DataFrame.from_dict(save_dict)

                    print(f"save dict for {direction}_{individual}_{foot}: ", save_dict)
                    df.to_csv(os.path.join(save_dir, r'avg_force_{}_{}_{}.csv'.format(direction, individual, foot)), index=False, header=True)


    return