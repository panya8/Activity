# Generated by Django 3.2.11 on 2022-01-13 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_auto_20220112_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_type',
            field=models.CharField(default='member', max_length=16),
        ),
    ]