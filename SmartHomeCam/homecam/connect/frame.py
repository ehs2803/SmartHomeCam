import copy
import os
import time


import cv2
import struct
import pickle
import datetime
from django.core.files.base import ContentFile

from SmartHomeCam.settings.base import BASE_DIR
from SmartHomeCam.storages import FileUpload, s3_client
from homecam.mode.detect_person_animal import YoloDetect
from homecam.mode.fire_detection import FireDetector
from homecam.mode.recognition_face import unknownFaceDetector
from homecam.mode.safeMode import SafeMode
from homecam.models import CapturePicture, RecordingVideo


class Frame:
    def __init__(self, client_socket, username, camid, policy):
        self.username = username
        self.camid = camid
        self.client_socket = client_socket
        self.data_buffer = b""
        self.data_size = struct.calcsize("L")
        self.imageFrame = None
        self.imagesave = None
        self.check = False

        self.recording_video_check = False
        self.out = None
        self.rvfilename = None

        self.check_current_recording = False

        # policy
        self.check_detect_person = policy['po_person']
        self.check_recognition_face = policy['po_unknown']
        self.check_detect_fire = policy['po_fire']
        self.check_detect_animal = policy['po_animal']
        self.check_detect_no_person = policy['po_safe_noperson']
        self.check_detect_no_action = policy['po_safe_noaction']
        self.check_detect_no_person_day = policy['po_safe_no_person_day']
        self.check_on_safemode = False

        # detector
        self.YoloDetector = YoloDetect()
        self.RecognitionFace = unknownFaceDetector(username)
        self.FireDetector = FireDetector(username)
        self.SafeMode = SafeMode(username)

    def detect_live(self):
        while True:
            if self.check == True:
                return
            # 설정한 데이터의 크기보다 버퍼에 저장된 데이터의 크기가 작은 경우
            while len(self.data_buffer) < self.data_size:
                # 데이터 수신
                try:
                    self.data_buffer += self.client_socket.recv(4096)
                except:
                    return
                '''
                temp = self.client_socket.recv(4096)
                if temp=='disconnect':
                    print(1)
                    self.disconnet()
                self.data_buffer += temp
                '''

            self.client_socket.sendall("10".encode())
            # 버퍼의 저장된 데이터 분할
            packed_data_size = self.data_buffer[:self.data_size]
            self.data_buffer = self.data_buffer[self.data_size:]
            # struct.unpack : 변환된 바이트 객체를 원래의 데이터로 변환
            frame_size = struct.unpack(">Q", packed_data_size)[0]
            # 프레임 데이터의 크기보다 버퍼에 저장된 데이터의 크기가 작은 경우
            while len(self.data_buffer) < frame_size:
                # 데이터 수신
                try:
                    self.data_buffer += self.client_socket.recv(4096)
                except:
                    return
            # 프레임 데이터 분할
            frame_data = self.data_buffer[:frame_size]
            self.data_buffer = self.data_buffer[frame_size:]
            # print("수신 프레임 크기 : {} bytes".format(frame_size))
            # loads : 직렬화된 데이터를 역직렬화
            # 역직렬화(de-serialization) : 직렬화된 파일이나 바이트 객체를 원래의 데이터로 복원하는 것
            frame = pickle.loads(frame_data)

            # imdecode : 이미지(프레임) 디코딩
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # 사람/반려동물 탐지
            if self.check_detect_person or self.check_detect_animal:
                tframe = self.YoloDetector.Detect_person_animal_YOLO(frame=frame, size=320, score_threshold=0.4, nms_threshold=0.4,
                                                                   username=self.username, camid=self.camid,
                                                  check_detect_person=self.check_detect_person,
                                                  check_detect_animal=self.check_detect_animal)
            # 외부인탐지
            if self.check_recognition_face:
                tframe = self.RecognitionFace.recognition_face(frame, self.camid)

            # 화재탐지
            if self.check_detect_fire:
                fframe = self.FireDetector.detect_fire(frame, 320, 0.4, 0.4, self.camid)

            # 일정시간 사람 미감지, 사람 행동 미감지 탐지
            if self.check_detect_no_action or self.check_detect_no_person:
                sframe = self.SafeMode.run_safe_mode(frame, self.camid, 320,
                                                     self.check_detect_no_person,
                                                     self.check_detect_no_action,
                                                     self.check_detect_no_person_day)
            # 동영상 녹화
            if self.recording_video_check==True:
                self.out.write(frame)

            ret, frame = cv2.imencode('.jpg', frame)
            self.imagesave = frame
            self.imageFrame = frame.tobytes()

    # 이미지 캡처
    def capture_picture(self, puser):
        user = puser
        cp = CapturePicture()
        cp.uid = user
        file = ContentFile(self.imagesave)

        file_s3 = copy.deepcopy(file)
        image_url = FileUpload(s3_client).upload(file_s3, 'capture/')

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        file.name = timestamp + '.jpg'
        cp.image = file
        cp.image_s3=image_url
        cp.time = timestamp
        cp.camid = self.camid
        cp.save()

    # 동영상 녹화
    def recording_video(self, puser):
        if self.recording_video_check == False:
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            self.rvfilename = 'media/tempVideoRepository/'+timestamp + '.mp4'
            self.out = cv2.VideoWriter(self.rvfilename, cv2.VideoWriter_fourcc(*'mp4v'), 20, (640, 480)) # *'H264'
            self.recording_video_check = True
            self.check_current_recording=True
        else:
            self.recording_video_check = False
            self.out.release()
            self.out = None
            self.check_current_recording=False
            saved_filename = self.rvfilename
            self.rvfilename = None
            user = puser
            rv = RecordingVideo()
            rv.uid = user
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            rv.time = timestamp

            savedFile = str(BASE_DIR)+"/"+saved_filename
            newFile = str(BASE_DIR)+"/"+saved_filename+".mp4"
            print(savedFile+" "+newFile)

            # 코덱 변경
            try:
                os.system(f"ffmpeg -i {savedFile} -vcodec libx264 {newFile}")
            except Exception as e:
                print(e)

            fp = open(saved_filename+".mp4", 'rb')
            vf = fp.read()

            file = ContentFile(vf)

            file_s3 = copy.deepcopy(file)
            video_url = FileUpload(s3_client).upload_video(file_s3, 'recording/')

            file.name = timestamp + '.mp4'
            rv.video = file
            rv.video_s3=video_url
            rv.camid = self.camid
            rv.save()

    # 동영상 프레임 얻기
    def get_frame(self):
        return self.imageFrame

    # 연결 해제
    def disconnet(self):
        self.check = True
        self.client_socket.close()
