####################################################################
## Run 'opencv_test\env\Scripts\Activate.ps1' befor run this file ##
####################################################################

import cv2 as cv
import numpy as np
import random
import copy

#cap = cv.VideoCapture(0)   ##pcカメラから画像取得の場合この二行を使う
#ret, img = cap.read()
img = cv.imread("test\sample9_0m.jpg")

#画像のサイズを小さくする（前処理）
height = img.shape[0]
width = img.shape[1]
#resized_img = cv.resize(img,(round(width), round(height)))
print("image size is", height ,width)

# HSVに変換
resized_img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#cv.imshow("HSV", resized_img_HSV)

#赤を抽出
low_hsv_min = np.array([0, 108, 30]) #108
low_hsv_max = np.array([4, 256, 256]) #4

#画像の2値化（Hueが0近辺）
maskHSV_low = cv.inRange(resized_img_HSV,low_hsv_min,low_hsv_max)

high_hsv_min = np.array([168, 108, 30]) #177
high_hsv_max = np.array([180, 256, 256])

#画像の2値化（Hueが179近辺）
maskHSV_high = cv.inRange(resized_img_HSV,high_hsv_min,high_hsv_max)

#２つの領域を統合
hsv_mask = maskHSV_low | maskHSV_high

#画像のマスク（合成）
resultHSV = cv.bitwise_and(img, img, mask = hsv_mask)


# ラベリング処理
label = cv.connectedComponentsWithStats(hsv_mask)

# オブジェクト情報を項目別に抽出
n = label[0] - 1
data = np.delete(label[2], 0, 0)
center = np.delete(label[3], 0, 0)
size = []

# オブジェクト情報を利用してラベリング結果を画面に表示
for i in range(n):

    # 各オブジェクトの外接矩形を赤枠で表示
    x0 = data[i][0]
    y0 = data[i][1]
    x1 = data[i][0] + data[i][2]
    y1 = data[i][1] + data[i][3]

    cv.rectangle(resultHSV, (x0, y0), (x1, y1), (0, 0, 255))

    size.append(data[i][4])

max_size = max(size)
num = size.index(max_size)
center_x = center[num][0]
center_y = center[num][1]

print("centerX : " + str(center_x))
print("centerY : " + str(center_y))
print(max_size)

cv.putText(resultHSV, "X: " + str(int(center_x)), (x1 - 30, y1 + 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
cv.putText(resultHSV, "Y: " + str(int(center_y)), (x1 - 30, y1 + 30), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))


cv.imshow("Result mask", hsv_mask)
cv.imshow("Result HSV", resultHSV)
cv.imshow("raw img", img)

cv.waitKey(0)
cv.destroyAllWindows()
