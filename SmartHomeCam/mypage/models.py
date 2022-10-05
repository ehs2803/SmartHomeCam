from django.db import models

# Create your models here.
from account.models import AuthUser

def user_directory_path(instance, filename):
    return 'images/family/{}/{}'.format(instance.uid.username, filename)


class Family(models.Model):
    fid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image1 = models.ImageField(upload_to=user_directory_path)
    image2 = models.ImageField(upload_to=user_directory_path ,blank=True, null=True)
    image3 = models.ImageField(upload_to=user_directory_path ,blank=True, null=True)
    image1_s3 = models.TextField(blank=True, null=True)
    image2_s3 = models.TextField(blank=True, null=True)
    image3_s3 = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=254, blank=True, null=True)
    tel = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'family'
        unique_together = (('fid', 'uid'),)