import pandas as pd
import os
import re

"""
STEP1:
This function is called if Step1 is selected. It is required to run this before executing Step2 for the first time.
A gui will open which asks the user to open a folder following a structure like the following exemplary one:
--> e.g.: "C:/Users/JojoS/Documents/phd/ClimbingRobot_XGen4/ClimbingLizardVideos_2020/Gecko01/video_analysis"
This folder contains all Gecko videos (.avi) for the Gecko01 group.

All files will be read in and some video information will be extracted. A dataframe called:
--> e.g.: "Gecko01_forceAnalysis.csv" will be saved in the same folder as above.
"""


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
#print("species: ", species)

lizardgroups_species = {}
for spec in species:
    lizardgroups_species[spec] = [lizardgroups_DLC[key] for key in lizardgroups_DLC.keys() if spec in key]
    # flatten values:
for key in lizardgroups_species.keys():
    nested_list = lizardgroups_species[key]
    lizardgroups_species[key] = [code for sublist in nested_list for code in sublist]
#print(lizardgroups_species)


# DEFINING FUNCTIONS:
def get_list_of_videos(current_path):
    # DLC group wise
    # gui open folder to select folder with lizard videos
    from glob import glob
    import os
    import auxiliaryfunctions

    tempdir = auxiliaryfunctions.open_gui_to_select_folder('STEP1: Please select a directory containing lizard videos (e.g.: "ClimbingLizardVideos_2020/Gecko02/video_analysis")')
    #tempdir = "C:/Users/JojoS/Documents/phd/ClimbingRobot_XGen4/ClimbingLizardsVideos_2020/Varanid01/video_analysis"
    if len(tempdir) > 0:
        print("You chose %s" % tempdir)
    # assumes that videos are in video_analysis inside the folder for the Group:
    foldername = auxiliaryfunctions.splitall(tempdir)[-2]
    #print("foldername: ", foldername)   # e.g. Dragon03
    filelist = glob(os.path.join(tempdir, '*.avi'))
    # extract filenames from filepaths:
    filenames = []
    for i in range(len(filelist)):
        filenames.append(filelist[i].rsplit(os.sep, 1)[1])
    #print("files in filelist: ")
    #print(*filelist, sep='\n')
    #print("filenames: ", filenames)

    print("{} files found in directory {}".format(len(filelist), foldername))

    return filelist, tempdir, filenames, foldername


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


def get_name_code(filenames, foldername, filelist, video_dir):
    import auxiliaryfunctions

    # get name and number of individual
    # TODO: get family of individual -> use dict above
    # TODO: get run number: either run15 or up_15
    new_row = {}
    codenames = {}
    # footfall_begin, footfall_end & foot are columns for later manually add frame numbers and foot: [FL, FR, HR, or HL]
    df = pd.DataFrame(columns=["filename", "code", "videoFrameCount", "family", "footfall_begin", "footfall_end", "foot", "notes"])

    for file, i in zip(filenames, range(len(filelist))):
        filename = file.rsplit(".", 1)[0]
        temp = re.compile("([a-zA-Z]+)([0-9]+)")
        res = temp.match(filename).groups()
        individual = str(res[0] + res[1])
        individual_spec = res[0]
        codenames[file] = individual
        new_row["filename"] = file
        new_row["code"] = individual
        frame_count_video = get_video_frame_count(filelist[i])['frames']
        new_row["videoFrameCount"] = frame_count_video
        for k,v in lizardgroups_species.items():
            if individual_spec in v:
                family = k
                new_row["family"] = family
        #print("new row: ", new_row)
        df = df.append(new_row, ignore_index=True)
    print(df)

    # save df as csv to then manually add the frame numbers for the footfall to analyze
    auxiliaryfunctions.write_df_to_csv(video_dir, "{}_forceAnalysis.csv".format(foldername), df)

    print("Before Step2 is executed footfall begin and end frames of good steps will have to be extracted from the videos by the user!!")

    # print codenames dict nicely:
    #print("codenames: ")
    #print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in codenames.items()) + "}")
    return codenames


def get_video_resolution():
    import ffmpeg
    #use ffmpeg
    return


def get_video_frame_count(fileloc):
    #import ffmpeg
    import subprocess
    # ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 input.mp4
    command = ['ffprobe',
               '-v', 'error',
               '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames', '-of',
               'default=nokey=1:noprint_wrappers=1', fileloc
               ]
    ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = ffmpeg.communicate()
    if (err): print(err)
    out = out.decode()  # converts byte like output of ffmpeg to string
    # extract number sequence = frame count from output:
    temp = re.compile("([0-9]+)")
    res = temp.match(out).groups()
    frame_count = str(res[0])
    return {'file': fileloc,
            'frames': frame_count}


def detect_forceplate():
    #use openCV
    # do at frame at 20% of frame number -> animal not covering forceplate
    return



