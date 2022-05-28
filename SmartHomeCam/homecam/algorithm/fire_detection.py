from homecam.algorithm.Email import EmailSender
from homecam.algorithm.SMSMessage import SmsSender


class FireDetector(EmailSender, SmsSender):
    pass