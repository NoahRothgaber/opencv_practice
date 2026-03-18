import cv2
import numpy as np

img = cv2.imread("images/02_mustard.jpg")
resized = cv2.resize(img, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)

hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

# Yellow in OpenCV HSV:
# H: ~20-35 (OpenCV H is 0-179), S: fairly high, V: fairly high
lower = np.array([20, 80, 80], dtype=np.uint8)
upper = np.array([35, 255, 255], dtype=np.uint8)

mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(resized, resized, mask=mask)

cv2.imshow("images", np.hstack([resized, output]))
cv2.waitKey(0)