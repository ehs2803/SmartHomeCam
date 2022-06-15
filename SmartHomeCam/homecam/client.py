import datetime
import time
from threading import Thread

from account.models import AuthUser
from homecam.frame import Frame
from homecam.models import CamConnectHistory, HomecamModeUseHistory


class Client:
    def __init__(self, username, client_socket, rpid):
        self.cnt = 0
        self.username = username
        self.connections = {}
        self.threads = {}


        self.cnt+=1
        conn = Frame(client_socket, username,rpid)
        self.connections[rpid]=conn

        live_detect_thread = Thread(target=conn.detect_live)
        live_detect_thread.start()
        self.threads[rpid] = live_detect_thread

        cam_connetct_history = CamConnectHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cam_connetct_history.uid = user
        cam_connetct_history.camid = rpid
        cam_connetct_history.time = timestamp
        cam_connetct_history.division = 'CONNECT'
        cam_connetct_history.save()

    def add_client(self, client_socket, rpid):
        self.cnt += 1
        conn = Frame(client_socket, self.username, rpid)
        self.connections[rpid] = conn
        live_detect_thread = Thread(target=conn.detect_live)
        live_detect_thread.start()
        self.threads[rpid] = live_detect_thread

        cam_connetct_history = CamConnectHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cam_connetct_history.uid = user
        cam_connetct_history.camid = rpid
        cam_connetct_history.time = timestamp
        cam_connetct_history.division = 'CONNECT'
        cam_connetct_history.save()

    def disconnect_socket(self, id):
        if self.connections[id].check_detect_person:
            self.save_mode_use_off('DETECT_PERSON')
        if self.connections[id].check_recognition_face:
            self.save_mode_use_off('DETECT_UNKNOWNFACE')
        if self.connections[id].check_detect_fire:
            self.save_mode_use_off('DETECT_FIRE')
        if self.connections[id].check_detect_animal:
            self.save_mode_use_off('DETECT_ANIMAL')
        if self.connections[id].check_on_safemode:
            self.save_mode_use_off('SAFEMODE')

        self.connections[id].disconnet()
        del self.connections[id]
        #del self.threads[id]
        self.cnt-=1

        cam_connetct_history = CamConnectHistory()
        user = AuthUser.objects.get(username=self.username)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cam_connetct_history.uid = user
        cam_connetct_history.camid = id
        cam_connetct_history.time = timestamp
        cam_connetct_history.division = 'DISCONNECT'
        cam_connetct_history.save()

        print(111111111111111111111111111)
        print(self.cnt)

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

