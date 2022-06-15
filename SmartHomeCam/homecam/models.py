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

class CamConnectHistory(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    camid = models.CharField(max_length=45, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    division = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cam_connect_history'

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

class CapturePicture(models.Model):
    cpid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image = models.ImageField(upload_to=user_directory_path)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capture_picture'

class RecordingVideo(models.Model):
    rvid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    video = models.FileField(upload_to=user_directory_path_video_userRequest)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recording_video'

class DetectPerson(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_detect_person)
    image2 = models.ImageField(upload_to=user_directory_path_detect_person)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_person'

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

class RecognitionFace(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_recognition_face)
    image2 = models.ImageField(upload_to=user_directory_path_recognition_face)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recognition_face'

class DetectFire(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_detect_fire)
    image2 = models.ImageField(upload_to=user_directory_path_detect_fire)
    time = models.DateTimeField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detect_fire'

class SafeModeNodetect(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    time = models.DateTimeField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'safe_mode_nodetect'

class SafeModeNoaction(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path_safemode_noaction)
    image2 = models.ImageField(upload_to=user_directory_path_safemode_noaction)
    time = models.DateTimeField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    camid = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'safe_mode_noaction'

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
