import boto3

from SmartHomeCam.settings.base import AWS_ACCESS_KEY_ID_SNS, AWS_SECRET_ACCESS_KEY_SNS


class SmsSender:
    def sendSMS(self, phoneNumber, messageContent):
        client = boto3.client(
            "sns",
            aws_access_key_id=AWS_ACCESS_KEY_ID_SNS,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY_SNS,
            region_name="ap-northeast-1"  # 도쿄
        )
        client.publish(
            PhoneNumber=phoneNumber, #"+8201047862803",
            Message=messageContent #"AWS SMS 파이썬 테스트"
        )

