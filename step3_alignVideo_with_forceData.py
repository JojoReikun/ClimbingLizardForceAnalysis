"""
STEP 3:
This step uses the data frame from step 2 (e.g.: "Gecko01_forceAnalysis_calib.csv"), which includes frame count and frame
rate of each video, and aligns the videos with the respective force data...

Requires: folder with all force data .txt files which are names in the same way as it's saved in the data frame:
--> e.g.: gdub2_down_23.txt

All force data files for the geckos are stored in folder: forceData_geckos

TODO:

- read in the data frame from step2 if it exists
- loop through all rows:
    - get frame count and frame rate of video
    - get number of force data rows per frame of video --> sampling rate force/video frame rate
    - e.g.: gdub2_up_22
        video length: 405
        video frame rate: 250
        if foot fall at frame 180 --> this corresponds to force row:
        90000 - (405-180)*(10000/250) = 81000
        the footfall at frame 180 in the video file should be equivalent to row 81000 in the force data file
"""