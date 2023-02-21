bgr = [10,10,130]

class MOTOR_CTL:

    #放出検知
    def release_detect():

    #落下検知
    def drop_detect():

    #パラシュート分離
    def sep_parachute():

    #位置推定
    def estimate_pos():
        angle = 0
        return angle

    ##モーター##
    def turn_right(angle):

    def turn_left(angle):

    def turn(angle):
        if angle <= 0:
            turn_right(abs(angle))
        if angle >0:
            turn_left(angle)

    def go_straight():

    def img_thresh(img,bgr):

    def calc_center(ThreshImage):

    def  main():

        #例えばwhileループとかで待ち作る？
        while release_detect()==0:
            print("False")
        #落下検知も放出検知と同様
        drop_detect()
        sep_parachute()
        angle = estimate_pos()
        turn(angle)
        go_straight()
        #画像取得

    while True:

        #photo_read()はラズパイのカメラから画像を読み込む関数
        img = photo_read()
        ThreshImage = img_thresh(img,bgr)
        object_centerX = calc_center(ThreshImage)[0]
        #画面中心のX座標
        screen_centerX = img.shape[1]/2

        #物体の重心座標の位置によって回転方向決める
        if object_centerX > screen_centerX:
            turn_right()
        elif object_centerX < screen_centerX:
            turn_left()
        else:
            go_straight()
        
        """
        終了条件を満たせばwhileループから抜け出す
        if ~~  終了条件
            break
        """

        while True:
            print("Goal!")

main()

