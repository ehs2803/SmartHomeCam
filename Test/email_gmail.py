
# 메일 모듈이다.
import smtplib
# 메일 메시지를 만드 모듈이다. (MIMEBase는 이하 MIMEMultipart, MIMEText, MIMEApplication, MIMEImage, MIMEAudio)의 상위 모듈이다.
# 굳이 선언할 필요없다.
#from email.mime.base import MIMEBase;
# 메일의 Data 영역의 메시지를 만드는 모듈 (MIMEText, MIMEApplication, MIMEImage, MIMEAudio가 attach되면 바운더리 형식으로 변환)
from email.mime.multipart import MIMEMultipart
# 메일의 본문 내용을 만드는 모듈
from email.mime.text import MIMEText
# 메일의 첨부 파일을 base64 형식으로 변환
from email.mime.application import MIMEApplication
# 메일의 이미지 파일을 base64 형식으로 변환(Content-ID 생성)
from email.mime.image import MIMEImage
# 메일의 음악 파일을 base64 형식으로 변환(Content-ID 생성)
from email.mime.audio import MIMEAudio

# 파일 IO
import io

# 메일 서버와 통신하기 전에 메시지를 만든다.
data = MIMEMultipart();
# 송신자 설정
data['From'] = "ehs2803@skuniv.ac.kr";
# 수신자 설정 (복수는 콤마 구분이다.)
data['To'] = "hr2803@naver.com,ehs1781@gmail.com";
# 참조 수신자 설정 data['Cc'] = "nowonbun@gmail.com";
# 숨은 참조 수신자 설정 data['Bcc'] = "nowonbun@gmail.com"
# 메일 제목
data['Subject'] = "[SmartHomecam] 보안 메일"

# 이미지 파일 추가
#with open("data/my_image.jpg", 'rb') as fp:
fp1 = open("data/faceimages/1.jpg", 'rb')
fp2 = open("data/faceimages/2.jpg", 'rb')
# Name은 메일 수신자에서 설정되는 파일 이름

img1 = MIMEImage(fp1.read(), Name = "img1")
img2 = MIMEImage(fp2.read(), Name = "img2")
# 해더에 Content-ID 추가(본문 내용에서 cid로 링크를 걸 수 있다.)
img1.add_header('Content-ID', '<capture1>')
img2.add_header('Content-ID', '<capture2>')
# Data 영역의 메시지에 바운더리 추가
data.attach(img1)
data.attach(img2)

# 텍스트 형식의 본문 내용
#msg = MIMEText("Hello world", 'plain');
# Html 형식의 본문 내용 (cid로 이미 첨부 파일을 링크했다.)
msg = MIMEText("""
    <h1>Hello Test</h1><br/>
    <h2>이미지1</h2>
    <img src='cid:capture1'>
    <h2>이미지2</h2>
    <img src='cid:capture2'>
"""
,'html')
# Data 영역의 메시지에 바운더리 추가
data.attach(msg)

# 메일 서버와 telnet 통신 개시
server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()  # say Hello
server.starttls()  # TLS 사용시 필요
# 로그인 한다.
server.login('ehs2803@skuniv.ac.kr', '')
# MAIL(송신자) 설정
sender = data['From'];
# RCPT(수신자), 리스트로 보낸다.
# 수신자 추가
receiver = data['To'].split(",");

# 메일 프로토콜 상 MAIL, RCPT, DATA 순으로 메시지를 보내야 하는데 이걸 sendmail함수에서 자동으로 해준다.
server.sendmail(sender, receiver, data.as_string());
# QUIT을 보내고 접속을 종료하고 메일을 보낸다.
server.quit();


'''
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()  # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('ehs2803@skuniv.ac.kr', '')

msg = MIMEText('확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......')
msg['Subject'] = '확이되지 않은 사람 확인'
msg['To'] = 'hr2803@naver.com'
smtp.sendmail('ehs2803@skuniv.ac.kr', 'hr2803@naver.com', msg.as_string())

smtp.quit()
'''


