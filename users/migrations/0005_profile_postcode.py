# Generated by Django 2.2.1 on 2019-07-11 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_add_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='postcode',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
