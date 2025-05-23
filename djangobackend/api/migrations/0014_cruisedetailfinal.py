# Generated by Django 5.1 on 2024-08-18 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_cruisedetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='CruiseDetailFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('month', models.CharField(max_length=100)),
                ('origin', models.CharField(max_length=100)),
                ('departure', models.CharField(max_length=100)),
                ('visiting', models.CharField(max_length=1000)),
                ('nights', models.IntegerField(default=0)),
                ('decks', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('seats', models.IntegerField(default=0)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('country', models.CharField(max_length=100)),
                ('continent', models.CharField(max_length=100)),
                ('image', models.ImageField(default='', upload_to='cruise/images')),
                ('cruiseName', models.CharField(default='Unnamed Cruise', max_length=100)),
                ('oceanviewRooms', models.IntegerField(default=0)),
                ('InteriorRooms', models.IntegerField(default=0)),
                ('oceanviewForward', models.IntegerField(default=0)),
                ('oceanviewMiddle', models.IntegerField(default=0)),
                ('oceanviewAft', models.IntegerField(default=0)),
                ('InteriorForward', models.IntegerField(default=0)),
                ('InteriorMiddle', models.IntegerField(default=0)),
                ('InteriorAft', models.IntegerField(default=0)),
            ],
        ),
    ]
