from django.db import models
from pytz import timezone

from django.conf import settings

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.date_joined.astimezone(korean_timezone)

    @property
    def last_login_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.last_login.astimezone(korean_timezone)

    class Meta:
        managed = False
        db_table = 'auth_user'

