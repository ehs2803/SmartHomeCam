from django.contrib.auth.models import User

from homecam.algorithm.Email import EmailSender
from homecam.algorithm.SMSMessage import SmsSender
from mypage.models import Family


class SafeMode(EmailSender, SmsSender):
    def __init__(self, username):
        self.username = username


        # 알림 연락처 정보
        self.PhoneNumberList=[]
        self.EmailAddressList=[]

    def run_safe_mode(self, frame, camid):
        pass

    def updateContactList(self, username):
        user = User.objects.get(username=username)
        family_members = Family.objects.filter(uid=user.id)
        self.PhoneNumberList.clear()
        self.EmailAddressList.clear()
        for family in family_members:
            self.EmailAddressList.append(family.email)
            self.PhoneNumberList.append(family.tel)
        print(self.EmailAddressList)
        print(self.PhoneNumberList)

    def sendSafeModeEmail(self, file1, file2):
        receivers = ''
        for email in self.EmailAddressList:
            receivers = receivers+email
            receivers = receivers+','
        receivers = receivers[:-1]
        super().makeContent(receiver=receivers, subject="[SmartHomecam] 안심모드 알림",
                            sendimg1=file1, sendimg2=file2)
        super().sendEmail()