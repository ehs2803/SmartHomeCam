import time
import cv2
import numpy as np
from django.contrib.auth.models import User

from homecam.algorithm.Email import EmailSender
from homecam.algorithm.SMSMessage import SmsSender
from mypage.models import Family


class SafeMode(EmailSender, SmsSender):
    def __init__(self, username):
        self.username = username

        self.classes = ["person"]
        # YOLO 네트워크 불러오기
        self.net = cv2.dnn.readNet("homecam/algorithm/data/yolov4-tiny.weights",
                                   "homecam/algorithm/data/yolov4-tiny.cfg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        # 클래스의 갯수만큼 랜덤 RGB 배열을 생성
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        # 시간 체크
        self.safe_mode_time = time.time()
        self.detect_time = time.time()

        # 알림 연락처 정보
        self.PhoneNumberList=[]
        self.EmailAddressList=[]

    def run_safe_mode(self, frame, camid, size):
        if time.time()-self.safe_mode_time>86400:
            pass
        if time.time()-self.detect_time<10:
            return

        copy_frame = frame.copy()
        # 이미지의 높이, 너비, 채널 받아오기
        height, width, channels = frame.shape

        # 네트워크에 넣기 위한 전처리
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (size, size), (0, 0, 0), True, crop=False)

        # 전처리된 blob 네트워크에 입력
        self.net.setInput(blob)

        # 결과 받아오기
        outs = self.net.forward(self.output_layers)

        check_person = False
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if not (class_id == 0):
                    continue
                if class_id==0 and confidence>0.5:
                    check_person=True

        if check_person==True:
            self.safe_mode_time=time.time()

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

    def sendSafeModeEmail(self, file1, file2):
        receivers = ''
        for email in self.EmailAddressList:
            receivers = receivers+email
            receivers = receivers+','
        receivers = receivers[:-1]
        super().makeContent(receiver=receivers, subject="[SmartHomecam] 안심모드 알림",
                            sendimg1=file1, sendimg2=file2)
        super().sendEmail()