# Kinect Writer with Head
# 2025
# Hermann Knopp
# python 3.10.10

# Init
import os
os.system("cls")
print("importing libs...")


# Libs
from datetime import datetime
from random import randrange

import sys
import numpy as np
import cv2
from openni import openni2, nite2, utils
import argparse


GRAY_COLOR = (64, 64, 64)
CAPTURE_SIZE_KINECT = (640, 480)
CAPTURE_SIZE_OTHERS = (640, 480)


def parse_arg():
    parser = argparse.ArgumentParser(description="Test OpenNI2 and NiTE2.")
    parser.add_argument("-w", "--window_width", type=int, default=640, help="Specify the window width.")
    parser.add_argument("-o", "--output_file", type=str, default="test.txt", required=False, help="Specify the output text file for XYZ data.")
    return parser.parse_args()



def draw_limb(img, ut, j1, j2, col, output_file, joint_name):

    # 1. Koordinate skalieren (cm -> m falls nötig)
    x1 = j1.position.x / 10
    y1 = j1.position.y / 10
    z1 = j1.position.z / 10



    # Koordinaten skalieren (cm -> m falls nötig)
    x2 = j2.position.x / 10
    y2 = j2.position.y / 10
    z2 = j2.position.z / 10

    # Mapping NiTE zu Blender-kompatiblen Namen
    joint_map = {
        "NITE_JOINT_HEAD": "Head",
        "NITE_JOINT_NECK": "ShoulderCenter",
        "NITE_JOINT_TORSO": "Hip",
        "NITE_JOINT_LEFT_SHOULDER": "ShoulderLeft",
        "NITE_JOINT_LEFT_ELBOW": "ElbowLeft",
        "NITE_JOINT_LEFT_HAND": "WristLeft",
        "NITE_JOINT_RIGHT_SHOULDER": "ShoulderRight",
        "NITE_JOINT_RIGHT_ELBOW": "ElbowRight",
        "NITE_JOINT_RIGHT_HAND": "WristRight",
        "NITE_JOINT_LEFT_HIP": "HipLeft",
        "NITE_JOINT_LEFT_KNEE": "KneeLeft",
        "NITE_JOINT_LEFT_FOOT": "AnkleLeft",
        "NITE_JOINT_RIGHT_HIP": "HipRight",
        "NITE_JOINT_RIGHT_KNEE": "KneeRight",
        "NITE_JOINT_RIGHT_FOOT": "AnkleRight",
    }

    # Mapping NiTE zu Blender-kompatiblen Namen
    #joint_map = {
    #    "NITE_JOINT_HEAD": "Head",
    #    "NITE_JOINT_NECK": "ShoulderCenter",
    #    "NITE_JOINT_TORSO": "Hip",
    #    "NITE_JOINT_LEFT_SHOULDER": "ElbowLeft",
    #    "NITE_JOINT_LEFT_ELBOW": "ShoulderLeft",
    #    "NITE_JOINT_LEFT_HAND": "WristLeft",
    #    "NITE_JOINT_RIGHT_SHOULDER": "ElbowRight",
    #    "NITE_JOINT_RIGHT_ELBOW": "ShoulderRight",
    #    "NITE_JOINT_RIGHT_HAND": "WristRight",
    #    "NITE_JOINT_LEFT_HIP": "HipLeft",
    #    "NITE_JOINT_LEFT_KNEE": "KneeLeft",
    #    "NITE_JOINT_LEFT_FOOT": "FootLeft",
    #    "NITE_JOINT_RIGHT_HIP": "HipRight",
    #    "NITE_JOINT_RIGHT_KNEE": "KneeRight",
    #    "NITE_JOINT_RIGHT_FOOT": "FootRight",
    #}



    joint_enum_name = str(joint_name).split('.')[-1]
    joint = joint_map.get(joint_enum_name)

    if joint:
        output_file.write(f"{joint} {x1:.2f} {y1:.2f} {z1:.2f} {x2:.2f} {y2:.2f} {z2:.2f}\n")

    # Tiefe für Bilddarstellung
    (x1, y1) = ut.convert_joint_coordinates_to_depth(j1.position.x, j1.position.y, j1.position.z)
    (x2d, y2d) = ut.convert_joint_coordinates_to_depth(j2.position.x, j2.position.y, j2.position.z)

    if 0.4 < j1.positionConfidence and 0.4 < j2.positionConfidence:
        c = GRAY_COLOR if (j1.positionConfidence < 1.0 or j2.positionConfidence < 1.0) else col
        cv2.line(img, (int(x1), int(y1)), (int(x2d), int(y2d)), c, 1)

        c1 = GRAY_COLOR if (j1.positionConfidence < 1.0) else col
        c2 = GRAY_COLOR if (j2.positionConfidence < 1.0) else col
        cv2.circle(img, (int(x1), int(y1)), 2, c1, -1)
        cv2.circle(img, (int(x2d), int(y2d)), 2, c2, -1)






