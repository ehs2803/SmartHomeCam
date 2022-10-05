import boto3
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import io


def read_image_from_s3(key):
    s3 = boto3.resource('s3',
                        aws_access_key_id='',
                        aws_secret_access_key=''
                        )
    bucket = s3.Bucket('')
    object1 = bucket.Object(key)
    response = object1.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return np.array(im)

# def read_image_from_s3(filename):
#     bucket = s3.Bucket('')
#     object = bucket.Object(filename)
#     file_stream = io.StringIO()
#     object.download_fileobj(file_stream)
#     img = mpimg.imread(file_stream)
#
#     # response = object.get()
#     # file_stream = response['Body']
#     # img = Image.open(file_stream)
#     # return img

read_image_from_s3('smarthomecam/real/family/3637b109-ccb4-4c94-b668-94c8913800a6.jpg')