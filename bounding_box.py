import numpy as np
import cv2
# Found using colorzilla the browser extension
lower = np.array([20, 80, 80], dtype=np.uint8)
upper = np.array([35, 255, 255], dtype=np.uint8)
# dictionary for the state of the bounding box coords
state = {
    "left_upper" : (0, 0),
    "right_upper" : (0, 0),
    "left_lower" : (0, 0),
    "right_lower" : (0, 0),
    "corner_count" : 0
}
img = cv2.imread("images/02_mustard.jpg")
resized = cv2.resize(img, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(resized, resized, mask=mask)
# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(output,(x,y),5,(0,0,255),-1)
        if param["corner_count"] == 0:
            param["left_upper"] = (x,y)
            print(f'Left_Upper Pixel = {param["left_upper"]}')
        elif param["corner_count"] == 1:
            param["right_upper"] = (x,y)
            print(f'Right_Upper Pixel = {param["right_upper"]}')
        elif param["corner_count"] == 2:
            param["left_lower"] = (x,y)
            print(f'Left_Lower Pixel = {param["left_lower"]}')
        elif param["corner_count"] == 3:
            param["right_lower"] = (x,y)
            print(f'Right_Lower Pixel = {param["right_lower"]}')
        
        param["corner_count"] += 1
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle, state)
box_drawn = False
while(1):
    cv2.imshow('image', output)
    if box_drawn is False:
        # draw the box and the center point
        if state["corner_count"] >=4:
            cv2.line(output, state["left_upper"] , state["right_upper"], (255, 0, 0), 5)
            cv2.line(output, state["right_upper"] , state["right_lower"], (255, 0, 0), 5)
            cv2.line(output, state["right_lower"] , state["left_lower"], (255, 0, 0), 5)
            cv2.line(output, state["left_lower"] , state["left_upper"], (255, 0, 0), 5)
            cv2.imshow('image',output)
            x_center = (state["left_upper"][0] + state["right_upper"][0]) // 2
            y_center = (state["left_upper"][1] + state["left_lower"][1]) // 2
            center = (x_center, y_center)
            print(f'Center = {center}')
            true_center = (center[0] * 10, center[1] * 10)
            cv2.circle(output, center, 10, (200,40,200), -1)
            print(f'True Center = {true_center}')
            box_drawn = True

    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()