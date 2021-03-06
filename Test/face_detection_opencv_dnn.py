
# Import required packages:
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

# 1) Caffe Model의 경우
#net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000_fp16.caffemodel")    # 99.922%/97.495%/79.345%
# Tensorflow Model의 경우
net = cv2.dnn.readNetFromTensorflow("opencv_face_detector_uint8.pb", "opencv_face_detector.pbtxt")  # 99.912%/97.502%/79.021%
cam = cv2.VideoCapture(0)
color_green = (0,255,0)
line_width = 3
while True:
    ret_val, image = cam.read()
    #image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104., 117., 123.], False, False)
    net.setInput(blob)
    detections = net.forward()  # 네트워트를 가동한다. 입력=> 네트워크 => 출력
    detected_faces = 0
    for i in range(0, detections.shape[2]):
        # Get the confidence (probability) of the current detection:
        confidence = detections[0, 0, i, 2]  # i번째 검출 영역의 confidence

        # Only consider detections if confidence is greater than a fixed minimum confidence:
        if confidence > 0.7:
            # Increment the number of detected faces:
            detected_faces += 1
            # Get the coordinates of the current detection:
            # print(detections[0, 0, i, 3:7])     # 정규화된 검출된 위치
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the detection and the confidence:
            text = "{:.1f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 2)
            cv2.putText(image, text, (startX, y + 4), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, lineType=cv2.LINE_AA,
                        color=(0, 0, 255), thickness=3)
            cv2.putText(image, text, (startX, y + 4), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, lineType=cv2.LINE_AA,
                        color=(255, 255, 255), thickness=1)
    cv2.imshow('my webcam', image)
    if cv2.waitKey(1) == 27:
        break  # esc to quit
cv2.destroyAllWindows()


