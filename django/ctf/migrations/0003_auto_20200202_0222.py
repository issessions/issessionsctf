# Generated by Django 2.2.6 on 2020-02-02 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0002_challenge_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='file_id',
            field=models.SlugField(default='', max_length=30, unique=True),
        ),
    ]