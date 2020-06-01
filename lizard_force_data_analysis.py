import pandas as pd
import numpy as np
import os
from pathlib import Path
import re

convert_videos_to_nv12 = False

destfolder = current_path = os.getcwd()

lizardgroups_DLC = {"Gecko01": ["gdub", "skrys", "swil"],
                    "Gecko02": ["gvari", "limac", "lstein", "scil", "seld", "umill"],
                    "Gecko03": ["nshae", "nam"],
                    "Gecko04": ["ocas", "ocog", "ofil", "omon"],
                    "Dragon01": ["aburn", "amur", "dnobbi", "lspin", "ttemp"],
                    "Dragon02": ["cinf", "cnuch", "pvit", "rdiem", "ttet"],
                    "Dragon03": ["daus", "glong"],
                    "Dragon04": ["lboy", "lboyd"],
                    "Skink01": ["cpan", "gqueen", "lmod"],
                    "Skink02": ["ecun"],
                    "Skink03": ["edep"],
                    "Varanid01": ["vgoul"],
                    "Varanid02": ["vbari", "vcaud", "vstorr"]}
species_tmp = []
temp = re.compile("([a-zA-Z]+)")
for key in lizardgroups_DLC.keys():
    res = temp.match(key).groups()
    species_tmp.append(res[0])
# only keep unique species names in list:
species = list(set(species_tmp))
print("species: ", species)

lizardgroups_species = {}
for spec in species:
    lizardgroups_species[spec] = [lizardgroups_DLC[key] for key in lizardgroups_DLC.keys() if spec in key]
    # flatten values:
for key in lizardgroups_species.keys():
    nested_list = lizardgroups_species[key]
    lizardgroups_species[key] = [code for sublist in nested_list for code in sublist]
print(lizardgroups_species)


# DEFINING FUNCTIONS:
def splitall(path):
    """
    splits the passed path in all it's components. All components will be returned in list.
    :param path:
    :return: list of all components
    """
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


def convert_videos_to_ImageJ_format(video_dir):
    """
    converts the videos in selected folder (e.g. Gecko02) from .avi format with h.264 codec to nv12
    so it becomes usable with ImageJ.
    The resulting raw_video files will have huge filesizes
    :param video_dir: filepath of the selected folder containing the videos
    :return:
    """
    # ImageJ can't read in .avi videos with h.264 codec
    # convert .avi videos to useable format:
    # ffmpeg -i infile.avi -pix_fmt nv12 -f avi -vcodec rawvideo outfile.avi
    import os
    import subprocess

    dst_dir = os.path.join(video_dir, "converted_nv12_files")

    for root, dirs, files in os.walk(video_dir):
        for f in files:
            prefix, suffix = os.path.splitext(f)
            if '.avi' == suffix:
                abspath_in = os.path.join(root, f)
                dir_out = root.replace(video_dir, dst_dir)
                if not os.path.exists(dir_out):
                    os.makedirs(dir_out)
                abspath_out = os.path.join(dir_out, '{}.avi'.format(prefix))
                subprocess.call(['ffmpeg', '-i', abspath_in,
                                 '-pix_fmt', 'nv12', '-f', 'avi', '-vcodec', 'rawvideo', abspath_out])


