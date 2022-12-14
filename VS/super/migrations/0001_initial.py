# Generated by Django 4.0.4 on 2022-04-30 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elections', '0003_voted_electionresults'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoterIdCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=10001)),
                ('region', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='elections.constituency')),
            ],
        ),
    ]
