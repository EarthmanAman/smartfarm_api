# Generated by Django 2.2.20 on 2021-09-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0021_auto_20210907_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropschedule',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]