# Generated by Django 2.2.1 on 2019-07-11 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_postcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='postcode',
            new_name='add_postcode',
        ),
    ]
