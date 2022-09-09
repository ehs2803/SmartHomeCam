import datetime

import cv2
import numpy as np
import time

from django.contrib.auth.models import User
from django.contrib.messages.storage import session
from django.core.files.base import ContentFile

from account.models import AuthUser

import django.contrib.sessions

from homecam.models import DetectPerson, DetectAnimal, Alarm
from homecam.sns.Email import EmailSender
from homecam.sns.SMSMessage import SmsSender
from mypage.models import Family
from django.conf import settings

class YoloDetect(EmailSender, SmsSender):
    def __init__(self):
        self.size_list = [320, 416, 608]
        # person(0)  cat(15) dog(16)
        self.classes = ["person", "bicycle", "car", "motorcycle",
           "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
           "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
           "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
           "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
           "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
           "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife",
           "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
           "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table",
           "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
           "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
           "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        # YOLO 네트워크 불러오기
        self.net = cv2.dnn.readNet("homecam/data/yolov4-tiny.weights", "homecam/data/yolov4-tiny.cfg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        # 클래스의 갯수만큼 랜덤 RGB 배열을 생성
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.detect_person_time = time.time()
        self.detect_animal_time = time.time()

        self.PhoneNumberList = []
        self.EmailAddressList = []

    def Detect_person_animal_YOLO(self, frame, size, score_threshold, nms_threshold, username, camid,
                                  check_detect_person,check_detect_animal):
        copy_frame = frame.copy()
        # 이미지의 높이, 너비, 채널 받아오기
        height, width, channels = frame.shape

        # 네트워크에 넣기 위한 전처리
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (size, size), (0, 0, 0), True, crop=False)

        # 전처리된 blob 네트워크에 입력
        self.net.setInput(blob)

        # 결과 받아오기
        outs = self.net.forward(self.output_layers)

        # 각각의 데이터를 저장할 빈 리스트
        class_ids = []
        confidences = []
        boxes = []

        check_person = False
        check_animal = False
        # printq
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if not (class_id == 0 or class_id == 15 or class_id == 16):
                    continue
                if check_detect_person and class_id==0:
                    check_person=True
                if check_detect_animal and (class_id==15 or class_id==16):
                    check_animal=True

                if confidence > 0.1:
                    # 탐지된 객체의 너비, 높이 및 중앙 좌표값 찾기
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # 객체의 사각형 테두리 중 좌상단 좌표값 찾기
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Non Maximum Suppression (겹쳐있는 박스 중 confidence 가 가장 높은 박스를 선택)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=score_threshold, nms_threshold=nms_threshold)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                class_name = self.classes[class_ids[i]]
                label = f"{class_name} {confidences[i]:.2f}"
                color = self.colors[class_ids[i]]

                # 사각형 테두리 그리기 및 텍스트 쓰기
                if (class_name=='person' and check_detect_person) or ((class_name=='cat' or class_name=='dog') and check_detect_animal):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.rectangle(frame, (x - 1, y), (x + len(class_name) * 13 + 65, y - 25), color, -1)
                    cv2.putText(frame, label, (x, y - 8), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 2)

        if check_detect_person and check_person:
            # 10초 후에
            if time.time() - self.detect_person_time > 10:
                print(1)
                ret1, frame1 = cv2.imencode('.jpg', frame)
                ret2, frame2 = cv2.imencode('.jpg', copy_frame)

                dp = DetectPerson()

                user = AuthUser.objects.get(username=username)
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                dp.uid = user
                file1 = ContentFile(frame1)
                file2 = ContentFile(frame2)
                file1.name = timestamp+'_1' + '.jpg'
                file2.name = timestamp+'_2' + '.jpg'
                dp.image1 = file1
                dp.image2 = file2
                dp.time = timestamp
                dp.camid = camid
                dp.save()

                alarm = Alarm()
                alarm.uid=user
                alarm.camid=camid
                alarm.time=timestamp
                alarm.confirm=0
                alarm.type='PERSON'
                alarm.did=dp.id
                alarm.save()

                self.updateContactList(username)
                #filepath1 = settings.MEDIA_ROOT+'/images/detectPerson/AuthUser object (3)/2022-05-19_082716_1.jpg'#'/media/' + str(dp.image1)
                #filepath2 = settings.MEDIA_ROOT+'/images/detectPerson/AuthUser object (3)/2022-05-19_082716_1.jpg'#'/media/' + str(dp.image2)
                filepath1 = settings.MEDIA_ROOT+'/'+str(dp.image1)#'/media/' + str(dp.image1)
                filepath2 = settings.MEDIA_ROOT+'/'+str(dp.image2)#'/media/' + str(dp.image2)
                #print(filepath1)
                self.sendDetectPersonEmail(filepath1, filepath2)
                self.sendDetectPersonEmail()
                self.detect_person_time = time.time()

        if check_detect_animal and check_animal:
            if time.time() - self.detect_animal_time >10:
                print('10sec after')
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                check_record_15=False
                check_record_16=False
                for index, id in enumerate(class_ids):
                    if confidences[index]>0.6 and (id==15 or id==16):
                        print(confidences[index], id)
                        if id==15:
                            if check_record_15==False:
                                check_record_15=True
                            else:
                                continue
                        if id==16:
                            if check_record_16==False:
                                check_record_16=True
                            else:
                                continue
                        ap = DetectAnimal()
                        user = AuthUser.objects.get(username=username)

                        ap.uid = user
                        ap.time= timestamp

                        ap.species = id

                        midWidth = width/2
                        midHeight = height/2
                        x,y,w,h = boxes[index]

                        cx = x+(w/2)
                        cy = y+(h/2)

                        location = 0
                        if cx<=midHeight and cy<=midWidth:
                            location=2
                        elif cx<=midHeight and cy>=midWidth:
                            location=1
                        elif cx>=midHeight and cy>=midWidth:
                            location=4
                        else:
                            location=3

                        ap.location = location
                        ap.camid = camid
                        ap.save()
                        self.detect_animal_time = time.time()


        return frame

    def updateContactList(self, username):
        user = User.objects.get(username=username)
        family_members = Family.objects.filter(uid=user.id)
        self.PhoneNumberList.clear()
        self.EmailAddressList.clear()
        for family in family_members:
            self.EmailAddressList.append(family.email)
            self.PhoneNumberList.append(family.tel)
        print(self.EmailAddressList)
        print(self.PhoneNumberList)

    def sendDetectPersonEmail(self, file1, file2):
        receivers = ''
        for email in self.EmailAddressList:
            receivers = receivers+email
            receivers = receivers+','
        receivers = receivers[:-1]
        super().makeContent(receiver=receivers, subject="[SmartHomecam] 사탐 탐지 알림",
                            sendimg1=file1, sendimg2=file2)
        super().sendEmail()

    def sendDetectPersonSMS(self):
        for phone in self.PhoneNumberList:
            receiver = '82'+phone
            receiver = receiver.replace('-', "")
            super().sendSMS(receiver, '[SmartHomeCam] 사람 탐지\n웹사이트에 들어가서 확인해보세요.')



