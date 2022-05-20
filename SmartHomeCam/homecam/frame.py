import time

from PIL import Image
from django.core.files import File
import cv2
import struct
import pickle
import datetime
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

from account.models import AuthUser
from homecam.algorithm.detect_person_animal import YoloDetect
from homecam.models import CapturePicture, RecordingVideo


class Frame:
    def __init__(self, client_socket, username, camid):
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

        self.check_detect_person = False
        self.check_recognition_face = False
        self.check_detect_fire = False
        self.check_detect_animal = False

        self.check_current_recording = False

        self.YoloDetector = YoloDetect()

    def detect_live(self):
        while True:
            if self.check == True:
                break
            # 설정한 데이터의 크기보다 버퍼에 저장된 데이터의 크기가 작은 경우
            while len(self.data_buffer) < self.data_size:
                # 데이터 수신
                self.data_buffer += self.client_socket.recv(4096)

            self.client_socket.sendall("10".encode())
            # 버퍼의 저장된 데이터 분할
            packed_data_size = self.data_buffer[:self.data_size]
            self.data_buffer = self.data_buffer[self.data_size:]
            # struct.unpack : 변환된 바이트 객체를 원래의 데이터로 변환
            frame_size = struct.unpack(">L", packed_data_size)[0]
            # 프레임 데이터의 크기보다 버퍼에 저장된 데이터의 크기가 작은 경우
            while len(self.data_buffer) < frame_size:
                # 데이터 수신
                self.data_buffer += self.client_socket.recv(4096)
            # 프레임 데이터 분할
            frame_data = self.data_buffer[:frame_size]
            self.data_buffer = self.data_buffer[frame_size:]
            # print("수신 프레임 크기 : {} bytes".format(frame_size))
            # loads : 직렬화된 데이터를 역직렬화
            # 역직렬화(de-serialization) : 직렬화된 파일이나 바이트 객체를 원래의 데이터로 복원하는 것
            frame = pickle.loads(frame_data)

            # imdecode : 이미지(프레임) 디코딩
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if self.check_detect_person or self.check_detect_animal:
                frame = self.YoloDetector.Detect_person_animal_YOLO(frame=frame, size=320, score_threshold=0.4, nms_threshold=0.4,
                                                                   username=self.username, camid=self.camid,
                                                  check_detect_person=self.check_detect_person,
                                                  check_detect_animal=self.check_detect_animal)
            if self.check_recognition_face:
                pass

            if self.recording_video_check==True:
                self.out.write(frame)

            ret, frame = cv2.imencode('.jpg', frame)
            self.imagesave = frame
            self.imageFrame = frame.tobytes()

    def capture_picture(self, puser):
        user = puser
        cp = CapturePicture()
        cp.uid = user
        file = ContentFile(self.imagesave)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        file.name = timestamp + '.jpg'
        cp.image = file
        cp.time = timestamp
        cp.camid = self.camid
        cp.save()

    def recording_video(self, puser):
        if self.recording_video_check == False:
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            self.rvfilename = 'media/tempVideoRepository/'+timestamp + '.mp4'
            print(self.rvfilename)
            self.out = cv2.VideoWriter(self.rvfilename, cv2.VideoWriter_fourcc(*'H264'), 20, (640, 480))
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

            fp = open(saved_filename, 'rb')
            vf = fp.read()
            file = ContentFile(vf)
            file.name = timestamp + '.mp4'
            rv.video = file
            rv.camid = self.camid
            rv.save()

    def get_frame(self):
        return self.imageFrame

    def disconnet(self):
        self.check = True
        self.client_socket.close()
