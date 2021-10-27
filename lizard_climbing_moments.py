import os
import auxiliaryfunctions

"""
This will currently only work for all gecko species EXCEPT the hfren. 

Hfren raw force data would need to be reanalysed
  --> make sure folder structure and file namings work for this script
  --> run step1 
  --> footfalls have to be extracted manually
  --> run step2
  --> forces need to be recalibrated using CoP of the force plate, not necessary for the other lizards
"""

# TODO: add body masses of lizards somewhere
# TODO: ISSUE!! we only have one foot at a time for forces --> for dynamic analysis we would need "live" data for fore and paired hind foot at the same time, figure out a way:
# e.g. get average force curve profiles for one species for fore and hind feet?
# or get mean lengths and use mean force values... but that wouldn't be continuous over a stride


def lizard_climbing_moments():
    #### DEFINE FILE LOCATIONS AND NAMES:
    destfolder = current_path = os.getcwd()

    tempdir = auxiliaryfunctions.open_gui_to_select_folder(
        'STEP3: Please select a directory containing lizard videos (e.g.: "ClimbingLizardVideos_2020/Gecko02/video_analysis")')
    # e.g. tempdir = "C:/Users/JojoS/Documents/phd/ClimbingRobot_XGen4/ClimbingLizardsVideos_2020/Gecko01/videos_analysis"

    # assumes that videos are in video_analysis inside the folder for the Group [-2]:
    foldername = auxiliaryfunctions.splitall(tempdir)[-2]
    # print("foldername: ", foldername)   # e.g. Dragon03

    # get the folder path which contains the raw force data .txt files for the lizards:
    # file naming gdub: e.g. gdub2_down_02.txt
    force_analysis_file = "{}_forceAnalysis_calib.csv".format(foldername)

    force_file_folder = auxiliaryfunctions.open_gui_to_select_folder(
        'Please select the folder containing all the .txt force data files')

    # get the folder path which contains the DLC tracked label data for the lizards:
    # file naming: e.g. gdub2_up_20_enhDLC_resnet50_lizardpaper21GJun15shuffle1_500000.csv
    DLC_file_folder = auxiliaryfunctions.open_gui_to_select_folder(
        'Please selsct the folder which contains the deeplabcut files which contains the label coordinates (post DLC, pre DOKA)')

    # go through DLC result files of lizards

    # find matching force file

    # find the stride (stance) in DLC data which matches the force stride

    # frame-wise:
        # calculate L1, L2 using the label locations from the DLC file for the stride (stance) in focus