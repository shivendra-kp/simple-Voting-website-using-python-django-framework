# Generated by Django 4.0.3 on 2022-04-18 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingregistrations',
            name='region',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.constituency'),
        ),
    ]
