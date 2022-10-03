# Generated by Django 4.1 on 2022-10-03 01:17

from django.db import migrations, models
import homecam.models


class Migration(migrations.Migration):

    dependencies = [
        ('homecam', '0012_alarm_homecam'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnknownFace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image1', models.ImageField(upload_to=homecam.models.user_directory_path_recognition_face)),
                ('image2', models.ImageField(upload_to=homecam.models.user_directory_path_recognition_face)),
                ('image1_s3', models.ImageField(blank=True, null=True, upload_to='')),
                ('image2_s3', models.ImageField(blank=True, null=True, upload_to='')),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('camid', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'recognition_face',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='RecognitionFace',
        ),
    ]
