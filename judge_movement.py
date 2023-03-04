from motor_final import *
import cv2
from camera import *

def judge_movement(center_diff):
    ###終了条件:要計測
                  
    if center_diff > 100:
        print("turn right!!")
        rotation(-10)
        brake()
    elif center_diff < -100:
        print("turn left!!")
        rotation(10)
        brake()
    else :
        print("forward!!")
        forward(5)
        brake()

def capture_judge(cap):
        rotation_counter = 0
        #cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
        #cap.set(cv2.CAP_PROP_EXPOSURE,10)
        ret, img = cap.read()
        #画像の上下左右反転
        RevImg = cv2.flip(img,-1)
        cv2.imwrite("image.jpg",RevImg)
        ThreshImage = img_thresh(RevImg)
        cv2.imwrite("BWimage.jpg",ThreshImage)
        object_centerX, max_size = calc_center(ThreshImage)
        print("first_centerX : " + str(object_centerX))
        print("first_max_size: "+str(max_size))
        #画面中心のX座標
        while rotation_counter < 5:
            if max_size > 100:
                while 100 < max_size < 1000:
                    screen_centerX = RevImg.shape[1]/2
                    center_diff = object_centerX - screen_centerX
                    print("center_diff:"+str(center_diff))
                    judge_movement(center_diff)
                    ret, img = cap.read()
                    RevImg = cv2.flip(img,-1)
                    cv2.imwrite("image.jpg",RevImg)
                    ThreshImage = img_thresh(RevImg)
                    cv2.imwrite("BWimage.jpg",ThreshImage)
                    object_centerX, max_size = calc_center(ThreshImage)
                    print("centerX : " + str(object_centerX))
                    print("max_size: "+str(max_size))
                brake()
                while True:
                    print("Goal!!!")
                
            else:
                while max_size < 100 and rotation_counter < 5:
                    rotation(60)
                    rotation_counter = rotation_counter+1
                    print("Rotation 60 degree!")
                    ret, img = cap.read()
                    RevImg = cv2.flip(img,-1)
                    cv2.imwrite("image.jpg",RevImg)
                    ThreshImage = img_thresh(RevImg)
                    cv2.imwrite("BWimage.jpg",ThreshImage)
                    object_centerX, max_size = calc_center(ThreshImage)
                    print("centerX : " + str(object_centerX))
                    print("max_size: "+str(max_size))
                    print("rotation_counter: "+str(rotation_counter))
        rotation(60)


