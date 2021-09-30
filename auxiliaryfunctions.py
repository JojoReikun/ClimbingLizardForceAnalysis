def write_df_to_csv(dst_folder, output_filename, df):
    import os
    import overwrite_dialog_prompt

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
            return print("file {} saved successfully here: {}".format(output_filename, dst_folder))

        elif operation == False:
            print("file {} already exists and was not overwritten!".format(output_filename))


def open_gui_to_select_folder():
    from tkinter import filedialog, Tk
    import os
    root = Tk()
    root.withdraw()  # use to hide tkinter window

    destfolder = current_path = os.getcwd()

    tempdir = filedialog.askdirectory(parent=root, initialdir=current_path,
                                       title='Please select a directory containing lizard videos (e.g.: "ClimbingLizardVideos_2020/Gecko02/video_analysis")')
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