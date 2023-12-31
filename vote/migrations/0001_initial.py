# Generated by Django 4.2.6 on 2023-10-21 10:17

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_name', models.CharField(max_length=20, unique=True, verbose_name='Название голоса')),
                ('audio_file', models.FileField(unique=True, upload_to='vote_media', verbose_name='Путь к аудио')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Тэги')),
            ],
            options={
                'ordering': ['audio_name'],
                'abstract': False,
                'indexes': [models.Index(fields=['audio_name'], name='vote_votemo_audio_n_ae709e_idx')],
            },
        ),
    ]
