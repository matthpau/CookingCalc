# Generated by Django 2.2.1 on 2019-07-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='add_city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='website',
            field=models.CharField(max_length=200),
        ),
    ]