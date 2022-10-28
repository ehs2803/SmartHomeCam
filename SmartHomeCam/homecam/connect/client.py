import datetime
import time
from threading import Thread

from account.models import AuthUser
from homecam.connect.frame import Frame

from homecam.models import CamConnectHistory, HomecamModeUseHistory

# 특정 user 홈카메라 연결 관리 객체
class Client:
    def __init__(self, username, client_socket, rpid, policy):
        self.cnt = 0 # 해당 유저가 연결한 홈카메라 객체
        self.username = username # username
        self.connections = {} # 홈카메라 객체 저장
        self.threads = {} # 스레드 저장


        self.cnt+=1
        conn = Frame(client_socket, username,rpid, policy)
        self.connections[rpid]=conn
        live_detect_thread = Thread(target=self.thread_func, args=(rpid,conn,))#Thread(target=conn.detect_live) # 스레드 객체 생성
        live_detect_thread.start() # 스레드 시작
        self.threads[rpid] = live_detect_thread
        # 홈카메라 연결 기록 저장
        cam_connetct_history = CamConnectHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cam_connetct_history.uid = user
        cam_connetct_history.camid = rpid
        cam_connetct_history.time = timestamp
        cam_connetct_history.division = 'CONNECT'
        cam_connetct_history.save()

    # 각 홈카메라 스레드 함수
    def thread_func(self, rpid, conn):
        conn.detect_live() # 이미지 수신
        self.disconnect_socket(rpid) # 연결 해제

    # 새로운 홈카메라 연결 추가
    def add_client(self, client_socket, rpid, policy):
        self.cnt += 1
        conn = Frame(client_socket, self.username, rpid, policy)
        self.connections[rpid] = conn
        live_detect_thread = Thread(target=self.thread_func, args=(rpid,conn,))#Thread(target=conn.detect_live)
        live_detect_thread.start()
        self.threads[rpid] = live_detect_thread
        # 홈카메라 연결 기록 저장
        cam_connetct_history = CamConnectHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cam_connetct_history.uid = user
        cam_connetct_history.camid = rpid
        cam_connetct_history.time = timestamp
        cam_connetct_history.division = 'CONNECT'
        cam_connetct_history.save()

    # socket disconnet
    def disconnect_socket(self, id):
        # if self.connections[id].check_detect_person:
        #     self.save_mode_use_off('DETECT_PERSON')
        # if self.connections[id].check_recognition_face:
        #     self.save_mode_use_off('DETECT_UNKNOWNFACE')
        # if self.connections[id].check_detect_fire:
        #     self.save_mode_use_off('DETECT_FIRE')
        # if self.connections[id].check_detect_animal:
        #     self.save_mode_use_off('DETECT_ANIMAL')
        # if self.connections[id].check_on_safemode:
        #     self.save_mode_use_off('SAFEMODE')

        self.connections[id].disconnet()
        del self.connections[id]
        #del self.threads[id]
        self.cnt-=1
        # 홈카메라 연결 기록 저장
        cam_connetct_history = CamConnectHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cam_connetct_history.uid = user
        cam_connetct_history.camid = id
        cam_connetct_history.time = timestamp
        cam_connetct_history.division = 'DISCONNECT'
        cam_connetct_history.save()

    # mode on/off 이력 db 저장
    def save_mode_use_off(self, mode):
        mode_history = HomecamModeUseHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        mode_history.uid = user
        mode_history.camid = id
        mode_history.time = timestamp
        mode_history.mode = mode
        mode_history.division = 'OFF'
        mode_history.save()

