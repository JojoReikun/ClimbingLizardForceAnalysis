import cv2
import os


def calibrate_x_y_cop_nano17(open_frame, file, filename, tempdir, foot):
    """
    This function gets called from the step2_lizard_force_data_analysis.py module, when working in Step2 of the program.
    Step2 requires the video folder:
       --> e.g. "C:/Users/JojoS/Documents/phd/ClimbingRobot_XGen4/ClimbingLizardsVideos_2020/Gecko01/videos_analysis"
    which contains all the raw .avi videos of the geckos and the respective .csv file from step1
       --> e.g.: Gecko01_forceAnalysis.csv
    If a proper footfall was detected and is entered in the
    :param open_frame:
    :param file:
    :param filename:
    :param tempdir:
    :param foot:
    :return:
    """
    refPt_box = []
    refPt_dist = []

    def click_and_draw_box(event, x, y, flags, param):
        global refPt_box
        global refPt_dist
        global box_coords
        global p1
        global p2
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being performed
        if event == cv2.EVENT_LBUTTONDOWN:  # start box
            refPt_box = [(x, y)]
        # check to see if the left mouse button was released after dragging
        elif event == cv2.EVENT_LBUTTONUP:  # end box
            # record the ending (x, y) coordinates
            refPt_box.append((x, y))
            box_coords = refPt_box
            # draw a rectangle around the region of interest
            cv2.rectangle(frame, refPt_box[0], refPt_box[1], (0, 255, 0), 2)
            # calculate centre of rectangle:
            center_x, center_y = calc_center_of_rectangle(refPt_box, frame, draw_text=True)
            p1=(center_x, center_y)
            # draw circle in middle of rectangle
            cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), 2)
            cv2.imshow("image", frame)
            return p1, box_coords
        elif event == cv2.EVENT_RBUTTONUP:
            # save location of footfall point
            refPt_dist = [(x, y)]
            # draw a point at clicked location
            p2=(refPt_dist[0][0], refPt_dist[0][1])
            cv2.circle(frame, (refPt_dist[0][0], refPt_dist[0][1]), 2, (0, 145, 230), 2)
            cv2.imshow("image", frame)
            return p2


    # load the image, clone it, and setup the mouse callback function
    # load the video at openFrame:
    cap = cv2.VideoCapture(file)
    cap.set(1, open_frame)  # Where open_frame is the frame to be opened (mid footfall)
    ret, frame = cap.read()  # Read the frame

    # display the current frame and video on frame:
    cv2.putText(frame, 'confirm operations with KEY: c, reset with KEY r, next video with KEY n',
                (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (222, 120, 0), 1)
    cv2.putText(frame, ('frame: {} of video: {} -- foot: {}'.format(open_frame, filename, foot)),
                (20, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 180, 0), 1)
    # clone the image to reset box
    clone = frame.copy()

    # display operation 1:
    cv2.putText(frame, '1st) Draw box around the force plate with LButton Mouse',
                (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (222, 120, 0), 1)
    # display operation 2:
    cv2.putText(frame, '2nd) Click on the foot of lizard which is on force plate with RButton Mouse',
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (222, 120, 0), 1)

    cv2.imshow("image", frame)


    # EVENT:
    cv2.setMouseCallback("image", click_and_draw_box)

    next = False
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            frame = clone.copy()
            # display operation 1:
            cv2.putText(frame, '1st) Draw box around the force plate with LButton Mouse',
                        (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (150, 200, 255), 1)
            # display operation 2:
            cv2.putText(frame, '2nd) Click on the foot of lizard which is on force plate with RButton Mouse',
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (222, 120, 0), 1)
            cv2.imshow("image", frame)
            refPt_box = []
        # if the 'c' key is pressed, break from the loop to confirm
        elif key == ord("c"):
            print("points CoP and footfall: ", p1, p2)
            print("box coords: ", box_coords)
            cv2.line(frame, p1, p2, (255, 0, 0), 1)
            # assumes force plate orientation: topright in video/ topleft in racetrack = positive in x and y
            # TODO: think through if this maybe needs more case definitions?!
            x_calib = -1*(p2[0] - p1[0])
            y_calib = -1*(p2[1] - p1[1])
            print("xcalib: ", x_calib, "y_calib: ", y_calib)

            cv2.imshow("image", frame)

            next = True

            # save as image:
            out_dir = os.path.join(tempdir, "calib_footfallframes_labeled")
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            file_save = filename.split(".")[0]
            cv2.imwrite(os.path.join(out_dir, "{}_{}_labeled.png".format(file_save, open_frame)), frame)
            print("saved labeled image {}_labeled".format(file_save))
        elif next == True and key == ord("n"):
            return box_coords, p1, p2, x_calib, y_calib

    # close all open windows
    cv2.destroyAllWindows()


def calc_center_of_rectangle(refPt_box, frame, draw_text):
    if refPt_box[1][0] > refPt_box[0][0] and refPt_box[1][1] > refPt_box[0][1]:  # start topleft
        center_x = round(refPt_box[0][0] + (refPt_box[1][0] - refPt_box[0][0]) / 2)
        center_y = round(refPt_box[0][1] + (refPt_box[1][1] - refPt_box[0][1]) / 2)
        # write text onto frame
        if draw_text:
            cv2.putText(frame, ('corner 1: {}, {}'.format(refPt_box[0][0], refPt_box[0][1])),
                        ((refPt_box[0][0]) - 50, (refPt_box[0][1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
            cv2.putText(frame, ('corner 2: {}, {}'.format(refPt_box[1][0], refPt_box[1][1])),
                        ((refPt_box[1][0]) - 50, (refPt_box[1][1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
    elif refPt_box[1][0] < refPt_box[0][0] and refPt_box[1][1] > refPt_box[0][1]:  # start topright
        center_x = round(refPt_box[1][0] + (refPt_box[0][0] - refPt_box[1][0]) / 2)
        center_y = round(refPt_box[0][1] + (refPt_box[1][1] - refPt_box[0][1]) / 2)
        # write text onto frame
        if draw_text:
            cv2.putText(frame, ('corner 1: {}, {}'.format(refPt_box[0][0], refPt_box[0][1])),
                        ((refPt_box[0][0]) - 50, (refPt_box[0][1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
            cv2.putText(frame, ('corner 2: {}, {}'.format(refPt_box[1][0], refPt_box[1][1])),
                        ((refPt_box[1][0]) - 50, (refPt_box[1][1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)

    elif refPt_box[1][0] < refPt_box[0][0] and refPt_box[1][1] < refPt_box[0][1]:  # start bottomright
        center_x = round(refPt_box[1][0] + (refPt_box[0][0] - refPt_box[1][0]) / 2)
        center_y = round(refPt_box[1][1] + (refPt_box[0][1] - refPt_box[1][1]) / 2)
        # write text onto frame
        if draw_text:
            cv2.putText(frame, ('corner 1: {}, {}'.format(refPt_box[0][0], refPt_box[0][1])),
                        ((refPt_box[0][0]) - 50, (refPt_box[0][1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
            cv2.putText(frame, ('corner 2: {}, {}'.format(refPt_box[1][0], refPt_box[1][1])),
                        ((refPt_box[1][0]) - 50, (refPt_box[1][1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)

    else:
        center_x = round(refPt_box[0][0] + (refPt_box[1][0] - refPt_box[0][0]) / 2)
        center_y = round(refPt_box[1][1] + (refPt_box[0][1] - refPt_box[1][1]) / 2)
        # write text onto frame
        if draw_text:
            cv2.putText(frame, ('corner 1: {}, {}'.format(refPt_box[0][0], refPt_box[0][1])),
                        ((refPt_box[0][0]) - 50, (refPt_box[0][1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
            cv2.putText(frame, ('corner 2: {}, {}'.format(refPt_box[1][0], refPt_box[1][1])),
                        ((refPt_box[1][0]) - 50, (refPt_box[1][1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)
    return center_x, center_y
