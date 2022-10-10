# Generated by Django 4.0.3 on 2022-04-18 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
                ('union', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short_name', models.CharField(default='', max_length=10)),
                ('formed', models.DateField()),
                ('party_logo', models.ImageField(blank=True, default='defaults/partylogo.png', null=True, upload_to='partylogo/')),
            ],
        ),
        migrations.CreateModel(
            name='PendingRegistrations',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('fathers_name', models.CharField(max_length=60)),
                ('mothers_name', models.CharField(max_length=60)),
                ('adhaar_num', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('visible', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('hidden', 'Hidden'), ('idle', 'Idle'), ('running', 'Running'), ('finished', 'Finished'), ('published', 'Published'), ('archived', 'Archived')], default='hidden', max_length=20)),
                ('regions', models.ManyToManyField(to='elections.constituency')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('constituency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.constituency')),
                ('election', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.election')),
                ('party', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elections.party')),
            ],
        ),
    ]