from django.db import models

from account.models import AuthUser

def user_directory_path(instance, filename):
    return 'images/capture/{}/{}'.format(instance.uid, filename)

class CapturePicture(models.Model):
    cpid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    image = models.ImageField(upload_to=user_directory_path)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capture_picture'