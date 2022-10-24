import boto3
import uuid

import numpy as np
from PIL import Image

from SmartHomeCam.settings.base import AWS_ACCESS_KEY_S3, AWS_SECRET_KEY_S3, S3_BUCKET_NAME, S3_BUCKET_REGION, S3_BUCKET_DIR

# s3 bucket 파일 업로드(이미지, 동영상)
class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file, dir):
        return self.client.upload(file, dir)

    def upload_video(self, file, dir):
        return self.client.upload_video(file,dir)

    def read_image(self,filename):
        return self.client.read_image_from_s3(filename)

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name, region, dir):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        resource_s3 = boto3.resource('s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3_client_get = resource_s3
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name
        self.region = region
        self.dir = dir

    def upload(self, file, s3dir):
        try:
            file_id = str(uuid.uuid4())
            extra_args = {'ContentType': 'image/jpg' }

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    self.dir+s3dir+file_id+'.jpg',
                    ExtraArgs = extra_args
                )
            return f'https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{self.dir}{s3dir}{file_id}.jpg'
        except Exception as e:
            print(e)
            return None

    def upload_video(self, file, s3dir):
        try:
            file_id = str(uuid.uuid4())
            extra_args = {'ContentType': 'video/mp4' }

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    self.dir+s3dir+file_id+'.mp4',
                    ExtraArgs = extra_args
                )
            return f'https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{self.dir}{s3dir}{file_id}.mp4'
        except Exception as e:
            print(e)
            return None

    def read_image_from_s3(self, filename):
        bucket = self.s3_client_get.Bucket(self.bucket_name)
        object = bucket.Object(self.dir+filename)
        response = object.get()
        file_stream = response['Body']
        img = Image.open(file_stream)
        img = np.array(img)
        return img


# MyS3Client instance
s3_client = MyS3Client(AWS_ACCESS_KEY_S3, AWS_SECRET_KEY_S3, S3_BUCKET_NAME, S3_BUCKET_REGION, S3_BUCKET_DIR)