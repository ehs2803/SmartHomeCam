import datetime
import os
import time

import cv2
import dlib
import numpy as np
from django.contrib.auth.models import User

from django.conf import settings
from django.core.files.base import ContentFile

from account.models import AuthUser
from homecam.sns.Email import EmailSender
from homecam.sns.SMSMessage import SmsSender
from mypage.models import Family

from homecam.models import RecognitionFace, Alarm


class unknownFaceDetector(EmailSender, SmsSender):
    def __init__(self, username):
        # shape predictor와 사용하는 recognition_model
        self.pose_predictor_5_point = dlib.shape_predictor("homecam/data/shape_predictor_5_face_landmarks.dat")
        self.face_encoder = dlib.face_recognition_model_v1("homecam/data/dlib_face_recognition_resnet_model_v1.dat")

        # threshold보다 큰 유클리디언 거리는 동일 인물로 판단하지 않음.
        self.threshold = 0.5

        # 얼굴검출 dlib hog face detector 사용.
        self.detector = dlib.get_frontal_face_detector()

        self.username = username

        # 사용자 계정에 등록된 가족 멤버 얼굴 사진들
        self.faces=[]
        self.images_list=[]
        self.images_encoding = []
        self.images_label = []
        self.updateFamilyMemberFaces()

        # 탐지 시간
        self.recognition_face_time=time.time()

        # 알림 연락처 정보
        self.PhoneNumberList=[]
        self.EmailAddressList=[]

    def updateFamilyMemberFaces(self):
        user = User.objects.get(username=self.username)
        family_members = Family.objects.filter(uid=user.id)
        for family in family_members:
            image1 = family.image1
            image2 = family.image2
            image3 = family.image3
            if image1!='':
                print(settings.MEDIA_ROOT+'/'+str(image1))
                image1_read = cv2.imread(settings.MEDIA_ROOT+'/'+str(image1), cv2.IMREAD_COLOR)
                self.faces.append(image1_read)
                faces, known_image_encoding = self.face_encodings(image1_read)
                for i, face in enumerate(faces):
                    img_face = image1_read[face.top():face.bottom(), face.left():face.right(), :]
                    self.images_list.append(img_face)
                    self.images_encoding.append(known_image_encoding[i])
                    self.images_label.append(family.name)
            if image2!='':
                image2_read = cv2.imread(settings.MEDIA_ROOT+'/'+str(image2), cv2.IMREAD_COLOR)
                self.faces.append(image2_read)
                faces, known_image_encoding = self.face_encodings(image2_read)
                for i, face in enumerate(faces):
                    img_face = image2_read[face.top():face.bottom(), face.left():face.right(), :]
                    self.images_list.append(img_face)
                    self.images_encoding.append(known_image_encoding[i])
                    self.images_label.append(family.name)
            if image3!='':
                image3_read = cv2.imread(settings.MEDIA_ROOT+'/'+str(image3), cv2.IMREAD_COLOR)
                self.faces.append(image3_read)
                faces, known_image_encoding = self.face_encodings(image3_read)
                for i, face in enumerate(faces):
                    img_face = image3_read[face.top():face.bottom(), face.left():face.right(), :]
                    self.images_list.append(img_face)
                    self.images_encoding.append(known_image_encoding[i])
                    self.images_label.append(family.name)
        print(len(self.images_encoding))

    # face_encodings은 128차원의 ndarray 데이터들을 사람 얼굴에 따라 리스트 자료형과 얼굴 위치좌표를 반환
    def face_encodings(self, face_image, number_of_times_to_upsample=1, num_jitters=2):
        """Returns the 128D descriptor for each face in the image"""
        # Detect faces:
        # hog 기반의 dlib face detector. gray 변환된 영상을 사용.
        gray = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)
        face_locations = self.detector(gray, number_of_times_to_upsample)
        # Detected landmarks:
        raw_landmarks = [self.pose_predictor_5_point(face_image, face_location) for face_location in face_locations]
        # Calculate the face encoding for every detected face using the detected landmarks for each one:
        return face_locations, [
            np.array(self.face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters))
            for raw_landmark_set in raw_landmarks]

    # unknown encoding을 known_encoding list에 비교해 유클리디어 거리를 계산해 이름과 반환하고, 거리는 오름차순 정렬해 반환한다.
    def compare_faces_ordered(self, dbfaces, encodings, face_names, encoding_to_check):
        """Returns the ordered distances and names when comparing a list of face encodings against a candidate to check"""
        distances = list(np.linalg.norm(encodings - encoding_to_check, axis=1))
        return zip(*sorted(zip(distances, dbfaces, face_names)))

    def recognition_face(self, img, camid):
        if time.time()-self.recognition_face_time<10:
            return;
        copy_image = img.copy()
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        unknown_image_rects, unknown_image_encoding = self.face_encodings(rgb_image)
        for i, det in enumerate(unknown_image_rects):
            cv2.rectangle(img, (det.left(), det.top()), (det.right(), det.bottom()), (0,255,0), 3)
            computed_distances_ordered, faces, ordered_names = self.compare_faces_ordered(self.images_list,
                                                                                     self.images_encoding,
                                                                                     self.images_label,
                                                                                    unknown_image_encoding[i])  # 비교
            if computed_distances_ordered[0] < self.threshold:
                print('detect: ', computed_distances_ordered[0])
            else:
                rfmodel = RecognitionFace()

                ret1, frame1 = cv2.imencode('.jpg', img)
                ret2, frame2 = cv2.imencode('.jpg', copy_image)
                user = AuthUser.objects.get(username=self.username)
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                rfmodel.uid = user
                file1 = ContentFile(frame1)
                file2 = ContentFile(frame2)
                file1.name = timestamp + '_1' + '.jpg'
                file2.name = timestamp + '_2' + '.jpg'
                rfmodel.image1 = file1
                rfmodel.image2 = file2
                rfmodel.time = timestamp
                rfmodel.camid = camid
                rfmodel.save()

                alarm = Alarm()
                alarm.uid = user
                alarm.camid = camid
                alarm.time = timestamp
                alarm.confirm = 0
                alarm.type = 'UNKNOWN'
                alarm.did = rfmodel.id
                alarm.save()

                self.updateContactList(self.username)
                filepath1 = settings.MEDIA_ROOT + '/' + str(rfmodel.image1)
                filepath2 = settings.MEDIA_ROOT + '/' + str(rfmodel.image2)
                self.sendDetectunknownFaceEmail(filepath1, filepath2)
                self.sendDetectUnknownSMS()

                self.recognition_face_time=time.time()
                print('unknown detect: ', computed_distances_ordered[0])
                break
        return img

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

    def sendDetectunknownFaceEmail(self, file1, file2):
        receivers = ''
        for email in self.EmailAddressList:
            receivers = receivers+email
            receivers = receivers+','
        receivers = receivers[:-1]
        super().makeContent(receiver=receivers, subject="[SmartHomecam] 확인되지 않은 사람 탐지",
                            sendimg1=file1, sendimg2=file2)
        super().sendEmail()

    def sendDetectUnknownSMS(self):
        for phone in self.PhoneNumberList:
            receiver = '82'+phone
            receiver = receiver.replace('-', "")
            super().sendSMS(receiver, '[SmartHomeCam] 외부인 탐지\n웹사이트에 들어가서 확인해보세요.')