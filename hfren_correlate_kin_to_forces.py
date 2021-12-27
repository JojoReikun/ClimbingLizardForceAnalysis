"""
This script uses the output files which contain the stride wise summarised kinematic data:
- geckos_hfren_DOKA_with_metadata.csv
TODO: add start and end frames for each step as new columns (then force step can be matched to the exact step)
 --> DONE 27/12/2021 in step1_DOKAs_to_CSVs_v2.R
and the file which contains the step wise summarised force data, after running the plot_hfren_forces.R script, which adds
the columns Fxy and dir_Fxy to the data:
- Geckos_forces_sync_output.csv

The force data will be used to iterate through the available steps, as there are less than kinematic data.
Then the correct kinematic step will be matched in the kinematic file and mean values can then be used as a pair.
TODO: don't use mean values but exact step using the timestamp (frames)
"""

### IMPORTS:
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


path = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis'
hfren_kin = pd.read_csv(os.path.join(path, "geckos_hfren_DOKA_with_metadata.csv"), skipinitialspace=True)
hfren_kin.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
print(hfren_kin.head())

hfren_forces = pd.read_csv(os.path.join(path, "Geckos_forces_sync_output_xy.csv"), skipinitialspace=True)
hfren_forces.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
print(hfren_forces.head())


#inititate the dictionaries to save forces_kinematics:
force_kin_dict_up = {"FR": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         },
                    "FL": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         },
                    "HR": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         },
                    "HL": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         }}

force_kin_dict_down = {"FR": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         },
                    "FL": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         },
                    "HR": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         },
                    "HL": {"forces": {"Fx": [],
                                "Fy": [],
                                "Fz": [],
                                "Fxy": [],
                                "dir_Fxy": []},
                         "kinematics": {"wrist_F": [],
                                         "wrist_H": [],
                                         "CROM_F": [],
                                         "CROM_H": [],
                                         "toe_spreading_F": [],
                                         "toe_spreading_H": []}
                         }}


# iterate through force steps:
print(f">>>>>>>>>>>>>>>>>>>>>> TOTAL NUMBER OF FORCE STEPS: {hfren_forces.shape[0]}")
for i in range(hfren_forces.shape[0]):
    filename_force = hfren_forces.loc[i, "filename"]
    direction_force = hfren_forces.loc[i, "direction"]
    foot_force = hfren_forces.loc[i, "foot"]
    print(f"\n\n ---------- filename ({i}/{hfren_forces.shape[0]}): ", filename_force)
    print("direction of climbing of force trial: ", direction_force)
    filename_force = filename_force.split(".")[0]
    filename_comps = filename_force.split("_")

    # get start and end frame of force footfall:
    force_start = hfren_forces.loc[i, "footfall_begin"]
    force_end = hfren_forces.loc[i, "footfall_end"]
    force_indices = range(force_start, force_end)

    filename_force = filename_comps[0] + "_" + direction_force + "_" + filename_comps[2]

    print("filename new: ", filename_force, "current force stride indices: ", force_indices)

    #print(hfren_kin["ID"].tolist()[1] == filename_force)

    # find the matching rows for the current individual in hfren_kin data:
    #print(hfren_kin["ID"].tolist()[1])
    match_row_index = hfren_kin.index[hfren_kin["ID"] == filename_force].tolist()

    if len(match_row_index) != 0:
        print("matching_names_rows_indices: ", match_row_index)

        hfren_kin_match = hfren_kin.iloc[match_row_index[0]:match_row_index[-1], ]
        if foot_force == "HR":
            foot_kin_to_match = "FL"
        elif foot_force == "HL":
            foot_kin_to_match = "FR"
        else:
            foot_kin_to_match = foot_force

        # look for rows in hfren_kin_match which also match the foot_force:
        hfren_kin_match_foot = hfren_kin_match.index[hfren_kin_match["foot"] == foot_kin_to_match].tolist()
        print("indices of kin rows which match the force foot: ", hfren_kin_match_foot)

        # now we have to find which of the matching feet is the correct step for the force data, using frame_start and frame_end
        # create a list of lists: each sublist contains the indices for a kinematic step within hfren_kin_match_foot
        matching_kin_step_indices = []

        for m in hfren_kin_match_foot:
            matching_kin_step_indices.append([i for i in range(hfren_kin.loc[m, "frame_start"], hfren_kin.loc[m, "frame_end"])])
        print("list of indices with lists of step indices of matching kin steps: ", matching_kin_step_indices)

        # find the list with the maximum overlay with the force indices:
        overlaps = [len(list(set(force_indices) & set(l))) for l in matching_kin_step_indices]
        overlaps_max = overlaps.index(max(overlaps))
        print("overlaps: ", overlaps, "; ", overlaps_max)

        matching_step = hfren_kin_match_foot[overlaps_max]

