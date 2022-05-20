# Generated by Django 3.1.3 on 2022-05-18 15:11

from django.db import migrations, models
import homecam.models


class Migration(migrations.Migration):

    dependencies = [
        ('homecam', '0002_recordingvideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectPerson',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image1', models.ImageField(upload_to=homecam.models.user_directory_path_detect_person)),
                ('image2', models.ImageField(upload_to=homecam.models.user_directory_path_detect_person)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'detect_person',
                'managed': False,
            },
        ),
    ]