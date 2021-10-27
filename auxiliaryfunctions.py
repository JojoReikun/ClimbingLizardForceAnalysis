def write_df_to_csv(dst_folder, output_filename, df):
    import os
    import overwrite_dialog_prompt
    import math

    dest_path = os.path.join(dst_folder, output_filename)
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    if not os.path.isfile(dest_path):
        df.to_csv(dest_path)
    else:
        prompt = overwrite_dialog_prompt.open_prompt()
        operation = prompt.show(output_filename)
        print("overwrite = ", operation)
        if operation == True:
            df.to_csv(dest_path)
            print("\n\nfile {} saved successfully here: {}".format(output_filename, dst_folder))

        elif operation == False:
            print("\n\nfile {} already exists and was not overwritten!".format(output_filename))


def open_gui_to_select_folder(prompt_title):
    from tkinter import filedialog, Tk
    import os
    root = Tk()
    root.withdraw()  # use to hide tkinter window

    destfolder = current_path = os.getcwd()

    tempdir = filedialog.askdirectory(parent=root, initialdir=current_path,
                                       title=prompt_title)
    if len(tempdir) > 0:
        print("You chose %s" % tempdir)
    return tempdir


def splitall(path):
    """
    splits the passed path in all it's components. All components will be returned in list.
    :param path:
    :return: list of all components
    """
    import os
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def define_lizard_habitats():
    lizard_habitats = {
        "arboreal": ["gdub", "gvari", "ocas", "ocog", "ofil", "omon", "seld"],
        "semi-arboreal": ["skrys"],
        "terrestrial": ["limac", "lstein", "nam", "umill"]
    }


def convert_videoframe_to_forcerow(video_frame_count, video_frame_rate, force_sampling_rate, trigger, force_sampling_time_s, video_frame):
    """
    !!! If this function only returns nan values, this is likely due to missing frame rates in the data !!!
    Add these and try again.
    :param video_frame_count:
    :param video_frame_rate:
    :param force_sampling_rate:
    :param trigger:
    :param force_sampling_time_s:
    :param video_frame:
    :return:
    """
    forceRow = (trigger*force_sampling_time_s) - ( (video_frame_count-video_frame) * (force_sampling_rate/video_frame_rate) )

    if math.isnan(forceRow):
        print("This function returning nan values is likely due to missing frame rates in *_forceAnalysis_calib.csv!!!\n"
              "Exit")
        exit()

    return int(forceRow)