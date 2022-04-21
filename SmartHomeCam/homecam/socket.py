import socket

from homecam.frame import Frame
from homecam.migrations.client import Client


class VideoCamera(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # Foo 클래스 객체에 _instance 속성이 없다면
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance                      # Foo._instance를 리턴

    def __init__(self):
        self.ip='127.0.0.1'
        self.port=50002
        self.threads = {} # 복수개의 라즈레리파이 객체
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()

    def __del__(self):
        self.server_socket.close()

    def run_server(self):
        while True:
            client_socket, addr = self.server_socket.accept();
            # socket의 recv함수는 연결된 소켓으로부터 데이터를 받을 대기하는 함수입니다. 최초 4바이트를 대기합니다.
            data = client_socket.recv(4);
            # 최초 4바이트는 전송할 데이터의 크기이다. 그 크기는 little 엔디언으로 byte에서 int형식으로 변환한다.
            length = int.from_bytes(data, "little");
            # 다시 데이터를 수신한다.
            data = client_socket.recv(length);
            # 수신된 데이터를 str형식으로 decode한다.
            msg = data.decode();

            if self.threads.get(msg):
                client_ = self.threads[msg]
                client_.add_client(client_socket)
                self.threads[msg] = client_
                print('#############################')
            else:
                client = Client(msg, client_socket)
                self.threads[msg] = client


