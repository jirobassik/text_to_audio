# Generated by Django 4.2.6 on 2023-12-02 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_to_audio_manager', '0003_taskaudiomanagermodel_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskaudiomanagermodel',
            options={'ordering': ['-time_add']},
        ),
        migrations.AlterField(
            model_name='taskaudiomanagermodel',
            name='task_id',
            field=models.CharField(max_length=100, verbose_name='ID задачи'),
        ),
    ]
