import lizard_force_data_analysis
import get_video_infos
import os

convert_videos_to_nv12 = False

# --------------------------------
step_1 = True
step_2 = False

destfolder = current_path = os.getcwd()


if __name__ == "__main__":
    # only get video infos:
    if step_1 == True and step_2 == False:
        print("STEP 1\n")
        filelist, video_dir, filenames, foldername = get_video_infos.get_list_of_videos(current_path)
        codenames = get_video_infos.get_name_code(filenames, foldername, filelist, video_dir)
        if convert_videos_to_nv12:
            get_video_infos.convert_videos_to_ImageJ_format(video_dir)

    # only get nano17 calibration:
    elif step_2 == True and step_1 == False:
        print("\n\nSTEP 2\n")
        lizard_force_data_analysis.nano17_openCV_as_ImageJ()

    # for testing:
    elif step_1 and step_2:
        print("TESTING")
        filelist, video_dir, filenames, foldername = get_video_infos.get_list_of_videos(current_path)
        codenames = get_video_infos.get_name_code(filenames, foldername, filelist, video_dir)
        if convert_videos_to_nv12:
            get_video_infos.convert_videos_to_ImageJ_format(video_dir)
        lizard_force_data_analysis.nano17_openCV_as_ImageJ()

