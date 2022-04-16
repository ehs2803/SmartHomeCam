import socket
from debugpy.common.singleton import Singleton

from homecam.frame import Frame

class VideoCamera(object):
    def __new__(cls):
      if not hasattr(cls, 'instance'):
        cls.instance = super(Singleton, cls).__new__(cls)
      return cls.instance

    def __init__(self):
        self.ip='127.0.0.1'
        self.port=50002
        self.threads = [] # 복수개의 라즈레리파이 객체
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(10)
        self.conn, self.addr = self.sock.accept()  # 소켓통신 연결
        self.camera = Frame(self.conn)  # Frame을 얻기위한 객체 생성

    def __del__(self):
        self.sock.close()