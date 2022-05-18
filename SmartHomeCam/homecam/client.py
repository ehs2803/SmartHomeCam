from threading import Thread

from homecam.frame import Frame


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

    def add_client(self, client_socket, rpid):
        self.cnt += 1
        conn = Frame(client_socket, self.username, rpid)
        self.connections[rpid] = conn
        live_detect_thread = Thread(target=conn.detect_live)
        live_detect_thread.start()
        self.threads[rpid] = live_detect_thread

    def disconnect_socket(self, id):
        self.connections[id].disconnet()
        del self.connections[id]
        #del self.threads[id]
        self.cnt-=1
        print(111111111111111111111111111)
        print(self.cnt)

