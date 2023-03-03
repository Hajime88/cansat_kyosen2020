import cv2 as cv
import numpy as np


#画像から赤の成分を取り出して二値化する関数
def img_thresh(img,bgr):
    thresh = 40

    #色の閾値
    minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
    maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])

    #画像の2値化
    ThreshImage = cv.inRange(img,minBGR,maxBGR)

    #cv.imshow("Result", maskBGR)
    return ThreshImage

#二値画像において白くなっている部分(実際には赤い部分)についてラベリングをして、最大の面積のラベルの重心を求める関数
def calc_center(ThreshImage):

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
        centerY = center[num][1]
        return centerX, centerY, max_size

    else:
        print("not detect Redcorn")
        centerX = 350
        centerY = 0
        return centerX, centerY


