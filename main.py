from step3_alignVideo_with_forceData import extract_force_data_for_steps
from step2_lizard_force_data_analysis import nano17_openCV_as_ImageJ
from step1_get_video_infos import get_list_of_videos, get_name_code, convert_videos_to_ImageJ_format
from hfren_strideDynamics import hfren_strideDynamics
from hfren_climbing_moments import hfren_climbing_moments
import os
import gui_choose_step_dialog_prompt

convert_videos_to_nv12 = False

# --------------------------------
destfolder = current_path = os.getcwd()

"""
This python script is meant to work with the climbing lizard data split by family and group.
It needs the following folders & files: 
-- ClimbingLizardVideos_2020 (currently in PhD/ClimbingRobot)
     --> within this there are subfolders e.g.: Gecko01, Gecko02, ..., Dragon01 etc.
      which contain subfolders e.g.: video_analysis (contain all videos in .avi format), video_train
-- all force files in.txt format are needed

Run Step1 first, then manual input into the exported dataframes is needed!
Then run Step2! 
If any of the result files of these already exists, the user will be asked if they want to overwrite this.
"""

if __name__ == "__main__":
    operation = None
    # open choose step prompt:
    gui = gui_choose_step_dialog_prompt.choose_step_prompt()
    operation = gui.show()

    print("\noperation selected: ", operation, "\n")

    if operation == "step1":
        """
        get the information from the videos and prepare the dataframe for the manual entering of foot falls
        """
        print("\n\nSTEP 1\n")
        filelist, video_dir, filenames, foldername = get_list_of_videos(current_path)
        codenames = get_name_code(filenames, foldername, filelist, video_dir)
        if convert_videos_to_nv12:
            convert_videos_to_ImageJ_format(video_dir)

    elif operation == "step2":
        """
        requires the output from step 1. This allows to extract CoP and foot fall locations and calibrates the distances
        px to mm. 
        """
        print("\n\nSTEP 2\n")
        nano17_openCV_as_ImageJ()

    elif operation == "step3":
        """
        requires the output from step 2 and all the force files with the names as in the output in one folder.
        This step aligns the force data with the video and extracts Min, Max and Mean values for the respective footfalls.
        """
        print("\n\nSTEP 3\n")
        extract_force_data_for_steps()

    elif operation == "step4":
        """
        This goes into hfren_strideDynamics, where average force profiles are generated, which are then used to calculate in-stride dynamics and momentum
        """
        print("\n\nSTEP 4\n")
        hfren_strideDynamics()

    elif operation == "step5":
        """ 
        This goes into hfren_climbing_moments.py and calculates the toppling moments of the hfren lizards
        """
        print("\n\nSTEP 5\n")
        hfren_climbing_moments()



