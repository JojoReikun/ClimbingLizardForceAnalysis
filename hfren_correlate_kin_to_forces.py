"""
This script uses the output files which contain the stride wise summarised kinematic data:
- geckos_hfren_DOKA_with_metadata.csv
and the file which contains the step wise summarised force data, after running the plot_hfren_forces.R script, which adds
the columns Fxy and dir_Fxy to the data:
- Geckos_forces_sync_output.csv

THe force data will be used to iterate through the available steps, as there are less than kinematic data.
Then the correct kinematic step will be matched in the kinematic file and mean values can then be used as a pair.
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


for i in range(hfren_forces.shape[0]):
    filename_force = hfren_forces.loc[i, "filename"]
    direction_force = hfren_forces.loc[i, "direction"]
    foot_force = hfren_forces.loc[i, "foot"]
    print("\n\n ---------- filename i: ", filename_force)
    print("direction of climbing of force trial: ", direction_force)
    filename_force = filename_force.split(".")[0]
    filename_comps = filename_force.split("_")

    filename_force = filename_comps[0] + "_" + direction_force + "_" + filename_comps[2]

    print("filename new: ", filename_force)

    print(hfren_kin["ID"].tolist()[1] == filename_force)

    # find the matching rows in hfren_kin data:
    print(hfren_kin["ID"].tolist()[1])
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

##### UP
        if direction_force == "up":

            # now average the kinematic data for these steps:
            wrist_F_list_up = []
            wrist_H_list_up = []
            CROM_F_list_up = []
            CROM_H_list_up = []
            toe_spreading_F_list_up = []
            toe_spreading_H_list_up = []

            wrist_F_average_up = []
            wrist_H_average_up = []
            CROM_F_average_up = []
            CROM_H_average_up = []
            toes_F_average_up = []
            toes_H_average_up = []


            list_of_lists = [wrist_F_list_up, wrist_H_list_up, CROM_F_list_up, CROM_H_list_up, toe_spreading_F_list_up, toe_spreading_H_list_up]
            list_of_averages = [wrist_F_average_up, wrist_H_average_up, CROM_F_average_up, CROM_H_average_up, toes_F_average_up, toes_H_average_up]

            for j in hfren_kin_match_foot:
                wrist_F_list_up.append(hfren_kin.loc[j, "midwrist_F"])
                wrist_H_list_up.append(hfren_kin.loc[j, "midwrist_H"])
                CROM_F_list_up.append(hfren_kin.loc[j, "CROM_F"])
                CROM_H_list_up.append(hfren_kin.loc[j, "CROM_H"])
                toe_spreading_F_list_up.append(hfren_kin.loc[j, "Mean_toe_F"])
                toe_spreading_H_list_up.append(hfren_kin.loc[j, "Mean_toe_H"])

            for l, a in zip(list_of_lists, list_of_averages):
                if np.isnan(l).all():
                    a.append(np.nan)
                else:
                    a.append(np.nanmean(l))

            # now add in the force values and corresponding kinematic values to the dict to the correct foot:
            force_kin_dict_up[foot_force]["forces"]["Fx"].append(round(hfren_forces.loc[i, "MeanX_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["Fy"].append(round(hfren_forces.loc[i, "MeanY_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["Fz"].append(round(hfren_forces.loc[i, "MeanZ_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["Fxy"].append(round(hfren_forces.loc[i, "MeanXY_rel"], 8))
            force_kin_dict_up[foot_force]["forces"]["dir_Fxy"].append(round(hfren_forces.loc[i, "dirMeanXY_rel"], 8))

            force_kin_dict_up[foot_force]["kinematics"]["wrist_F"].append(round(wrist_F_average_up[0], 2))
            force_kin_dict_up[foot_force]["kinematics"]["wrist_H"].append(round(wrist_H_average_up[0], 2))
            force_kin_dict_up[foot_force]["kinematics"]["CROM_F"].append(round(CROM_F_average_up[0], 2))
            force_kin_dict_up[foot_force]["kinematics"]["CROM_H"].append(round(CROM_H_average_up[0], 2))
            force_kin_dict_up[foot_force]["kinematics"]["toe_spreading_F"].append(round(toes_F_average_up[0], 2))
            force_kin_dict_up[foot_force]["kinematics"]["toe_spreading_H"].append(round(toes_H_average_up[0], 2))

##### DOWN
        elif direction_force == "down":
            # now average the kinematic data for these steps:
            wrist_F_list_down = []
            wrist_H_list_down = []
            CROM_F_list_down = []
            CROM_H_list_down = []
            toe_spreading_F_list_down = []
            toe_spreading_H_list_down = []

            wrist_F_average_down = []
            wrist_H_average_down = []
            CROM_F_average_down = []
            CROM_H_average_down = []
            toes_F_average_down = []
            toes_H_average_down = []

            list_of_lists = [wrist_F_list_down, wrist_H_list_down, CROM_F_list_down, CROM_H_list_down, toe_spreading_F_list_down,
                             toe_spreading_H_list_down]
            list_of_averages = [wrist_F_average_down, wrist_H_average_down, CROM_F_average_down, CROM_H_average_down, toes_F_average_down,
                                toes_H_average_down]

            for j in hfren_kin_match_foot:
                wrist_F_list_down.append(hfren_kin.loc[j, "midwrist_F"])
                wrist_H_list_down.append(hfren_kin.loc[j, "midwrist_H"])
                CROM_F_list_down.append(hfren_kin.loc[j, "CROM_F"])
                CROM_H_list_down.append(hfren_kin.loc[j, "CROM_H"])
                toe_spreading_F_list_down.append(hfren_kin.loc[j, "Mean_toe_F"])
                toe_spreading_H_list_down.append(hfren_kin.loc[j, "Mean_toe_H"])

            for l, a in zip(list_of_lists, list_of_averages):
                if np.isnan(l).all():
                    a.append(np.nan)
                else:
                    a.append(np.nanmean(l))

            # now add in the force values and corresponding kinematic values to the dict to the correct foot:
            force_kin_dict_down[foot_force]["forces"]["Fx"].append(round(hfren_forces.loc[i, "MeanX_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["Fy"].append(round(hfren_forces.loc[i, "MeanY_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["Fz"].append(round(hfren_forces.loc[i, "MeanZ_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["Fxy"].append(round(hfren_forces.loc[i, "MeanXY_rel"], 8))
            force_kin_dict_down[foot_force]["forces"]["dir_Fxy"].append(round(hfren_forces.loc[i, "dirMeanXY_rel"], 8))

            force_kin_dict_down[foot_force]["kinematics"]["wrist_F"].append(round(wrist_F_average_down[0], 2))
            force_kin_dict_down[foot_force]["kinematics"]["wrist_H"].append(round(wrist_H_average_down[0], 2))
            force_kin_dict_down[foot_force]["kinematics"]["CROM_F"].append(round(CROM_F_average_down[0], 2))
            force_kin_dict_down[foot_force]["kinematics"]["CROM_H"].append(round(CROM_H_average_down[0], 2))
            force_kin_dict_down[foot_force]["kinematics"]["toe_spreading_F"].append(round(toes_F_average_down[0], 2))
            force_kin_dict_down[foot_force]["kinematics"]["toe_spreading_H"].append(round(toes_H_average_down[0], 2))


print("force_kin_dict_up: ", force_kin_dict_up)


#### PLOTTING:
for foot in ["FR", "FL", "HR", "HL"]:
    for force in force_kin_dict_up[foot]["forces"].keys():
        x = force_kin_dict_up[foot]["forces"][force]

        fig, axs = plt.subplots(3,2)
        #fig = plt.figure(constrained_layout=True)
        #spec = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)
        axs[0,0].scatter(x, force_kin_dict_up[foot]["kinematics"]["wrist_F"])
        axs[0,0].title.set_text(f'{force} - wrist_F')
        axs[0,1].scatter(x, force_kin_dict_up[foot]["kinematics"]["wrist_H"])
        axs[0,1].title.set_text(f'{force} - wrist_H')
        axs[1,0].scatter(x, force_kin_dict_up[foot]["kinematics"]["CROM_F"])
        axs[1,0].title.set_text(f'{force} - CROM_F')
        axs[1,1].scatter(x, force_kin_dict_up[foot]["kinematics"]["CROM_H"])
        axs[1,1].title.set_text(f'{force} - CROM_H')
        axs[2,0].scatter(x, force_kin_dict_up[foot]["kinematics"]["toe_spreading_F"])
        axs[2,0].title.set_text(f'{force} - toe_spreading_F')
        axs[2,1].scatter(x, force_kin_dict_up[foot]["kinematics"]["toe_spreading_H"])
        axs[2,1].title.set_text(f'{force} - toe_spreading_H')
        fig.tight_layout(pad=1)
        fig.suptitle(f"{foot}")

        # save plots:
        save_dir = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\kin_force_corr'
        plt.savefig(os.path.join(save_dir, f"CorrKinForce_up_{foot}_{force}.jpg"))
        plt.close()

        #plt.show()

    for force in force_kin_dict_down[foot]["forces"].keys():
        x = force_kin_dict_down[foot]["forces"][force]

        fig, axs = plt.subplots(3, 2)
        # fig = plt.figure(constrained_layout=True)
        # spec = gridspec.GridSpec(nrows=3, ncols=2, figure=fig)
        axs[0, 0].scatter(x, force_kin_dict_down[foot]["kinematics"]["wrist_F"], c="red")
        axs[0, 0].title.set_text(f'{force} - wrist_F')
        axs[0, 1].scatter(x, force_kin_dict_down[foot]["kinematics"]["wrist_H"], c="red")
        axs[0, 1].title.set_text(f'{force} - wrist_H')
        axs[1, 0].scatter(x, force_kin_dict_down[foot]["kinematics"]["CROM_F"], c="red")
        axs[1, 0].title.set_text(f'{force} - CROM_F')
        axs[1, 1].scatter(x, force_kin_dict_down[foot]["kinematics"]["CROM_H"], c="red")
        axs[1, 1].title.set_text(f'{force} - CROM_H')
        axs[2, 0].scatter(x, force_kin_dict_down[foot]["kinematics"]["toe_spreading_F"], c="red")
        axs[2, 0].title.set_text(f'{force} - toe_spreading_F')
        axs[2, 1].scatter(x, force_kin_dict_down[foot]["kinematics"]["toe_spreading_H"], c="red")
        axs[2, 1].title.set_text(f'{force} - toe_spreading_H')
        fig.tight_layout(pad=1)
        fig.suptitle(f"{foot}")

        # save plots:
        save_dir = r'D:\Jojo\PhD\ClimbingRobot\ClimbingLizardForceAnalysis\kin_force_corr'
        plt.savefig(os.path.join(save_dir, f"CorrKinForce_down_{foot}_{force}.jpg"))
        plt.close()

        # plt.show()
