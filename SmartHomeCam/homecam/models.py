from django.db import models

from account.models import AuthUser

def user_directory_path(instance, filename):
    return 'images/capture/{}/{}'.format(instance.uid, filename)

def user_directory_path_video_userRequest(instance, filename):
    return 'videos/userRequest/{}/{}'.format(instance.uid, filename)

def user_directory_path_detect_person(instance, filename):
    return 'images/detectPerson/{}/{}'.format(instance.uid, filename)

def user_directory_path_recognition_face(instance, filename):
    return 'images/recognitionFace/{}/{}'.format(instance.uid, filename)

def user_directory_path_detect_fire(instance, filename):
    return 'images/detectFire/{}/{}'.format(instance.uid, filename)

def user_directory_path_safemode_noaction(instance, filename):
    return 'images/noaction/{}/{}'.format(instance.uid, filename)

def user_directory_path_detect_falldown(instance, filename):
    return 'images/detectFalldown/{}/{}'.format(instance.uid, filename)

# 알림 저장
class Alarm(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    camid = models.CharField(max_length=45, blank=True, null=True)
    time = models.DateTimeField()
    confirm = models.IntegerField()
    type = models.CharField(max_length=45, blank=True, null=True)
    did = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alarm'

# 홈카메라 정보 저장
class Homecam(models.Model):
    camid = models.CharField(primary_key=True, max_length=45)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    po_person = models.IntegerField(blank=True, null=True)
    po_unknown = models.IntegerField(blank=True, null=True)
    po_animal = models.IntegerField(blank=True, null=True)
    po_fire = models.IntegerField(blank=True, null=True)
    po_safe_noperson = models.IntegerField(blank=True, null=True)
    po_safe_noaction = models.IntegerField(blank=True, null=True)
    po_safe_no_person_day = models.IntegerField(blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'homecam'
        unique_together = (('camid', 'uid'),)

# 홈카메라 연결/해제 정보 저장
class CamConnectHistory(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    camid = models.CharField(max_length=45, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    division = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cam_connect_history'

# 홈캠 모드 on/off 기록 저장
class HomecamModeUseHistory(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    camid = models.CharField(max_length=45, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    mode = models.CharField(max_length=45, blank=True, null=True)
    division = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'homecam_mode_use_history'

# 사용자 캡처 이미지
class CapturePicture(models.Model):
    cpid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image = models.ImageField(upload_to=user_directory_path)
    image_s3 = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capture_picture'

# 사용자 녹화 동영상
class RecordingVideo(models.Model):
    rvid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    video = models.FileField(upload_to=user_directory_path_video_userRequest)
    video_s3 = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording_video'

# 홈캠모드 - 사람 탐지 모드
class DetectPerson(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_detect_person)
    image2 = models.ImageField(upload_to=user_directory_path_detect_person)
    image1_s3 = models.TextField(blank=True, null=True)
    image2_s3 = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_person'

# 홈캠모드 - 반려동물 탐지 모드
class DetectAnimal(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    species = models.IntegerField(blank=True, null=True)
    location = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_animal'

# 홈캠모드 - 외부인 탐지 모드
class DetectUnknown(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_recognition_face)
    image2 = models.ImageField(upload_to=user_directory_path_recognition_face)
    image1_s3 = models.TextField(blank=True, null=True) # TextField
    image2_s3 = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_unknown'

# 홈캠모드 - 화재 탐지 모드
class DetectFire(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_detect_fire)
    image2 = models.ImageField(upload_to=user_directory_path_detect_fire)
    image1_s3 = models.TextField(blank=True, null=True)
    image2_s3 = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_fire'

# 홈캠모드 - 일정시간 사람 미탐지 모드
class SafeModeNodetect(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    time = models.DateTimeField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'safe_mode_nodetect'

# 홈캠모드 - 사람 행동 미감지 모드
class SafeModeNoaction(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_safemode_noaction)
    image2 = models.ImageField(upload_to=user_directory_path_safemode_noaction)
    image1_s3 = models.TextField(blank=True, null=True)
    image2_s3 = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'safe_mode_noaction'

'''
class DetectFalldown(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_detect_falldown)
    image2 = models.ImageField(upload_to=user_directory_path_detect_falldown)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_falldown'

'''