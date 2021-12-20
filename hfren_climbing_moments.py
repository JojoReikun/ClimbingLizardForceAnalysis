import os
import auxiliaryfunctions

"""
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

bodymasses_dict = {"hfren11": 2.75,
                   "hfren13": 3.25,
                   "hfren14": 3.87,
                   "hfren16": 3.47,
                   "hfren17": 2.30,
                   "hfren18": 3.53}


def hfren_climbing_moments():
    #### DEFINE FILE LOCATIONS AND NAMES:
    destfolder = current_path = os.getcwd()
    doka_hfren_folder = r'C:\Users\JojoS\Documents\phd\ClimbingRobot_XGen4\ClimbingLizardDLCAnalysis\lizardanalysis\lizardpaper21-js-hfren-2021-06-28\analysis-results'

    # TODO: assign working folder (some hfren folder)

    # TODO: get the average force profile data (export from other module as csv or txt!)
    force_file_folder = auxiliaryfunctions.open_gui_to_select_folder(
        'Please select the folder containing all the .txt force data files')

    # get the folder path which contains the DLC tracked label data for the lizards, containing the length between attached feet:
    # TODO: do this for hfren
    # file naming: e.g. gdub2_up_20_enhDLC_resnet50_lizardpaper21GJun15shuffle1_500000.csv
    DLC_file_folder = auxiliaryfunctions.open_gui_to_select_folder(
        'Please selsct the folder which contains the deeplabcut files which contains the label coordinates (post DLC, pre DOKA)')

    # go through DLC result files of lizards to iterate through all strides

    # find matching force profiles for the current foot pair

    # frame-wise:
        # calculate the toppling moment