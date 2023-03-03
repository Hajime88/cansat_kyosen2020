import cv2 as cv
import numpy as np

"""
#画像から赤の成分を取り出して二値化する関数(RBGによって)
def img_thresh(img,bgr):
    thresh = 40

    #色の閾値
    minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
    maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])

    #画像の2値化
    ThreshImage = cv.inRange(img,minBGR,maxBGR)

    #cv.imshow("Result", maskBGR)
    return ThreshImage
"""

#画像から赤の成分を取り出して二値化する関数(HSVによって)
def img_thresh(img):
    # HSVに変換
    resized_img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #画像の2値化（Hueが0近辺）
    low_hsv_min = np.array([0, 100, 20])
    low_hsv_max = np.array([5, 255, 255])
    maskHSV_low = cv.inRange(resized_img_HSV,low_hsv_min,low_hsv_max)

    #画像の2値化（Hueが179近辺）
    high_hsv_min = np.array([175, 100, 20])
    high_hsv_max = np.array([179, 255, 255])
    maskHSV_high = cv.inRange(resized_img_HSV,high_hsv_min,high_hsv_max)
    #２つの領域を統合
    ThreshImage = maskHSV_low | maskHSV_high
    return ThreshImage

#二値画像において白くなっている部分(実際には赤い部分)についてラベリングをして、最大の面積のラベルの重心を求める関数
def calc_center(ThreshImage, not_detect_counter):

    # ラベリング処理 
    # label:ラベル数, ラベル番号の配列データ, data, オブジェクトの重心座標
    # data:オブジェクトの外接矩形の左上のx座標、y座標、高さ、幅、 面積
    label = cv.connectedComponentsWithStats(ThreshImage)

    # オブジェクト情報を項目別に抽出
    #背景のラベル番号もカウントされているので-1する
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)
    size = []

    #各ラベルの面積でリストを作る
    for i in range(n):
        size.append(data[i][4])
    
    #最大の面積を求める
    if len(size)!= 0:
        max_size = max(size)
    #最大の面積を持つラベルの重心を出す
        num = size.index(max_size)
        centerX = center[num][0]
        not_detect_counter = not_detect_counter
        return centerX, max_size,  not_detect_counter

    else:
        print("not detect Redcorn")
        centerX = 320
        max_size = 0
        not_detect_counter = not_detect_counter+1
        return centerX, max_size, not_detect_counter


