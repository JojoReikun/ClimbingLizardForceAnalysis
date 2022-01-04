"""
!! FOLDER PATHS AND FILE NAMES ARE ALL HARDCODED ATM!!

This module will calculate the toppling moments over the time of a stride of lizards 
(currently made for hfren for Lizard Paper) up vs down. 

Because we only have one foot at a time for forces BUT for dynamic analysis we would need "live" data for fore and pair
hind foot at the same time, average force curve profiles for one individual for each foot were calculated.
(in hfren_strideDynamics.py)

For the calculations the following things are needed:
- Forces for the stride (average force profiles)
- Length between the fore and hind foot attached (add to DOKA)
- height of the BCOM compared to wall
- mass of lizards

Because the average force profile of a stride for a foot has a lot more frames than the kinematic stride data,
an interval selection of points of the force data is performed depending on stride length.

The moment for climbing head-up act around the hind feet, hence Fzn is from the fore feet, whereas for climbing head-down
this is the other way around: The moment acts around the fore feet, hence Fzn is from the hind feet.
"""

#### IMPORTS:
from glob import glob
import pandas as pd
import numpy as np
import scipy.interpolate as interp
import os
import matplotlib.pyplot as plt
import seaborn as sb

bodymasses_dict = {"hfren11": 2.75,
                   "hfren13": 3.25,
                   "hfren14": 3.87,
                   "hfren16": 3.47,
                   "hfren17": 2.30,
                   "hfren18": 3.53}     # grams

SVL_dict = {"hfren11": 426,
                   "hfren13": 419,
                   "hfren14": 463,
                   "hfren16": 463,
                   "hfren17": 364,
                   "hfren18": 424}     # mm

conv_factor_dict = {"hfren11": 0.6,
                   "hfren13": 0.67,
                   "hfren14": 0.67,
                   "hfren16": 0.6,
                   "hfren17": 0.6,
                   "hfren18": 0.58}     # px/mm

g = 9.81   # m/s^2
h = 0


# pd.set_option('display.max_columns', None)


moments_dict = {"up" : {"hfren11": [],
                        "hfren13": [],
                        "hfren14": [],
                        "hfren16": [],
                        "hfren17": [],
                        "hfren18": []},
                "down" : {"hfren11": [],
                        "hfren13": [],
                        "hfren14": [],
                        "hfren16": [],
                        "hfren17": [],
                        "hfren18": []}}

lengths_dict = {"up": [], "down": []}


def loop_encode(i):
    # get utf-8 encoded version of the string
    cell_value = 'stance000{}'.format(i).encode()
    # print("-----> stance phase cell value :", cell_value)
    return cell_value


def calc_toppling_moment(g, h, forceZ_FR_i, forceZ_FL_i, forceZ_HR_i, forceZ_HL_i, length_FL_i, length_FR_i, individual, foot, direction):
    # calculates the toppling moment around the hindfoot, assuming only a 2D view of the scene
    # and assuming the tail is not a contact point on the wall.
    if foot == "FL":
        if direction == "up":
            Fn_z_i = forceZ_FL_i
        elif direction == "down":
            Fn_z_i = forceZ_HR_i
        length = length_FL_i
    elif foot == "FR":
        if direction == "up":
            Fn_z_i = forceZ_FR_i
        elif direction == "down":
            Fn_z_i = forceZ_HL_i
        length = length_FR_i

    # convert length from px to mm:
    length = length/conv_factor_dict[individual]
    # convert mm to m:
    length = length/1000

    m = bodymasses_dict[individual]/1000    # to get mass in kg

    # # use SVL divided by 100 for each Gecko [mm]:
    # h = SVL_dict[individual]/100
    # # convert mm to m:
    # h = h/1000

    # use value from Autumn et al. (2006) paper --> 2cm off the ground
    h = 0.02    # in m

    # # estimate h assuming a static equilibrium
    # h = estimate_static_equ_h(Fn_z_i, length, m, g)

    moment = h * m * g + Fn_z_i * length

    print("____")
    print(f"individual: {individual}")
    print("h * m * g + Fn_z_i * length: ", f"{h} * {m} * {g} + {Fn_z_i} * {length}")
    print("\n >>>>>>>> in function moment: ", moment, "\n")
    print("____")

    return moment


