# Generated by Django 4.0.3 on 2022-04-18 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_userdata_dob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='adhaar_num',
            new_name='adhaar_number',
        ),
    ]