def draw_skeleton(img, ut, user, col, output_file):
    for idx1, idx2 in [
        #Head ---neu
        (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_HEAD),

        #----
        
        #Hip
        (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_TORSO),

        #----
        # Shoulder Center ---neu
        (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_NECK),

        #----
        
        #Left Shoulder 
        (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_LEFT_SHOULDER),
        #(nite2.JointType.NITE_JOINT_LEFT_SHOULDER, nite2.JointType.NITE_JOINT_TORSO),
        
        #Left Elbow 
        (nite2.JointType.NITE_JOINT_LEFT_SHOULDER, nite2.JointType.NITE_JOINT_LEFT_ELBOW),

        #Left Hand  
        (nite2.JointType.NITE_JOINT_LEFT_ELBOW, nite2.JointType.NITE_JOINT_LEFT_HAND), 

        #----

        #Right Shoulder
        (nite2.JointType.NITE_JOINT_NECK, nite2.JointType.NITE_JOINT_RIGHT_SHOULDER),
        
        #Right Elbow  
        (nite2.JointType.NITE_JOINT_RIGHT_SHOULDER, nite2.JointType.NITE_JOINT_RIGHT_ELBOW),
        
        #Right Hand
        (nite2.JointType.NITE_JOINT_RIGHT_ELBOW, nite2.JointType.NITE_JOINT_RIGHT_HAND),

        #----
        
        #Left Hip
        (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_LEFT_HIP),
        
        #Left Knee 
        (nite2.JointType.NITE_JOINT_LEFT_HIP, nite2.JointType.NITE_JOINT_LEFT_KNEE),
        
        #Left Foot
        (nite2.JointType.NITE_JOINT_LEFT_KNEE, nite2.JointType.NITE_JOINT_LEFT_FOOT),

        #----

        #Right Hip
        (nite2.JointType.NITE_JOINT_TORSO, nite2.JointType.NITE_JOINT_RIGHT_HIP),
        
        #Right Knee
        (nite2.JointType.NITE_JOINT_RIGHT_HIP, nite2.JointType.NITE_JOINT_RIGHT_KNEE),

        #Right Foot 
        (nite2.JointType.NITE_JOINT_RIGHT_KNEE, nite2.JointType.NITE_JOINT_RIGHT_FOOT),

        #----        
        
    ]:
        draw_limb(img, ut, user.skeleton.joints[idx1], user.skeleton.joints[idx2], col, output_file, idx2)

    # Frame-Ende markieren
    output_file.write("\n")

     


def init_capture_device():
    openni2.initialize()
    nite2.initialize()
    return openni2.Device.open_any()


def close_capture_device():
    nite2.unload()
    openni2.unload()
    cv2.destroyAllWindows() 

def capture_skeleton():
    args = parse_arg()
    dev = init_capture_device()
    
    dev_name = dev.get_device_info().name.decode("UTF-8")
    print("Device Name: {}".format(dev_name))
    use_kinect = False
    if dev_name == "Kinect":
        use_kinect = True
        print("Using Kinect.")

    depth_stream = dev.create_depth_stream()
    depth_stream.start()



    try:
        user_tracker = nite2.UserTracker(dev)
    except utils.NiteError:
        print(
            "Unable to start the NiTE human tracker. Check "
            "the error messages in the console. Model data "
            "(s.dat, h.dat...) might be inaccessible."
        )
        sys.exit(-1)

    (img_w, img_h) = CAPTURE_SIZE_KINECT if use_kinect else CAPTURE_SIZE_OTHERS
    win_w = args.window_width
    win_h = int(img_h * win_w / img_w)


    # Old Dummy Code for argparse
    # Öffnen der Textdatei zum Schreiben
    #with open(args.output_file, 'w') as output_file:

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    output_file=dir_path + "/motioncapture_" + dt_string +".txt"
    


    # Öffnen der Textdatei zum Schreiben
    with open(output_file, 'w') as output_file:

        print("Enter Main Capture Routine")


        while True:

            #try:  

            ut_frame = user_tracker.read_frame()

            #except Exception as e:
            #    print("Error: ",str(e))
            #    pass 



            #print("Debug2")

            depth_frame = depth_stream.read_frame()
            depth_frame_data = depth_frame.get_buffer_as_uint16()
            img = np.ndarray((depth_frame.height,depth_frame.width),dtype=np.uint16,buffer=depth_frame_data).astype(np.float32)
            if use_kinect:
                img = img[0:img_h, 0:img_w]

            (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(img)
            if min_val < max_val:
                img = (img - min_val) / (max_val - min_val)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            if ut_frame.users:
                for user in ut_frame.users:
                    if user.is_new():
                        print("New person id:{} detected.".format(user.id))
                        user_tracker.start_skeleton_tracking(user.id)
                    elif (user.state == nite2.UserState.NITE_USER_STATE_VISIBLE and user.skeleton.state ==nite2.SkeletonState.NITE_SKELETON_TRACKED):
                        draw_skeleton(img, user_tracker, user, (255, 255, 255), output_file)
                        
                        # 1. Trennline 1 Frame
                        #output_file.write("\n")



            # Bild anzeigen
            cv2.imshow("Depth", cv2.resize(img, (win_w, win_h)))
 
            

            # Um das Bildfenster nicht einfrieren zu lassen, musst du `cv2.waitKey(1)` verwenden
            key = cv2.waitKey(10)  # 1 ms warten, um Fenster zu aktualisieren
            if key == ord("q"):  # Mit 'q' das Programm beenden
                break

    close_capture_device()


if __name__ == "__main__":

    cv2.destroyAllWindows() 

    capture_skeleton()
