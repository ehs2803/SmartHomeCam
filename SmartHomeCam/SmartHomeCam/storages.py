import boto3
import uuid

from SmartHomeCam.settings.base import AWS_ACCESS_KEY_S3, AWS_SECRET_KEY_S3, S3_BUCKET_NAME, S3_BUCKET_REGION, S3_BUCKET_DIR

class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file, dir):
        return self.client.upload(file, dir)

    def upload_video(self, file, dir):
        return self.client.upload_video(file,dir)

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name, region, dir):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
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


# MyS3Client instance
s3_client = MyS3Client(AWS_ACCESS_KEY_S3, AWS_SECRET_KEY_S3, S3_BUCKET_NAME, S3_BUCKET_REGION, S3_BUCKET_DIR)