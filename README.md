## required packages:
* numpy
* pandas
* opencv
* tk
* ffmpeg

## Description:
This script helps to automize the force data analysis. The program is divided into two Steps, which can be run 
independently of each other, though Step 2 requires the output of Step 1 + the manual inclusion of the footfall frames.

#### Step1:
* Run main.py, set Step1=True, Step2=False.
* open the folder in dialog which contains the videos of the lizard eg. .../Gecko01/videos_analysis
* when Step1 is finished, a .csv file (e.g. Gecko01_forceAnalysis.csv) containing all filenames, individual names, video information and 4 empty columns "footfall_begin", "footfall_end", "foot" and "notes will be saved into selected folder

---
**Now you need to add the frame numbers for the footfall and the foot (FL, FR, HR or HL) to this 
csv file. Take notes in the notes column if wanted, they will be transferred to final file. 
Save the file and close.**
---

#### Step2:
* Run main.py, set Step2=True, Step1=False.
* open the folder in dialog which contains the videos of the lizard eg. .../Gecko01/videos_analysis

Note: *Gecko01* will be extarcted for the later filename, hence split[-2]. If all the videos are not in a subfolder, this split argument can be changed to [-1] to get the last part in the string as the later filename!
* a gui will be opened, showing the frame at mid footfall, which will tell you to:

  * 1st) draw a box around the forceplate by clicking on the first corner and dragging LMouseButton to the last corner. 

  * 2nd) Rightclick on the foot on the forceplate. Confirm with "c" or if you misdrew something reset with "r". Click "n" to get to the next video. An image of the drawn box and the footpoint on top of the frame will be saved in the selected folder/calib_footfall_labeled
* once all videos are done this will save a new csv: Gecko01_forceAnalysis_calib.csv containing all infos from the first file + the conversion factor, the coordinates of the box, the CoP of the forceplate, the point of the footfall, the conversion factor px to mm etc.
