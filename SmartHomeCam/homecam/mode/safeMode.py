import datetime
import time
import cv2
import numpy as np
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from SmartHomeCam import settings
from account.models import AuthUser
from homecam.sns.Email import EmailSender
from homecam.sns.SMSMessage import SmsSender
from homecam.models import SafeModeNodetect, SafeModeNoaction, Alarm
from mypage.models import Family


class SafeMode(EmailSender, SmsSender):
    def __init__(self, username):
        self.username = username

        self.classes = ["person"]
        # YOLO 네트워크 불러오기
        self.net = cv2.dnn.readNet("homecam/data/yolov4-tiny.weights",
                                   "homecam/data/yolov4-tiny.cfg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        # 클래스의 갯수만큼 랜덤 RGB 배열을 생성
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

        # 시간 체크
        self.safe_mode_time = time.time()
        self.detect_time = time.time()
        self.time_noDetect = 86400
        self.time_noAction = 30
        self.detect_action_time = None
        self.detect_location = [-20,-20]

        # 알림 연락처 정보
        self.PhoneNumberList=[]
        self.EmailAddressList=[]

    def init_noDetectTime(self):
        self.safe_mode_time=time.time()
        self.detect_action_time = None
        self.detect_location=[0,0]

    def run_safe_mode(self, frame, camid, size):
        if time.time()-self.safe_mode_time>self.time_noDetect:
            smnd = SafeModeNodetect()
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            user = AuthUser.objects.get(username=self.username)

            smnd.uid = user
            smnd.time = timestamp
            smnd.period = self.time_noDetect
            smnd.camid = camid
            smnd.save()

            alarm = Alarm()
            alarm.uid = user
            alarm.camid = camid
            alarm.time = timestamp
            alarm.confirm = 0
            alarm.type = 'NOPERSON'
            alarm.did = smnd.id
            alarm.save()

            self.safe_mode_time=time.time()

            self.updateContactList(self.username)
            self.sendSafeModeEmail_no_detect(self.username, camid, self.time_noDetect)
            self.sendDetectNoDetectPersonSMS()
            print('save')
        if time.time()-self.detect_time<10:
            return
        self.detect_time = time.time()

        copy_frame = frame.copy()
        # 이미지의 높이, 너비, 채널 받아오기
        height, width, channels = frame.shape

        # 네트워크에 넣기 위한 전처리
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (size, size), (0, 0, 0), True, crop=False)

        # 전처리된 blob 네트워크에 입력
        self.net.setInput(blob)

        # 결과 받아오기
        outs = self.net.forward(self.output_layers)

        boxes = []
        confidences = []
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
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # 객체의 사각형 테두리 중 좌상단 좌표값 찾기
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # Non Maximum Suppression (겹쳐있는 박스 중 confidence 가 가장 높은 박스를 선택)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.4, nms_threshold=0.4)

        if check_person==True:
            self.safe_mode_time=time.time()
        else:
            self.detect_action_time = None
            self.detect_location = [-20,-20]
            return

        #if len(boxes)>1:
        #    print('1more detect',len(boxes))
        #    return
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                cx = x + (w / 2)
                cy = y + (h / 2)
                if self.detect_action_time==None:
                    self.detect_action_time=time.time()
                ox, oy = self.detect_location
                self.detect_location = [cx, cy]
                if abs(cx-ox)>10 or abs(cy-oy)>10:
                    self.detect_action_time = time.time()
                    print('행동미감지 초기화')
                print('행동미감지 진행중')
                if time.time()-self.detect_action_time>self.time_noAction:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)

                    smna = SafeModeNoaction()

                    ret1, frame1 = cv2.imencode('.jpg', frame)
                    ret2, frame2 = cv2.imencode('.jpg', copy_frame)
                    user = AuthUser.objects.get(username=self.username)
                    ts = time.time()
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                    smna.uid = user
                    file1 = ContentFile(frame1)
                    file2 = ContentFile(frame2)
                    file1.name = timestamp + '_1' + '.jpg'
                    file2.name = timestamp + '_2' + '.jpg'
                    smna.image1 = file1
                    smna.image2 = file2
                    smna.time = timestamp
                    smna.camid = camid
                    smna.period = self.time_noAction
                    smna.save()

                    alarm = Alarm()
                    alarm.uid = user
                    alarm.camid = camid
                    alarm.time = timestamp
                    alarm.confirm = 0
                    alarm.type = 'NOACTION'
                    alarm.did = smna.id
                    alarm.save()

                    self.updateContactList(self.username)
                    filepath1 = settings.MEDIA_ROOT + '/' + str(smna.image1)
                    filepath2 = settings.MEDIA_ROOT + '/' + str(smna.image2)
                    self.sendSafeModeEmail_no_action(filepath1, filepath2)
                    self.sendDetectNoActionSMS()

                    self.detect_action_time=None
                    print('행동미감지')


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

    def sendSafeModeEmail_no_detect(self, username, camid, period):
        receivers = ''
        for email in self.EmailAddressList:
            receivers = receivers+email
            receivers = receivers+','
        receivers = receivers[:-1]
        super().makeContent_noimage(receiver=receivers, subject="[SmartHomecam] 안심모드 알림 - 사람활동 미감지",
                                    username=username, camid=camid, period=period)
        super().sendEmail()

    def sendSafeModeEmail_no_action(self, file1, file2):
        receivers = ''
        for email in self.EmailAddressList:
            receivers = receivers+email
            receivers = receivers+','
        receivers = receivers[:-1]
        super().makeContent(receiver=receivers, subject="[SmartHomecam] 안심모드 사람 행동 미감지",
                            sendimg1=file1, sendimg2=file2)
        super().sendEmail()

    def sendDetectNoDetectPersonSMS(self):
        day = self.time_noDetect/86400
        for phone in self.PhoneNumberList:
            receiver = '82'+phone
            receiver = receiver.replace('-', "")
            super().sendSMS(receiver, '[SmartHomeCam] '+str(day)+'일동안 사람인식 않됨\n웹사이트에 들어가서 확인해보세요.')

    def sendDetectNoActionSMS(self):
        hour = self.time_noAction/3600
        for phone in self.PhoneNumberList:
            receiver = '82'+phone
            receiver = receiver.replace('-', "")
            super().sendSMS(receiver, '[SmartHomeCam] '+str(hour)+'시간 사람 행동 인식 않됨\n웹사이트에 들어가서 확인해보세요.')