'''
class EmailHTMLImageContent:
    """e메일에 담길 이미지가 포함된 컨텐츠"""

    def __init__(self, str_subject, str_image_file_name, str_cid_name, template, template_params):
        """이미지파일(str_image_file_name), 컨텐츠ID(str_cid_name)사용된 string template과 딕셔너리형 template_params받아 MIME 메시지를 만든다"""
        assert isinstance(template, Template)
        assert isinstance(template_params, dict)
        self.msg = MIMEMultipart()

        # e메일 제목을 설정한다
        self.msg['Subject'] = str_subject  # e메일 제목을 설정한다

        # e메일 본문을 설정한다
        str_msg = template.safe_substitute(**template_params)  # ${변수} 치환하며 문자열 만든다
        mime_msg = MIMEText(str_msg, 'html')  # MIME HTML 문자열을 만든다
        self.msg.attach(mime_msg)

        # e메일 본문에 이미지를 임베딩한다
        assert template.template.find("cid:" + str_cid_name) >= 0, 'template must have cid for embedded image.'
        assert os.path.isfile(str_image_file_name), 'image file does not exist.'
        with open(str_image_file_name, 'rb') as img_file:
            mime_img = MIMEImage(img_file.read())
            mime_img.add_header('Content-ID', '<' + str_cid_name + '>')
        self.msg.attach(mime_img)

    def get_message(self, str_from_email_addr, str_to_eamil_addrs):
        """발신자, 수신자리스트를 이용하여 보낼메시지를 만든다 """
        mm = copy.deepcopy(self.msg)
        mm['From'] = str_from_email_addr  # 발신자
        mm['To'] = ",".join(str_to_eamil_addrs)  # 수신자리스트
        return mm


class EmailSender:
    """e메일 발송자"""

    def __init__(self, str_host, num_port=25):
        """호스트와 포트번호로 SMTP로 연결한다 """
        self.str_host = str_host
        self.num_port = num_port
        self.ss = smtplib.SMTP(host=str_host, port=num_port)
        # SMTP인증이 필요하면 아래 주석을 해제하세요.
        # self.ss.starttls() # TLS(Transport Layer Security) 시작
        # self.ss.login('계정명', '비밀번호') # 메일서버에 연결한 계정과 비밀번호

    def send_message(self, emailContent, str_from_email_addr, str_to_eamil_addrs):
        """e메일을 발송한다 """
        cc = emailContent.get_message(str_from_email_addr, str_to_eamil_addrs)
        self.ss.send_message(cc, from_addr=str_from_email_addr, to_addrs=str_to_eamil_addrs)
        del cc

str_subject = 'hello with image'
template = Template("""<html>
                            <head></head>
                            <body>
                                Hi ${NAME}.<br>
                                <img src="cid:my_image1"><br>
                                This is a test message.
                            </body>
                        </html>""")
template_params       = {'NAME':'Son'}
str_image_file_name   = 'justice.png'
str_cid_name          = 'my_image1'
emailHTMLImageContent = EmailHTMLImageContent(str_subject, str_image_file_name, str_cid_name, template, template_params)

str_from_email_addr = 'god@test.com' # 발신자
str_to_eamil_addrs  = ['angel@test.com', 'devil@test.com'] # 수신자리스트
emailSender.send_message(emailHTMLImageContent, str_from_email_addr, str_to_eamil_addrs)

'''

'''
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()  # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('ehs2803@skuniv.ac.kr', 'Hr167722!!')

msg = MIMEText('확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......'
               '확인되지 않은 사람이 확인되었습니다......확인되지 않은 사람이 확인되었습니다......')
msg['Subject'] = '확이되지 않은 사람 확인'
msg['To'] = 'hr2803@naver.com'
smtp.sendmail('ehs2803@skuniv.ac.kr', 'hr2803@naver.com', msg.as_string())

smtp.quit()

'''
