# Generated by Django 4.2.6 on 2023-10-26 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0003_historymodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historymodel',
            name='audio_file',
            field=models.FileField(upload_to='history_media', verbose_name='Результат озвучивания'),
        ),
    ]
