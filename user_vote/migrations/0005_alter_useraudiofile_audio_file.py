# Generated by Django 4.2.6 on 2023-11-26 13:38

from django.db import migrations, models
import utils.file_validation


class Migration(migrations.Migration):

    dependencies = [
        ('user_vote', '0004_remove_useraudiofile_test_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraudiofile',
            name='audio_file',
            field=models.FileField(upload_to='user_vote_media', validators=[utils.file_validation.MultipleFileExtensionValidator(('wav',)), utils.file_validation.ContentValidator(('audio/wav', 'audio/x-wav')), utils.file_validation.MaxFileSizeValidation(2097152)], verbose_name='Путь к аудио'),
        ),
    ]
