import time
import torch
import numpy as np
import torchvision.transforms as transforms
# from pytorchyolo.models import load_model
from queue import Queue
from threading import Thread


# from Detection.Utils import  ResizePadding
from homecam.algorithm.openpose.Detection.Models import load_model
from homecam.algorithm.openpose.Detection.Utils import ResizePadding, non_max_suppression


class TinyYOLOv3_onecls(object):
    def __init__(self,
                 input_size=416,
                 config_file='homecam/algorithm/openpose/yolov3-tiny.cfg',
                 weight_file='homecam/algorithm/openpose/yolov3-tiny.weights',
                 nms=0.2,
                 conf_thres=0.45,
                 device='cuda'):
        self.input_size = input_size
        self.model=load_model(config_file, weight_file)
        self.model.eval()
        self.device = device
        self.nms = nms
        self.conf_thres = conf_thres
        self.resize_fn = ResizePadding(input_size, input_size)
        self.transf_fn = transforms.ToTensor()

    def detect(self, image, need_resize=True, expand_bb=5):
        image_size = (self.input_size, self.input_size)
        if need_resize:
            image_size = image.shape[:2]
            image = self.resize_fn(image)
        image = self.transf_fn(image)[None, ...]
        scf = torch.min(self.input_size / torch.FloatTensor([image_size]), 1)[0]
        detected = self.model(image.to(self.device))
        detected = non_max_suppression(detected, self.conf_thres, self.nms)[0]
        if detected is not None:
            detected[:, [0, 2]] -= (self.input_size - scf * image_size[1]) / 2
            detected[:, [1, 3]] -= (self.input_size - scf * image_size[0]) / 2
            detected[:, 0:4] /= scf # x,y 좌표

            detected[:, 0:2] = np.maximum(0, detected[:, 0:2] - expand_bb)
            detected[:, 2:4] = np.minimum(image_size[::-1], detected[:, 2:4] + expand_bb)
            
        return detected


class ThreadDetection(object):
    def __init__(self,
                 dataloader,
                 model,
                 queue_size=256):
        self.model = model

        self.dataloader = dataloader
        self.stopped = False
        self.Q = Queue(maxsize=queue_size)

    def start(self):
        t = Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            images = self.dataloader.getitem()

            outputs = self.model.detect(images)

            if self.Q.full():
                time.sleep(2)
            self.Q.put((images, outputs))

    def getitem(self):
        return self.Q.get()

    def stop(self):
        self.stopped = True

    def __len__(self):
        return self.Q.qsize()







