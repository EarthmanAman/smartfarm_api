# Generated by Django 2.2.20 on 2021-06-26 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='pic',
            field=models.ManyToManyField(to='farm.Image'),
        ),
    ]
