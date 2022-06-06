import cv2
import numpy as np
import socket
import struct  # 바이트(bytes) 형식의 데이터 처리 모듈
import pickle  # 바이트(bytes) 형식의 데이터 변환 모듈
import torch
from playsound import playsound

from homecam.algorithm.openpose.ActionsEstLoader import TSSTG
from homecam.algorithm.openpose.Detection.Utils import ResizePadding
from homecam.algorithm.openpose.DetectorLoader import TinyYOLOv3_onecls
from homecam.algorithm.openpose.PoseEstimateLoader import SPPE_FastPose
from homecam.algorithm.openpose.Track.Tracker import Tracker, Detection
from homecam.algorithm.openpose.fn import draw_single

'''
import cctv.views
'''

RPICNT = 0

def preproc2(image):
    resize_fn = ResizePadding(384, 384) # 기본 384*384 size~
    """preprocess function for CameraLoader.
    """
    image = resize_fn(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def kpt2bbox(kpt, ex=20):
    """Get bbox that hold on all of the keypoints (x,y)
    kpt: array of shape `(N, 2)`,
    ex: (int) expand bounding box,
    """
    return np.array((kpt[:, 0].min() - ex, kpt[:, 1].min() - ex,
                     kpt[:, 0].max() + ex, kpt[:, 1].max() + ex))

def init_user():
    device = 'cuda'
    print("device : ",device)  # cuda
    # DETECTION MODEL.
    inp_dets = 384
    detect_model = TinyYOLOv3_onecls(inp_dets, device=device)
    # POSE MODEL.
    inp_pose = '224x160'.split('x')
    inp_pose = (int(inp_pose[0]), int(inp_pose[1]))
    pose_model = SPPE_FastPose('resnet50', inp_pose[0], inp_pose[1], device=device)
    # Tracker.
    max_age = 30
    tracker = Tracker(max_age=max_age, n_init=3)
    # Actions Estimate.
    action_model = TSSTG()
    return detect_model,pose_model,tracker,action_model,inp_dets


def detect_human_algorithms(frame_img, init_args, cindex):
    detect_model, pose_model, tracker, action_model, inp_dets = init_args

    # 새로 추가한 label classes
    classes = ["person", "bicycle", "car", " motorcycle",
               "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
               "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
               "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
               "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
               "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
               "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife",
               "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
               "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table",
               "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
               "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
               "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush", "wheelchair"]

    frame = frame_img  # cam.getitem()

    # Detect humans bbox in the frame with detector model.
    detected = detect_model.detect(frame, need_resize=False, expand_bb=10)

    # Predict each tracks bbox of current frame from previous frames information with Kalman filter.
    tracker.predict()
    # Merge two source of predicted bbox together.
    for track in tracker.tracks:
        det = torch.tensor([track.to_tlbr().tolist() + [0.5, 1.0, 0.0]], dtype=torch.float32)
        detected = torch.cat([detected, det], dim=0) if detected is not None else det

    detections = []  # List of Detections object for tracking.
    if detected is not None:
        detected_hum = []
        for det_obj in detected:
            if torch.equal(det_obj.type(torch.int64)[6], torch.tensor(0)):
                detected_hum.append(det_obj.tolist())
        if detected_hum:
            detected_hum = torch.tensor(detected_hum)
            cctv.views.check_cam[cindex] = True
        else:
            detected_hum = None
            cctv.views.check_cam[cindex] = False
        if detected_hum is not None:  # 사람만 들어갈 수 있도록 조정
            # Predict skeleton pose of each bboxs.
            poses = pose_model.predict(frame, detected_hum[:, 0:4], detected_hum[:, 4])
            # Create Detections object.
            detections = [Detection(kpt2bbox(ps['keypoints'].numpy()),
                                    np.concatenate((ps['keypoints'].numpy(),
                                                    ps['kp_score'].numpy()), axis=1),
                                    ps['kp_score'].mean().numpy()) for ps in poses]
        # # 원래 있던 yolo VISUALIZE.
        # (x1, y1, x2, y2, object_conf, class_score, class_pred)
        human = []
        bed = []
        for bb in detected[:, :]:  # torch.cat( [detected[:, :], detected_oth[:,:]]):
            detect_obj = bb.type(torch.int64).tolist()
            detect_name = detect_obj[6]
            name = detect_name
            x1, y1, x2, y2 = detect_obj[0:4]
            # if torch.equal(detect_name ,torch.tensor(0)): # <- 사람만 인식하여 그림 그려줌
            if detect_name == 0:
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                frame = cv2.putText(frame, classes[name], (x1 + 5, y1 - 15), cv2.FONT_HERSHEY_COMPLEX,
                                    0.4, (0, 0, 255), 1)
                human.append(detect_obj[0:4])
            else:
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                frame = cv2.putText(frame, classes[name], (x1 + 5, y1 - 15), cv2.FONT_HERSHEY_COMPLEX,
                                    0.4, (0, 255, 0), 1)
    # Update tracks by matching each track information of current and previous frame or
    # create a new track if no matched.
    tracker.update(detections)

    for i, track in enumerate(tracker.tracks):
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        bbox = track.to_tlbr().astype(int)
        center = track.get_center().astype(int)
        action = 'pending..'
        clr = (0, 255, 0)
        # Use 30 frames time-steps to prediction.
        if len(track.keypoints_list) == 30:
            pts = np.array(track.keypoints_list, dtype=np.float32)
            out = action_model.predict(pts, frame.shape[:2])
            action_name = action_model.class_names[out[0].argmax()]
            action = '{}: {:.2f}%'.format(action_name, out[0].max() * 100)
            if action_name == 'Fall Down':
                clr = (255, 0, 0)
            elif action_name == 'Lying Down':
                clr = (255, 200, 0)
            if action_name == 'Fall Down':  # action_name이 핵심
                print("act", action_name)
                cctv.views.check_cam[cindex] = True
                tts_s_path = 'data/falldown_alarm.mp3'  # 음성 알림 파일
                playsound(tts_s_path)  # 음성으로 알림
            else:
                cctv.views.check_cam[cindex] = False
        # VISUALIZE.
        if track.time_since_update == 0:
            if True:
                frame = draw_single(frame, track.keypoints_list[-1])
            frame = cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 1)
            frame = cv2.putText(frame, str(track_id), (center[0], center[1]), cv2.FONT_HERSHEY_COMPLEX,
                                0.4, (255, 0, 0), 2)
            frame = cv2.putText(frame, action, (bbox[0] + 5, bbox[1] + 15), cv2.FONT_HERSHEY_COMPLEX,
                                0.4, clr, 1)
    # Show Frame.
    frame = cv2.resize(frame, (0, 0), fx=2., fy=2.)
    frame = frame[:, :, ::-1]
    return frame



#init_args_user =init_user()
class Frame:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.data_buffer = b""
        self.data_size = struct.calcsize("L")
        self.rpIndex = RPICNT

    def get_frame(self, n):
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
        frame = preproc2(frame)
        frame = detect_human_algorithms(frame, init_args_user, self.rpIndex)

        ret, frame = cv2.imencode('.jpg', frame)
        return frame.tobytes()
