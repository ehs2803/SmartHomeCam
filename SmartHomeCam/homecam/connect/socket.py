import datetime
import time

import socket
from account.models import AuthUser
from homecam.connect.client import Client

from django.contrib.auth.models import User

from homecam.models import Homecam

# 홈카메라 소켓 연결
class VideoCamera(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # VideoCamera 클래스 객체에 _instance 속성이 없다면
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)  # VideoCamera 클래스의 객체를 생성하고 VideoCamera._instance로 바인딩
        return cls._instance                      # VideoCamera._instance를 리턴

    def __init__(self):
        self.ip=''
        self.port=50000
        self.threads = {} # 복수개의 user 객체
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()

    def __del__(self):
        self.server_socket.close()

    def run_server(self):
        while True:
            client_socket, addr = self.server_socket.accept();
            # socket의 recv함수는 연결된 소켓으로부터 데이터를 받을 대기하는 함수. 최초 4바이트를 대기
            data = client_socket.recv(4);
            # 최초 4바이트는 전송할 데이터의 크기. 그 크기는 little 엔디언으로 byte에서 int형식으로 변환
            length = int.from_bytes(data, "little");
            # 다시 데이터를 수신.
            data = client_socket.recv(length);
            # 수신된 데이터를 str형식으로 decode
            msg = data.decode()
            userid, rpid = msg.split(':')

            check_db = False
            policy = {}
            user = User.objects.get(username=userid)
            homecam = Homecam.objects.filter(camid=rpid, uid=user.id)
            if homecam.count()==0: # 홈카메라 id가 db에 등록되지 않은경우
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                # Homecam 객체 초기화 및 db에 저장
                newHomecam = Homecam()
                newHomecam.camid = rpid
                newHomecam.uid = AuthUser.objects.get(username=user.username)
                newHomecam.po_person=0
                newHomecam.po_unknown=0
                newHomecam.po_animal=0
                newHomecam.po_fire=0
                newHomecam.po_safe_noperson=0
                newHomecam.po_safe_noaction=0
                newHomecam.po_safe_no_person_day=1
                newHomecam.reg_time=timestamp
                newHomecam.save()
                # 정책 설정
                policy['po_person'] = newHomecam.po_person
                policy['po_unknown'] = newHomecam.po_unknown
                policy['po_animal'] = newHomecam.po_animal
                policy['po_fire'] = newHomecam.po_fire
                policy['po_safe_noperson'] = newHomecam.po_safe_noperson
                policy['po_safe_noaction'] = newHomecam.po_safe_noaction
                policy['po_safe_no_person_day'] = newHomecam.po_safe_no_person_day
            else: # db에 저장되 있는 경우
                check_db=True
                # 정책 불러오기
                policy['po_person'] = homecam.get().po_person
                policy['po_unknown'] = homecam.get().po_unknown
                policy['po_animal'] = homecam.get().po_animal
                policy['po_fire'] = homecam.get().po_fire
                policy['po_safe_noperson'] = homecam.get().po_safe_noperson
                policy['po_safe_noaction'] = homecam.get().po_safe_noaction
                policy['po_safe_no_person_day'] = homecam.get().po_safe_no_person_day

            if self.threads.get(userid): # 해당 user객체가 존재하는 경우
                client_ = self.threads[userid]
                client_.add_client(client_socket, rpid, policy)
                self.threads[userid] = client_
            else:
                client = Client(userid, client_socket, rpid, policy)
                self.threads[userid] = client


