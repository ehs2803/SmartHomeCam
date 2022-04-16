import cv2
import struct
import pickle

class Frame:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.data_buffer = b""
        self.data_size = struct.calcsize("L")

    def get_frame(self):
        # 설정한 데이터의 크기보다 버퍼에 저장된 데이터의 크기가 작은 경우
        while len(self.data_buffer) <self.data_size:
            # 데이터 수신
            self.data_buffer += self.client_socket.recv(4096)
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
        print("수신 프레임 크기 : {} bytes".format(frame_size))
        # loads : 직렬화된 데이터를 역직렬화
        # 역직렬화(de-serialization) : 직렬화된 파일이나 바이트 객체를 원래의 데이터로 복원하는 것
        frame = pickle.loads(frame_data)

        # imdecode : 이미지(프레임) 디코딩
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        #frame = preproc2(frame)
        #frame = detect_human_algorithms(frame, init_args_user, self.rpIndex)

        ret, frame = cv2.imencode('.jpg', frame)
        return frame.tobytes()