# Generated by Django 3.2.11 on 2022-03-22 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0016_auto_20220322_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='day_start',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
