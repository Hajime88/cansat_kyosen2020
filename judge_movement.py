from motor_final import *
import cv2
from camera import *



def judge_movement(center_diff, max_size):
    ###終了条件:要計測
    if max_size > 1000:
        destroy()
        while True:
            print("GOAL!!!")
                  
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

def capture_judge(bgr, not_detect_counter):
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        #画像の上下左右反転
        RevImg = cv2.flip(img,-1)
        cv2.imwrite("image.jpg",RevImg)
        ThreshImage = img_thresh(RevImg,bgr)
        cv2.imwrite("BWimage.jpg",ThreshImage)
        object_centerX, max_size, not_detect_counter = calc_center(ThreshImage)
        print("centerX : " + str(object_centerX))

        #画面中心のX座標
        screen_centerX = RevImg.shape[1]/2
        center_diff = object_centerX - screen_centerX
        print(center_diff)
        judge_movement(center_diff,max_size)
        return not_detect_counter


