# Generated by Django 3.1.3 on 2022-06-01 09:39

from django.db import migrations, models
import homecam.models


class Migration(migrations.Migration):

    dependencies = [
        ('homecam', '0005_recognitionface'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectFire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image1', models.ImageField(upload_to=homecam.models.user_directory_path_detect_fire)),
                ('image2', models.ImageField(upload_to=homecam.models.user_directory_path_detect_fire)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('camid', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'detect_fire',
                'managed': False,
            },
        ),
    ]
