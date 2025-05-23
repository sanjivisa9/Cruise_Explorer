# Generated by Django 5.1 on 2024-09-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_booking_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogedInUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
