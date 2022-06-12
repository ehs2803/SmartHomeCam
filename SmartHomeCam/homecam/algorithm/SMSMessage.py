import boto3

class SmsSender:
    def __init__(self):
        self.client = boto3.client(
            "sns",
            aws_access_key_id="",
            aws_secret_access_key="",
            region_name="ap-northeast-1"  # 도쿄
        )

    def sendSMS(self, phoneNumber, messageContent):
        self.client.publish(
            PhoneNumber=phoneNumber, #"+8201047862803",
            Message=messageContent #"AWS SMS 파이썬 테스트"
        )

