# Generated by Django 4.1 on 2022-09-03 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecam', '0011_delete_detectfalldown'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('camid', models.CharField(blank=True, max_length=45, null=True)),
                ('time', models.DateTimeField()),
                ('confirm', models.IntegerField()),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
                ('did', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'alarm',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Homecam',
            fields=[
                ('camid', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('po_person', models.IntegerField(blank=True, null=True)),
                ('po_unknown', models.IntegerField(blank=True, null=True)),
                ('po_animal', models.IntegerField(blank=True, null=True)),
                ('po_fire', models.IntegerField(blank=True, null=True)),
                ('po_safe_no_person', models.IntegerField(blank=True, null=True)),
                ('po_safe_noaction', models.IntegerField(blank=True, null=True)),
                ('po_safe_no_person_day', models.IntegerField(blank=True, null=True)),
                ('reg_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'homecam',
                'managed': False,
            },
        ),
    ]