# Generated by Django 2.2.1 on 2019-07-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20190712_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='temp_address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]