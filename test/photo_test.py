import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
cap.set(cv2.CAP_PROP_EXPOSURE,10)

ret, frame = cap.read()
frame = cv2.flip(frame,-1)
cv2.imwrite('sample9_0m.jpg', frame)
print(cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
print(cap.get(cv2.CAP_PROP_EXPOSURE))

cap.release()
cv2.destroyAllWindows()
