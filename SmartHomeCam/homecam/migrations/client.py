from threading import Thread

from homecam.frame import Frame


class Client:
    def __init__(self, username, client_socket):
        self.id = 0
        self.cnt = 0
        self.username = username
        self.connections = {}
        self.threads = {}

        self.id += 1
        self.cnt+=1
        conn = Frame(client_socket)
        self.connections[str(self.id)]=conn

        live_detect_thread = Thread(target=conn.detect_live)
        live_detect_thread.start()
        self.threads[str(self.id)] = live_detect_thread

    def add_client(self, client_socket):
        self.id+=1
        self.cnt += 1
        conn = Frame(client_socket)
        self.connections[str(self.id)] = conn
        live_detect_thread = Thread(target=conn.detect_live)
        live_detect_thread.start()
        self.threads[str(self.id)] = live_detect_thread

    def disconnect_socket(self, id):
        self.connections[id].disconnet()
        del self.connections[id]
        #del self.threads[id]
        self.cnt-=1
        print(111111111111111111111111111)
        print(self.cnt)

