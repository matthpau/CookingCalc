# Generated by Django 2.2.3 on 2019-07-17 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0007_auto_20190716_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(verbose_name='Event end date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(verbose_name='Event start date'),
        ),
    ]