def nano17_openCV_as_ImageJ():
    from glob import glob
    import os
    import nano17_calibration
    import auxiliaryfunctions
    import math

    tempdir = auxiliaryfunctions.open_gui_to_select_folder()
    #tempdir = "C:/Users/JojoS/Documents/phd/ClimbingRobot_XGen4/ClimbingLizardsVideos_2020/Gecko01/videos_analysis"
    if len(tempdir) > 0:
        print("You chose %s" % tempdir)
    # assumes that videos are in video_analysis inside the folder for the Group [-2]:
    foldername = splitall(tempdir)[-2]
    # print("foldername: ", foldername)   # e.g. Dragon03

    force_analysis_file = "{}_forceAnalysis.csv".format(foldername)
    # looks for and reads in "*_forceAnalysis.csv" file in tempdir folder:
    df_force_analysis = pd.read_csv(os.path.join(tempdir, force_analysis_file))
    # check if columns footfall_begin & footfall_end contain entries != NaN
    check_columns = ["footfall_begin", "footfall_end"]
    for col in check_columns:
        if df_force_analysis[col].isnull().values.all():
            print("determine and enter frame number for {} to continue".format(col))
            return

    # get row number of csv file (needed to iterate through rows, in case videos are used multiple times:
    df_force_analysis.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
    data_rows_count = df_force_analysis.shape[0]  # number of rows already excluded the header

    # filepaths and filenames of videos: needed for accessing videos with opencv
    filelist = glob(os.path.join(tempdir, '*.avi'))
    # extract video filenames from filepaths and assort filename to filepath in dictionary:
    filenames_dict_tmp = {}
    for i in range(len(filelist)):
        filenames_dict_tmp[filelist[i]] = (filelist[i].rsplit(os.sep, 1)[1])
    filenames_dict = dict([(value, key) for key, value in filenames_dict_tmp.items()])  # swap keys and values
    print("filenames dictionary: ", filenames_dict)

    # requires number of frames of video
    # store box_coords, centre point, and distances from center to footfall: x_calib, y_calib
    calib_dict = {"file":[],
                  "family":[],
                  "code":[],
                  "video_frame_count":[],
                  "footfall_frames_boe":[],
                  "box_coords":[],
                  "center_points":[],
                  "footfall_points":[],
                  "foot":[],
                  "x_calibs":[],
                  "y_calibs":[],
                  "notes":[]}
    #for filepath, filename in zip(filelist, filenames):
    for j in range(data_rows_count):
        # get filename and filepath for current row item:
        filename = df_force_analysis.loc[j, "filename"]
        filepath = filenames_dict[filename]

        # looks for begin and end frame of current file
        #index = df_force_analysis[df_force_analysis["filename"] == filename].index[0]
        beg_frame = df_force_analysis.loc[j, "footfall_begin"]
        end_frame = df_force_analysis.loc[j, "footfall_end"]
        if math.isnan(beg_frame) == False and math.isnan(end_frame) == False:
            open_frame = int(round(end_frame - ((end_frame-beg_frame)/2), 0))
        else:
            open_frame = np.nan
        boe = [beg_frame, open_frame, end_frame]
        family = df_force_analysis.loc[j, "family"]
        code = df_force_analysis.loc[j, "code"]
        frame_count = df_force_analysis.loc[j, "videoFrameCount"]

        foot = df_force_analysis.loc[j, "foot"]

        print("\nfilename: {}, index: {}, beg_frame: {}, end_frame: {}, open_frame: {}".format(filename, j, beg_frame, end_frame, open_frame))

        # open frame nr. middle between footfall_begin & footfall_end
        # TODO: https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/

        if math.isnan(open_frame) == False:
            box_coords, p1, p2, x_calib, y_calib = nano17_calibration.calibrate_x_y_cop_nano17(open_frame, filepath, filename, tempdir, foot)
        else:
            box_coords = [(np.nan, np.nan), (np.nan, np.nan)]
            p1 = (np.nan, np.nan)
            p2 = (np.nan, np.nan)
            x_calib = np.nan
            y_calib = np.nan

        calib_dict["family"].append(family)
        calib_dict["code"].append(code)
        calib_dict["video_frame_count"].append(frame_count)
        calib_dict["footfall_frames_boe"].append(boe)
        calib_dict["notes"].append(df_force_analysis.loc[j, "notes"])
        calib_dict["file"].append(filename)
        calib_dict["box_coords"].append(box_coords)
        calib_dict["center_points"].append(p1)
        calib_dict["footfall_points"].append(p2)
        calib_dict["x_calibs"].append(x_calib)
        calib_dict["y_calibs"].append(y_calib)
        calib_dict["foot"].append(foot)
        #print("calib_dict: ", calib_dict)

    # print every key-value pair in new line:
    print("calib dict: ")
    print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in calib_dict.items()) + "}")

    # do 3 factor calibration to convert calib distances in mm -> this will lead to open GUI
    calib_dict_converted, df_conv, conversion_factor = do_three_factor_calibration(calib_dict)

    # store calibration distances in csv
    auxiliaryfunctions.write_df_to_csv(tempdir, "{}_forceAnalysis_calib.csv".format(foldername), df_conv)

    return


