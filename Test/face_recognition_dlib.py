import cv2
import dlib
import numpy as np
import pickle
from matplotlib import pyplot as plt
import time
from imutils import face_utils

# threshold보다 큰 유클리디언 거리는 동일 인물로 판단하지 않음.
threshold = 0.6

model_path = './data'
pose_predictor_5_point = dlib.shape_predictor(model_path + "shape_predictor_5_face_landmarks.dat")
face_encoder = dlib.shape_predictor(model_path + "dlib_face_recognition_resnet_model_v1.dat")

net = cv2.dnn.readNetFromTensorflow("opencv_face_detector_uint8.pb", "opencv_face_detector.pbtxt")  # 99.912%/97.502%/79.021%
cam = cv2.VideoCapture(0)
color_green = (0,255,0)
line_width = 3

# face_encodings은 128차원의 ndarray 데이터들을 사람 얼굴에 따라 리스트 자료형과 얼굴 위치좌표를 반환
def face_encodings(face_image, number_of_times_to_upsample=1, num_jitters=2):
    """Returns the 128D descriptor for each face in the image"""
    # Detect faces:
    # hog 기반의 dlib face detector. gray 변환된 영상을 사용.
    gray = cv.cvtColor(face_image, cv.COLOR_RGB2GRAY)
    face_locations = detector(gray, number_of_times_to_upsample)
    # Detected landmarks:
    raw_landmarks = [pose_predictor_5_point(face_image, face_location) for face_location in face_locations]
    # Calculate the face encoding for every detected face using the detected landmarks for each one:
    return face_locations, [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters))
                            for raw_landmark_set in raw_landmarks]

# unknown encoding을 known_encoding list에 비교해 유클리디어 거리를 계산해 이름과 반환하고, 거리는 오름차순 정렬해 반환한다.
def compare_faces_ordered(dbfaces, encodings, face_names, encoding_to_check):
    """Returns the ordered distances and names when comparing a list of face encodings against a candidate to check"""
    distances = list(np.linalg.norm(encodings - encoding_to_check, axis=1))
    return zip(*sorted(zip(distances,dbfaces, face_names)))


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







