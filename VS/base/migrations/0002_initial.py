# Generated by Django 4.0.3 on 2022-04-18 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='region',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.constituency'),
        ),
        migrations.AddField(
            model_name='userdata',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
