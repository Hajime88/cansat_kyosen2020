from motor_final import *
import cv2
from camera import *
from serialsend import *

def judge_movement(center_diff):
    ###終了条件:要計測
                  
    if center_diff > 62:
        serial_write("turn right!!")
        rotation(-10)
    elif center_diff < -62:
        serial_write("turn left!!")
        rotation(10)
    else :
        serial_write("forward!!")

def sixty_turn(red_zone):
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    #画像の上下左右反転
    RevImg = cv2.flip(img,-1)
    cv2.imwrite("image.jpg",RevImg)
    ThreshImage = img_thresh(RevImg)
    cv2.imwrite("BWimage.jpg",ThreshImage)
    object_centerX, max_size = calc_center(ThreshImage)
    serial_write("centerX : " + str(object_centerX))
    serial_write("max_size: "+str(max_size))
    screen_centerX = RevImg.shape[1]/2
    center_diff = object_centerX - screen_centerX
    serial_write("center_diff:"+str(center_diff)) #中心位置と赤の重心との差
    cap.release()

    
    if max_size > 75:
        if center_diff > 100:
            red_zone = "Left"
        elif center_diff < -100:
            red_zone = "Right"
        else:
            red_zone = "Center"
        serial_write(red_zone)
        return red_zone, max_size
    else:
        if red_zone == "Right":
            rotation(-60)
        else:
            rotation(60)
    
    return "None", 0




# def capture_judge(cap):
#         #rotation_counter = 0
#         #cap = cv2.VideoCapture(0)
#         #cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
#         #cap.set(cv2.CAP_PROP_EXPOSURE,10)
#         ret, img = cap.read()
#         #画像の上下左右反転
#         RevImg = cv2.flip(img,-1)
#         cv2.imwrite("image.jpg",RevImg)
#         ThreshImage = img_thresh(RevImg)
#         cv2.imwrite("BWimage.jpg",ThreshImage)
#         object_centerX, max_size = calc_center(ThreshImage)
#         serial_write("first_centerX : " + str(object_centerX))
#         serial_write("first_max_size: "+str(max_size))
#         #画面中心のX座標
#         while rotation_counter < 5:
#             if max_size > 100:
#                 while max_size < 1000:
#                     screen_centerX = RevImg.shape[1]/2
#                     center_diff = object_centerX - screen_centerX
#                     serial_write("center_diff:"+str(center_diff)) #中心位置と赤の重心との差

#                     forward(1) #とりあえず1m直進

#                     # judge_movement(center_diff)
#                     # ret, img = cap.read()
#                     # RevImg = cv2.flip(img,-1)
#                     # cv2.imwrite("image.jpg",RevImg)
#                     # ThreshImage = img_thresh(RevImg)
#                     # cv2.imwrite("BWimage.jpg",ThreshImage)
#                     # object_centerX, max_size = calc_center(ThreshImage)
#                     # serial_write("centerX : " + str(object_centerX))
#                     # serial_write("max_size: "+str(max_size))
#                 brake()
#                 while True:
#                     serial_write("Goal!!!")
                
#             else:
#                 while max_size < 100 and rotation_counter < 5:
#                     rotation(60)
#                     rotation_counter = rotation_counter+1
#                     serial_write("Rotation 60 degree!")
#                     ret, img = cap.read()
#                     RevImg = cv2.flip(img,-1)
#                     cv2.imwrite("image.jpg",RevImg)
#                     ThreshImage = img_thresh(RevImg)
#                     cv2.imwrite("BWimage.jpg",ThreshImage)
#                     object_centerX, max_size = calc_center(ThreshImage)
#                     serial_write("centerX : " + str(object_centerX))
#                     serial_write("max_size: "+str(max_size))
#                     serial_write("rotation_counter: "+str(rotation_counter))
#         rotation(60)

def capture_judge():
    rotation_counter = 0
    red_zone = "None"
    while rotation_counter < 6:
        serial_write("rotation_counter="+str(rotation_counter))
        red_zone, max_size = sixty_turn(red_zone)

        while max_size != 0:
            forward(1) #とりあえず1m直進

            if red_zone == "Left":
                search_counter = 0
                while search_counter < 3:
                    red_zone, max_size = sixty_turn(red_zone)
                    if max_size == 0:
                        search_counter += 1
                        flag = 0
                    else:
                        flag = 1
                        break
                
                if flag == 0:
                    forward(1)
                    rotation(-120)
                    break
                
                    
            
            elif red_zone == "Right":
                search_counter = 0
                while search_counter < 3:
                    red_zone, max_size = sixty_turn(red_zone)
                    if max_size == 0:
                        search_counter += 1
                        flag = 0
                    else:
                        flag = 1
                        break
                
                if flag == 0:
                    forward(1)
                    rotation(120)
                    break
            
            else:
                search_counter = 0
                while search_counter < 6:
                    red_zone, max_size = sixty_turn(red_zone)
                    if max_size == 0:
                        search_counter += 1
                        flag = 0
                    else:
                        flag = 1
                        break
                
                if flag == 0:
                    rotation(180)
                    forward(1)
                    rotation(-120)
                    break
            
            #ゴールへ到着
            if max_size > 5000:
                for i in range(10):
                    serial_write("max_size>5000 -> Go to Goal!!!")
                #まず一回写真を取る
                cap = cv2.VideoCapture(0)
                ret, img = cap.read()
                #画像の上下左右反転
                RevImg = cv2.flip(img,-1)
                cv2.imwrite("image.jpg",RevImg)
                ThreshImage = img_thresh(RevImg)
                cv2.imwrite("BWimage.jpg",ThreshImage)
                object_centerX, max_size = calc_center(ThreshImage)
                serial_write("centerX : " + str(object_centerX))
                serial_write("max_size: "+str(max_size))
                screen_centerX = RevImg.shape[1]/2
                center_diff = object_centerX - screen_centerX
                serial_write("center_diff:"+str(center_diff)) #中心位置と赤の重心との差
                cap.release()

                while max_size < 50000:

                    judgement_counter = 0
                    while abs(center_diff) > 62 and judgement_counter < 10:
                        judge_movement(center_diff)
                        cap = cv2.VideoCapture(0)
                        ret, img = cap.read()
                        #画像の上下左右反転
                        RevImg = cv2.flip(img,-1)
                        cv2.imwrite("image.jpg",RevImg)
                        ThreshImage = img_thresh(RevImg)
                        cv2.imwrite("BWimage.jpg",ThreshImage)
                        object_centerX, max_size = calc_center(ThreshImage)
                        serial_write("centerX : " + str(object_centerX))
                        serial_write("max_size: "+str(max_size))
                        screen_centerX = RevImg.shape[1]/2
                        center_diff = object_centerX - screen_centerX
                        serial_write("center_diff:"+str(center_diff)) #中心位置と赤の重心との差
                        cap.release()

                        judgement_counter += 1
                
                    forward(0.3)

                forward(0.7)
                while True:
                    serial_write("Goal!!!!!!!!!!!!")
        
        rotation_counter += 1









            


