# Generated by Django 2.2.20 on 2021-06-28 14:59

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0008_auto_20210628_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='image_ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20),
        ),
    ]
