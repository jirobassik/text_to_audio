# Generated by Django 4.2.6 on 2023-10-12 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_alter_votemodel_audio_name'),
        ('history', '0002_alter_historymodel_use_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historymodel',
            name='use_vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.votemodel'),
        ),
    ]
