import os

current_path = os.getcwd()

#################################################
convert = False
flipping = True
#################################################


def get_list_of_videos(current_path, videoformat='avi'):
    # gui open folder to select folder with videos to be converted, default: .avi videos
    import os
    from glob import glob
    from tkinter import filedialog, Tk
    import os

    root = Tk()
    root.withdraw()  # use to hide tkinter window

    tempdir = filedialog.askdirectory(parent=root, initialdir=current_path,
                                        title='Please select a directory containing the videos to be converted (e.g.: "Gecko02")')
    if len(tempdir) > 0:
        print("You chose %s" % tempdir)
    filelist = glob(os.path.join(tempdir, '*.{}'.format(videoformat)))
    # extract filenames from filepaths:
    filenames = []
    for i in range(len(filelist)):
        filenames.append(filelist[i].rsplit(os.sep, 1)[1])
    print("files in filelist: ")
    print(*filelist, sep='\n')

    print("\n{} video files have been found in directory".format(len(filelist)))

    return filelist, tempdir, videoformat


def convert_videos_to_ImageJ_format(video_dir, videoformat, outputformat="nv12"):
    """
    converts the videos in selected folder (e.g. Gecko02) from .avi format with h.264 codec to nv12
    so it becomes usable with ImageJ.
    The resulting raw_video files will have huge filesizes
    :param video_dir: filepath of the selected folder containing the videos
    :param outputformat: choose if videos should be converted to a different format or remain same (e.g. only flip video)
                         options: "nv12" TODO: extend
    :return:
    """
    # ImageJ can't read in .avi videos with h.264 codec
    # convert .avi videos to useable format:
    # ffmpeg -i infile.avi -pix_fmt nv12 -f avi -vcodec rawvideo outfile.avi
    import os
    import subprocess

    dst_dir = os.path.join(video_dir, "converted_video_files")

    for root, dirs, files in os.walk(video_dir):
        for f in files:
            prefix, suffix = os.path.splitext(f)
            if '.avi' == suffix:
                abspath_in = os.path.join(root, f)
                dir_out = root.replace(video_dir, dst_dir)
                if not os.path.exists(dir_out):
                    os.makedirs(dir_out)
                abspath_out = os.path.join(dir_out, '{}.{}'.format(prefix, videoformat))
                # TODO: define different case scenarios
                if outputformat == "nv12":
                    #TODO: change to ffmpeg python instead of subprocess
                    subprocess.call(['ffmpeg', '-i', abspath_in,
                                     '-pix_fmt', 'nv12', '-f', 'avi', '-vcodec', 'rawvideo', abspath_out])


def flip_videos(video_dir, hflip=False, vflip=True):
    #TODO: set hflip and vflip via checkbox gui
    import os
    import subprocess

    dst_dir = os.path.join(video_dir, "flipped_video_files")

    for root, dirs, files in os.walk(video_dir):
        for f in files:
            prefix, suffix = os.path.splitext(f)
            if '.avi' == suffix:
                abspath_in = os.path.join(root, f)
                dir_out = root.replace(video_dir, dst_dir)
                if not os.path.exists(dir_out):
                    os.makedirs(dir_out)

                if hflip == True and vflip == False:
                    flip = 'hflip'
                elif hflip == True and vflip == True:
                    flip = 'hlip-vflip'
                elif hflip == False and vflip == True :
                    flip = 'vflip'
                else:
                    print("no flipping executed, because hflip and vflip are false")
                    break

                abspath_out = os.path.join(dir_out, f'{prefix}_{flip}.avi')

                # TODO: change to ffmpeg python instead of subprocess
                #ffmpeg -i INPUT -vf vflip -c:a copy OUTPUT
                if vflip == True and hflip == False:
                    subprocess.call(['ffmpeg', '-i', abspath_in, '-vf', 'vflip', 'copy', abspath_out])
                if hflip == True and vflip == False:
                    subprocess.call(['ffmpeg', '-i', abspath_in, '-vf', 'hflip', 'copy', abspath_out])
                if vflip == True and hflip == True:
                    subprocess.call(['ffmpeg', '-i', abspath_in, '-vf', 'hflip, vflip', 'copy', abspath_out])


# lets user choose the folder containing the videos via gui:
filelist, video_dir, videoformat = get_list_of_videos(current_path, videoformat="avi")
if convert == True:
    # converts videos in folder to selected format (currently only nv12 programmed to use video in ImageJ):
    convert_videos_to_ImageJ_format(video_dir, videoformat)
if flipping == True:
    flip_videos(video_dir)