# Generated by Django 2.2.6 on 2020-02-02 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0003_auto_20200202_0222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='file_id',
            new_name='minio_file_id',
        ),
        migrations.AlterField(
            model_name='challenge',
            name='category',
            field=models.SlugField(choices=[('programming', 'Programming'), ('cryptography', 'Cryptography'), ('packetanalysis', 'Packet Analysis'), ('trivia', 'Trivia'), ('webapp', 'Web App'), ('database', 'Database'), ('sysadmin', 'SysAdmin'), ('steganography', 'Steganography'), ('reversing', 'Reversing'), ('lockpicking', 'Lockpicking'), ('forensics', 'Forensics')], max_length=30),
        ),
    ]