def do_three_factor_calibration(calib_dict):
    import math
    # w = 50mm, h = 50mm, d = 70.711 mm
    # needs video resolution
    w = 50.
    h = 50.
    d = 70.711
    calib_dict_converted = {"file": [], "family":[], "code":[], "video_frame_count":[], "framerate":[], "foot":[],
                            "footfall_begin": [], "footfall_end": [], "open_frame": [],
                            "CoP": [], "footfall_point":[], "conversion_factor":[], "x_calib_mm": [], "y_calib_mm": [],
                            "notes":[]}
    for i in range(len(calib_dict["file"])):
        filename = calib_dict["file"][i]
        CoP = calib_dict["center_points"][i]
        footfall_point = calib_dict["footfall_points"][i]
        boe = calib_dict["footfall_frames_boe"][i]
        footfall_begin = boe[0]
        open_frame = boe[1]
        footfall_end = boe[2]
        foot = calib_dict["foot"][i]
        box_coords = calib_dict["box_coords"][i]    # e.g. [(552, 238), (690, 383)]
        note = calib_dict["notes"][i]
        framerate = np.nan  # empty cell for framerate to fill in later

        if math.isnan(box_coords[0][0]) == False:
            #determine the px to mm conversion factor:
            box_width_px = abs(box_coords[0][0]-box_coords[1][0])
            box_height_px = abs(box_coords[0][1]-box_coords[1][1])
            conversion_factor = (box_width_px/w + box_height_px/h)/2.

            # convert calibration values to mm:
            x_calib_mm = round(calib_dict["x_calibs"][i]/conversion_factor, 3)
            y_calib_mm = round(calib_dict["y_calibs"][i]/conversion_factor, 3)

        else:
            conversion_factor = np.nan
            x_calib_mm = np.nan
            y_calib_mm = np.nan

        # append new values to calib_dict_converted:
        calib_dict_converted["file"].append(filename)
        calib_dict_converted["family"].append(calib_dict["family"][i])
        calib_dict_converted["code"].append(calib_dict["code"][i])
        calib_dict_converted["video_frame_count"].append(calib_dict["video_frame_count"][i])
        calib_dict_converted["foot"].append(foot)
        calib_dict_converted["footfall_begin"].append(footfall_begin)
        calib_dict_converted["open_frame"].append(open_frame)
        calib_dict_converted["footfall_end"].append(footfall_end)
        calib_dict_converted["CoP"].append(CoP)
        calib_dict_converted["footfall_point"].append(footfall_point)
        calib_dict_converted["conversion_factor"].append(conversion_factor)
        calib_dict_converted["x_calib_mm"].append(x_calib_mm)
        calib_dict_converted["y_calib_mm"].append(y_calib_mm)
        calib_dict_converted["notes"].append(note)
        calib_dict_converted["framerate"].append(framerate)

    # print every key-value pair in new line:
    print("calib dict converted: ")
    print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in calib_dict_converted.items()) + "}")
    df_conv = pd.DataFrame.from_dict(calib_dict_converted)
    #print(df_conv)

    return calib_dict_converted, df_conv, conversion_factor


def import_force_data_files():
    from glob import glob

    filelist = glob(os.path.join(destfolder, '*_morph.csv'))


