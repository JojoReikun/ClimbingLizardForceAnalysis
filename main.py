import step2_lizard_force_data_analysis
import step1_get_video_infos
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
    # open choose step prompt:
    gui = gui_choose_step_dialog_prompt.choose_step_prompt()
    operation = gui.show()
    if operation == True:
        # Button1 = Step1 = will be set operation to True when clicked
        step_1 = True
        step_2 = False
    else:
        # Button2 = Step2 = will be set operation to False when clicked
        step_1 = False
        step_2 = True

    # only get video infos:
    if step_1 == True and step_2 == False:
        print("STEP 1\n")
        filelist, video_dir, filenames, foldername = step1_get_video_infos.get_list_of_videos(current_path)
        codenames = step1_get_video_infos.get_name_code(filenames, foldername, filelist, video_dir)
        if convert_videos_to_nv12:
            step1_get_video_infos.convert_videos_to_ImageJ_format(video_dir)

    # only get nano17 calibration:
    elif step_2 == True and step_1 == False:
        print("\n\nSTEP 2\n")
        step2_lizard_force_data_analysis.nano17_openCV_as_ImageJ()

    # for testing:
    elif step_1 and step_2:
        print("TESTING")
        filelist, video_dir, filenames, foldername = step1_get_video_infos.get_list_of_videos(current_path)
        codenames = step1_get_video_infos.get_name_code(filenames, foldername, filelist, video_dir)
        if convert_videos_to_nv12:
            step1_get_video_infos.convert_videos_to_ImageJ_format(video_dir)
        step2_lizard_force_data_analysis.nano17_openCV_as_ImageJ()

    else:
        exit()

