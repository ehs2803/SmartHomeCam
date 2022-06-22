import boto3

client = boto3.client(
"sns",
aws_access_key_id="",
aws_secret_access_key="",
region_name="ap-northeast-1" # 도쿄
)
'''
# 주제에 대한 구독자 추가
topic_arn = 'arn:aws:sns:ap-northeast-1:059024450957:SmartHomecam'
client.subscribe(
TopicArn=topic_arn,
Protocol='sms',
Endpoint='+8201047862803'
)
# 주제를 구독한 사람들에게 메시지 보내기
client.publish(
TopicArn=topic_arn ,
Message="파이썬 코드로 문자 보내기"
)
'''
# 주제나 구독자를 정하지 않으면 다음과 같이 간단하게 구현 가능
client.publish(
PhoneNumber="8201047862803",
Message="AWS SMS 파이썬 테스트"
)