##### UP
        if direction_force == "up":
            # now add in the force values and corresponding kinematic values to the dict to the correct foot:
            force_kin_dict_up[foot_force]["forces"]["Fx"].append(round(hfren_forces.loc[i, "MeanX_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["Fy"].append(round(hfren_forces.loc[i, "MeanY_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["Fz"].append(round(hfren_forces.loc[i, "MeanZ_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["Fxy"].append(round(hfren_forces.loc[i, "MeanXY_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["dir_Fxy"].append(round(hfren_forces.loc[i, "dirMeanXY_rel"], 8))

            force_kin_dict_up[foot_force]["kinematics"]["wrist_F"].append(round(hfren_kin.loc[matching_step, "midwrist_F"], 2))
            force_kin_dict_up[foot_force]["kinematics"]["wrist_H"].append(round(hfren_kin.loc[matching_step, "midwrist_H"], 2))
            force_kin_dict_up[foot_force]["kinematics"]["CROM_F"].append(round(hfren_kin.loc[matching_step, "CROM_F"], 2))
            force_kin_dict_up[foot_force]["kinematics"]["CROM_H"].append(round(hfren_kin.loc[matching_step, "CROM_H"],2))
            force_kin_dict_up[foot_force]["kinematics"]["toe_spreading_F"].append(round(hfren_kin.loc[matching_step, "Mean_toe_F"], 2))
            force_kin_dict_up[foot_force]["kinematics"]["toe_spreading_H"].append(round(hfren_kin.loc[matching_step, "Mean_toe_H"], 2))

##### DOWN
        elif direction_force == "down":
            # now add in the force values and corresponding kinematic values to the dict to the correct foot:
            force_kin_dict_down[foot_force]["forces"]["Fx"].append(round(hfren_forces.loc[i, "MeanX_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["Fy"].append(round(hfren_forces.loc[i, "MeanY_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["Fz"].append(round(hfren_forces.loc[i, "MeanZ_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["Fxy"].append(round(hfren_forces.loc[i, "MeanXY_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["dir_Fxy"].append(round(hfren_forces.loc[i, "dirMeanXY_rel"], 8))

            force_kin_dict_down[foot_force]["kinematics"]["wrist_F"].append(round(hfren_kin.loc[matching_step, "midwrist_F"], 2))
            force_kin_dict_down[foot_force]["kinematics"]["wrist_H"].append(round(hfren_kin.loc[matching_step, "midwrist_H"], 2))
            force_kin_dict_down[foot_force]["kinematics"]["CROM_F"].append(round(hfren_kin.loc[matching_step, "CROM_F"], 2))
            force_kin_dict_down[foot_force]["kinematics"]["CROM_H"].append(round(hfren_kin.loc[matching_step, "CROM_H"],2))
            force_kin_dict_down[foot_force]["kinematics"]["toe_spreading_F"].append(round(hfren_kin.loc[matching_step, "Mean_toe_F"], 2))
            force_kin_dict_down[foot_force]["kinematics"]["toe_spreading_H"].append(round(hfren_kin.loc[matching_step, "Mean_toe_H"], 2))

    else:
        print("\n >>>>> NEXT <<<<<< \n")

print("force_kin_dict_up: ", force_kin_dict_up)


#### PLOTTING:
# TODO: write plotting function to selsct certain combinations
plot_pairs= {"Fz":"wrist_F",
              "Fz":"CROM_F",
              "Fxy":"wrist_F"}
force = "Fz"
kin = "wrist_F"
kin2= "wrist_H"
plt.figure(figsize=(12,6))
plt.scatter(y=force_kin_dict_up["FL"]["forces"][force], x=force_kin_dict_up["FL"]["kinematics"][kin], color="b")
plt.scatter(y=force_kin_dict_up["FR"]["forces"][force], x=force_kin_dict_up["FR"]["kinematics"][kin], color="b")
plt.scatter(y=force_kin_dict_down["HR"]["forces"][force], x=force_kin_dict_down["HR"]["kinematics"][kin2], color="r")
plt.scatter(y=force_kin_dict_down["HL"]["forces"][force], x=force_kin_dict_down["HL"]["kinematics"][kin2], color="r")
plt.title(f"{force} - {kin}")
plt.xlabel(f"{kin}")
plt.ylabel(f"{force}")
plt.show()

# for foot in ["FR", "FL", "HR", "HL"]:
#     for force in force_kin_dict_up[foot]["forces"].keys():
#         y = force_kin_dict_up[foot]["forces"][force]
#
#         fig, axs = plt.subplots(3,2)
#         #fig = plt.figure(constrained_layout=True)
#         #spec = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)
#         axs[0,0].scatter(force_kin_dict_up[foot]["kinematics"]["wrist_F"], y)
#         axs[0,0].title.set_text(f'{force} - wrist_F')
#         axs[0,1].scatter(force_kin_dict_up[foot]["kinematics"]["wrist_H"], y)
#         axs[0,1].title.set_text(f'{force} - wrist_H')
#         axs[1,0].scatter(force_kin_dict_up[foot]["kinematics"]["CROM_F"], y)
#         axs[1,0].title.set_text(f'{force} - CROM_F')
#         axs[1,1].scatter(force_kin_dict_up[foot]["kinematics"]["CROM_H"], y)
#         axs[1,1].title.set_text(f'{force} - CROM_H')
#         axs[2,0].scatter(force_kin_dict_up[foot]["kinematics"]["toe_spreading_F"], y)
#         axs[2,0].title.set_text(f'{force} - toe_spreading_F')
#         axs[2,1].scatter(force_kin_dict_up[foot]["kinematics"]["toe_spreading_H"], y)
#         axs[2,1].title.set_text(f'{force} - toe_spreading_H')
#         fig.tight_layout(pad=1)
#         fig.suptitle(f"{foot}")
#
#         # save plots:
#         save_dir = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\kin_force_corr'
#         #plt.savefig(os.path.join(save_dir, f"CorrKinForce_up_{foot}_{force}.jpg"))
#         #plt.close()
#
#         plt.show()
#
#     for force in force_kin_dict_down[foot]["forces"].keys():
#         y = force_kin_dict_down[foot]["forces"][force]
#
#         fig, axs = plt.subplots(3, 2)
#         # fig = plt.figure(constrained_layout=True)
#         # spec = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)
#         axs[0, 0].scatter(force_kin_dict_down[foot]["kinematics"]["wrist_F"], y, c="red")
#         axs[0, 0].title.set_text(f'{force} - wrist_F')
#         axs[0, 1].scatter(force_kin_dict_down[foot]["kinematics"]["wrist_H"], y, c="red")
#         axs[0, 1].title.set_text(f'{force} - wrist_H')
#         axs[1, 0].scatter(force_kin_dict_down[foot]["kinematics"]["CROM_F"], y, c="red")
#         axs[1, 0].title.set_text(f'{force} - CROM_F')
#         axs[1, 1].scatter(force_kin_dict_down[foot]["kinematics"]["CROM_H"], y, c="red")
#         axs[1, 1].title.set_text(f'{force} - CROM_H')
#         axs[2, 0].scatter(force_kin_dict_down[foot]["kinematics"]["toe_spreading_F"], y, c="red")
#         axs[2, 0].title.set_text(f'{force} - toe_spreading_F')
#         axs[2, 1].scatter( force_kin_dict_down[foot]["kinematics"]["toe_spreading_H"], y, c="red")
#         axs[2, 1].title.set_text(f'{force} - toe_spreading_H')
#         fig.tight_layout(pad=1)
#         fig.suptitle(f"{foot}")
#
#         # save plots:
#         save_dir = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\kin_force_corr'
#         #plt.savefig(os.path.join(save_dir, f"CorrKinForce_down_{foot}_{force}.jpg"))
#         #plt.close()
#
#         plt.show()
