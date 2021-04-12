import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# img = cv2.imread("C:/Users/eliwss0/Documents/misc-projects/resistor-calculator/python_opencv/1.jpg")

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    brwnLower = (10,45,90)
    brwnUpper = (25,110,240)
    thresh = cv2.inRange(hsv, brwnLower, brwnUpper)

    orange_lower = np.array([5, 135, 0], np.uint8) #TODO
    orange_upper = np.array([15, 255, 255], np.uint8)
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)

    black_lower = np.array([5, 0, 0], np.uint8) #?
    black_upper = np.array([30, 105, 55], np.uint8)
    black_mask = cv2.inRange(hsv, black_lower, black_upper)

    yellow_lower = np.array([22, 100, 125], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    red_lower = np.array([0, 100, 5], np.uint8)
    red_upper = np.array([5, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    brown_lower = np.array([5, 70, 145], np.uint8)
    brown_upper = np.array([10, 255, 220], np.uint8)
    brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)

    green_lower = np.array([60, 60, 60], np.uint8)
    green_upper = np.array([90, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    blue_lower = np.array([90, 150, 5], np.uint8)
    blue_upper = np.array([105, 255, 175], np.uint8)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

    violet_lower = np.array([150, 130, 75], np.uint8) #TODO
    violet_upper = np.array([179, 255, 255], np.uint8)
    violet_mask = cv2.inRange(hsv, violet_lower, violet_upper)

    gray_lower = np.array([30, 0, 150], np.uint8)
    gray_upper = np.array([179, 110, 215], np.uint8)
    gray_mask = cv2.inRange(hsv, gray_lower, gray_upper)

    white_lower = np.array([0, 0, 205], np.uint8)
    white_upper = np.array([179, 20, 255], np.uint8)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14,14))
    clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # get external contours
    contours = cv2.findContours(clean, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(frame.shape[:2],dtype=np.uint8)

    result1 = frame.copy()
    result2 = frame.copy()
    resistor = mask.copy()
    resistor2 = resistor.copy()

    for c in contours:
        cv2.drawContours(result1,[c],0,(0,0,0),2)
        rot_rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rot_rect)
        box = np.int0(box)
        if (rot_rect[1][0]>3*rot_rect[1][1] or rot_rect[1][1]>3*rot_rect[1][0]) and rot_rect[1][0]*2+rot_rect[1][1]*2 > 200:
            cv2.drawContours(result2,[box],0,(0,0,0),2)
            roi = cv2.boundingRect(box)
            cv2.fillPoly(mask,[box],[255,255,255])
            resistor = cv2.bitwise_and(frame,frame,mask=mask)
            #TODO draw rectangle around colored bands

            grayBands = cv2.cvtColor(resistor, cv2.COLOR_BGR2GRAY)
            contourBands = cv2.findContours(grayBands, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            contourBands = contourBands[0] if len(contourBands) == 2 else contourBands[1]

            for c2 in contourBands:
                cv2.drawContours(resistor,[c2],0,(0,0,0),2)
                rot_rectBands = cv2.minAreaRect(c2)
                boxBands = cv2.boxPoints(rot_rectBands)
                boxBands = np.int0(boxBands)
                cv2.drawContours(resistor2,[boxBands],0,(0,0,0),2)
                roi = cv2.boundingRect(boxBands)
                cv2.fillPoly(mask,[boxBands],[255,0,0])
                colorMask1 = cv2.bitwise_or(red_mask,orange_mask) #TODO bitwise or for all colors
                resistor2 = cv2.bitwise_and(resistor,resistor,mask=colorMask1)

    # display result
    cv2.imshow("thresh", thresh)
    cv2.imshow("clean", clean)
    cv2.imshow("result1", result1)
    cv2.imshow("result2", result2)
    cv2.imshow("resistor", resistor)
    cv2.imshow("resistor-colors", resistor2)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
cv2.destroyAllWindows()

# def morphology():
#     # apply morphology
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
#     clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
#     clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#     # get external contours
#     contours = cv2.findContours(clean, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#     contours = contours[0] if len(contours) == 2 else contours[1]