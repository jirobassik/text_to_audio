# Generated by Django 4.2.6 on 2023-10-21 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_add', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Время добавления')),
                ('text', models.CharField(max_length=100, verbose_name='Озвученный текст')),
                ('audio_file', models.FileField(unique=True, upload_to='history_media', verbose_name='Результат озвучивания')),
            ],
            options={
                'ordering': ['text'],
            },
        ),
    ]
