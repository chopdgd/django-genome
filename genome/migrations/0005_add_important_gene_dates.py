# Generated by Django 2.2.4 on 2019-08-02 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genome', '0004_preferred_transcripts'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='date_approved',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='gene',
            name='date_modified',
            field=models.TextField(blank=True),
        ),
    ]
