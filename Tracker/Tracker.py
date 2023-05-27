import cv2
from adafruit_servokit import ServoKit

def track(*args):
     x, res_x, min_ang, max_ang, ang_range, k = args
     ang = min_ang + max_ang - (x / (res_x / ang_range)) # find angle from detection
     if ang > max_ang:
         ang = max_ang
     if ang < min_ang:
         ang = min_ang
     k.servo[0].angle = int(ang) # change angle of the servo

def main():
     cap = cv2.VideoCapture(0) # capture video
     min_ang, max_ang = 10,170
     ang_range = max_ang - min_ang # servo range
     res_x, res_y = 320, 240
     cap.set(3, res_x) # set horizontal resolution
     cap.set(4, res_y) # set vertical resolution
     # setup motor
     kit = ServoKit(channels=16)
     # threshold = amount of false positives, history = amount of past frames
     detector = cv2.createBackgroundSubtractorMOG2(history=8,
varThreshold=6)

     while(True):
         _, frame = cap.read() # read from camera
         roi = frame
         mask = detector.apply(roi) # apply mask for easier detections
         contours, _ =cv2.findContours(mask, cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE) # find all contours
         detections = [] # list for detections
         # empty variables
         max_idx,max_area,idx = 0,0,0
         for cnt in contours:
             #calc area and ignore small objects
             area = cv2.contourArea(cnt)
             if area > 300:
                 x,y,w,h = cv2.boundingRect(cnt)
                 detections.append([x,y,w,h]) # add to vector
                 area = w*h
                 if area > max_area: # find largest object
                     max_area, max_idx = area, idx # save index and area
                 idx = idx + 1
         if (len(detections) > 0):
             x,y,w,h = detections[max_idx]
              # draw rectangle around object
             cv2.rectangle(roi, (x,y), (x+w, y+h), (0, 255, 0), 3)
             track(x,res_x,min_ang,max_ang,ang_range,kit)
         cv2.imshow('frame', frame) # show footage
         if cv2.waitKey(1) & 0xFF == ord('q'):
             break
     cap.release()
     cap.destroyAllWindows()

if __name__ == "__main__":
     main()

