# Generated by Django 2.2.20 on 2021-06-28 12:48

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0006_auto_20210628_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='image',
        ),
        migrations.AddField(
            model_name='crop',
            name='imageF',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to='images/', verbose_name='ImageF'),
        ),
    ]
