# Generated by Django 3.1.3 on 2022-06-06 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecam', '0006_detectfire'),
    ]

    operations = [
        migrations.CreateModel(
            name='SafeModeNodetect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('period', models.IntegerField(blank=True, null=True)),
                ('camid', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'safe_mode_nodetect',
                'managed': False,
            },
        ),
    ]