def estimate_static_equ_h(Fn_z_i, length, m, g):
    """
    for static equilibrium of the toppling moment, we can assume it to be zero. Therefore, for a case with two contact points beeing the feet,
    h can be calculated as: h = -(Fnf * L1)/m*g (for up) or using Fnh for down.
    :return:
    """
    h = -1.0 * (Fn_z_i * length) / (m * g)
    return h



def hfren_climbing_moments():
    #### DEFINE FILE LOCATIONS AND NAMES:
    # file naming: e.g. hfren11_down_03_hflipDLC_resnet50_lizardpaper21GJun15shuffle1_500000.csv
    doka_hfren_folder = r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardDLCAnalysis\lizardanalysis\lizardpaper21-js-hfren-2021-06-28\analysis-results'
    doka_files_list = glob(os.path.join(doka_hfren_folder, "*.csv"))

    force_file_folder = r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardForceAnalysis_2020\forceData_hfren\correctedForces\average_force_profiles'
    # filenaming = e.g. avg_force_down_hfren11_FR.csv

    # go through DLC result files of lizards to iterate through all strides
    for doka_file in doka_files_list:
        # make two empty lists for storing all step_moments for this individual
        stance_moments_FR = []
        stance_moments_FL = []

        # read in the DOKA data
        kin_data = pd.read_csv(doka_file)
        kin_data.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
        data_rows_count = kin_data.shape[0]  # number of rows

        filename = doka_file.rsplit(os.sep, 1)[1]
        print("\n------> current file: ", filename)
        individual = filename.split("_", 1)[0]
        direction = filename.split("_", 2)[1]
        print("individual: ", individual, "direction: ", direction)

        active_columns = {"stepphase_FL": "FL",
                          "stepphase_FR": "FR"}
        max_step_count = 1000

        # find matching averaged foot force profiles for individual:
        force_profile_FR = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_FR_smoothed.csv"))
        force_profile_FL = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_FL_smoothed.csv"))
        force_profile_HR = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_HR_smoothed.csv"))
        force_profile_HL = pd.read_csv(os.path.join(force_file_folder, f"avg_force_{direction}_{individual}_HL_smoothed.csv"))

        # only z axis forces (normal forces) are needed for topplling moments:
        force_profile_FR = force_profile_FR["avg_Fz"]
        force_profile_FL = force_profile_FL["avg_Fz"]
        force_profile_HR = force_profile_HR["avg_Fz"]
        force_profile_HL = force_profile_HL["avg_Fz"]

        force_array_length = len(force_profile_FR)

        for col, foot in active_columns.items():
            col = col.strip('')
            for i in range(1, max_step_count):
                stance_moments = []
                stance_counter = loop_encode(i)
                kin_data_stance_section_indices = kin_data.index[kin_data[col] == str(stance_counter)].tolist()
                print("\n kin_data_stance_section_indices: ", kin_data_stance_section_indices, "\n")
                kin_data_stance_section = pd.DataFrame(kin_data[kin_data[col] == str(stance_counter)])

                #print("kin_data_stance_section: ", kin_data_stance_section, type(kin_data_stance_section))
                # print the indices of the kin_data section which are later called by i loop
                #kin_data_stance_section_top = kin_data_stance_section.head()
                stance_indices = list(kin_data_stance_section.index.values)

                print(f"col: {col}, foot: {foot}, stance counter: {stance_counter}, stance length: {len(kin_data_stance_section_indices)}")

                if len(kin_data_stance_section) == 0:   # could change this to a filter for stance sections > 5 too
                    print("stance section is length 0... break")
                    break

                else:
                    df_stance_section_indices = list(kin_data_stance_section.index.values)  # list of stance indices
                    stance_length = len(df_stance_section_indices)
                    #print("stance_length: ", stance_length)

                    ####### CALCULATE THE TOPPLING MOMENTS:
                    # depending on the stancelength, that many equally spread data points of the force data will be used
                    force_array_interval = round(force_array_length / stance_length) - 1
                    print("force array interval: ", force_array_interval)
                    #print("force_profile_FR: ", force_profile_FR)
                    force_profile_FR_points = [force_profile_FR[n*force_array_interval] for n in range(stance_length)]
                    force_profile_FL_points = [force_profile_FL[n*force_array_interval] for n in range(stance_length)]
                    force_profile_HR_points = [force_profile_HR[n*force_array_interval] for n in range(stance_length)]
                    force_profile_HL_points = [force_profile_HL[n*force_array_interval] for n in range(stance_length)]

                    print("force_profile_FR_points: ", force_profile_FR_points)

                    for j, k in enumerate(stance_indices): # k = from 1 ; j = actual indices
                        #print(f"length of frame i ({i}): ", kin_data_stance_section.loc[i, "dyn_footpair_height_FL"])

                        toppling_moment = calc_toppling_moment(g, h, force_profile_FR_points[j],
                                                               force_profile_FL_points[j],
                                                               force_profile_HR_points[j], force_profile_HL_points[j],
                                                               kin_data_stance_section.loc[k, "dyn_footpair_height_FL"],
                                                               kin_data_stance_section.loc[k, "dyn_footpair_height_FR"],
                                                               individual, foot, direction)
                        stance_moments.append(toppling_moment)

                        moments_dict[direction][individual].append(toppling_moment)

                        # add length for current frame to length_dict to plot difference up vs down:
                        if foot =="FR":
                            lengths_dict[direction].append(kin_data_stance_section.loc[k, "dyn_footpair_height_FR"],)
                            if direction == "up":
                                lengths_dict["down"].append(np.nan)
                            else:
                                lengths_dict["up"].append(np.nan)
                        else:
                            lengths_dict[direction].append(kin_data_stance_section.loc[k, "dyn_footpair_height_FL"],)
                            if direction == "up":
                                lengths_dict["down"].append(np.nan)
                            else:
                                lengths_dict["up"].append(np.nan)

                    print(f">>>>> moments: {stance_moments}\n")

                    if foot == "FR":
                        stance_moments_FR.append(stance_moments)
                    elif foot == "FL":
                        stance_moments_FL.append(stance_moments)

        ### plot moments in current stance
        # compress array
        print("length of moments: ", len(stance_moments_FR), "stance moments FR: ", stance_moments_FR)
        stance_moments_FR = [stance for stance in stance_moments_FR if not np.isnan(stance[0])]
        stance_moments_FR = [stance for stance in stance_moments_FR if len(stance)>3]
        print("length: ", len(stance_moments_FR), "stance moments FR after length filter: ", stance_moments_FR)
        stance_lengths_FR = [len(stance) for stance in stance_moments_FR]
        stance_moments_FR_new = []
        for stance in stance_moments_FR:
            stance = np.array(stance)
            stance_moments_FR_interp = interp.interp1d(np.arange(np.array(stance).size), stance)
            stance_moments_FR_new.append(stance_moments_FR_interp(np.linspace(0, stance.size - 1, int(np.nanmean(stance_lengths_FR)))))

        print("stance_moments_FR: ", stance_moments_FR_new)

        if len(stance_moments_FR) > 0:
            x = np.linspace(1, int(np.nanmean(stance_lengths_FR)) + 1, num=int(np.nanmean(stance_lengths_FR)))
            plot_filename = f"FR-{filename}"
            for stance in stance_moments_FR_new:
                plt.plot(x, stance)
                plt.scatter(x, y=stance)
            plt.hlines(y=0, xmin=1, xmax=int(np.nanmean(stance_lengths_FR)) + 1)
            plt.title(plot_filename)
            plt.ylabel("frame wise toppling moment")
            plt.xlabel("frame of stance phase")
            plt.savefig(r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardForceAnalysis_2020\forceData_hfren\correctedForces\dynamic_toppling_moments\{}.png'.format(plot_filename), dpi=100)
            plt.close()
            #plt.show()


    print("\n DONE! \n >>>>>>>>>>>>>> moments_dict: \n", moments_dict)

    ### PLOTTING:
    print("lengths lengths: ", len(lengths_dict["up"]), len(lengths_dict["down"]))
    pd.DataFrame(lengths_dict).plot(kind='density')
    plt.xlabel('length (in px) betw. fore and hind foot')

    for direction in moments_dict.keys():
        for individual in moments_dict[direction].keys():
            moments_dict[direction][individual] = np.nanmean(moments_dict[direction][individual])
            #moments_dict[direction][individual]["sd"] = np.nanstd(moments_dict[direction][individual])

    pd.DataFrame(moments_dict).plot(kind='bar', figsize=(12, 7))
    plt.ylabel("stance means toppling moment")
    plt.xlabel("individual")
    #plt.savefig(r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardForceAnalysis_2020\forceData_hfren\correctedForces\toppling_moments.pdf', dpi=300)
    #plt.close()
    plt.show()

    return