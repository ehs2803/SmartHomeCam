import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailSender:
    def __init__(self):
        self.data = None
        self.sender = "ehs2803@skuniv.ac.kr"

    def makeContent(self, receiver, subject, sendimg1, sendimg2):
        # 메일 서버와 통신하기 전에 메시지를 만든다.
        self.data = MIMEMultipart()
        # 송신자 설정
        self.data['From'] = self.sender
        # 수신자 설정 (복수는 콤마 구분이다.)
        self.data['To'] = "hr2803@naver.com,ehs1781@gmail.com"
        # 메일 제목
        self.data['Subject'] = "[SmartHomecam] 보안 메일"

        # 이미지 파일 추가
        fp1 = open("data/faceimages/1.jpg", 'rb')
        fp2 = open("data/faceimages/2.jpg", 'rb')
        # Name은 메일 수신자에서 설정되는 파일 이름

        img1 = MIMEImage(fp1.read(), Name="img1")
        img2 = MIMEImage(fp2.read(), Name="img2")
        # 해더에 Content-ID 추가(본문 내용에서 cid로 링크를 걸 수 있다.)
        img1.add_header('Content-ID', '<capture1>')
        img2.add_header('Content-ID', '<capture2>')
        # Data 영역의 메시지에 바운더리 추가
        self.data.attach(img1)
        self.data.attach(img2)

        # 텍스트 형식의 본문 내용
        # Html 형식의 본문 내용 (cid로 이미 첨부 파일을 링크했다.)
        msg = MIMEText("""
            <h1>Hello Test</h1><br/>
            <h2>이미지1</h2>
            <img src='cid:capture1'>
            <h2>이미지2</h2>
            <img src='cid:capture2'>
        """
                       , 'html')
        # Data 영역의 메시지에 바운더리 추가
        self.data.attach(msg)

    def sendEmail(self):
        # 메일 서버와 telnet 통신 개시
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()  # say Hello
        server.starttls()  # TLS 사용시 필요
        # 로그인 한다.
        server.login('ehs2803@skuniv.ac.kr', '')
        # MAIL(송신자) 설정
        sender = self.data['From']
        # RCPT(수신자), 리스트로 보낸다.
        # 수신자 추가
        receiver = self.data['To'].split(",")
        # 메일 프로토콜 상 MAIL, RCPT, DATA 순으로 메시지를 보내야 하는데 이걸 sendmail함수에서 자동으로 해준다.
        server.sendmail(sender, receiver, self.data.as_string())
        # QUIT을 보내고 접속을 종료하고 메일을 보낸다.
        server.quit()




