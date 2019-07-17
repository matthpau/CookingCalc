# Generated by Django 2.2.3 on 2019-07-17 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20190715_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='run_newsletter',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='local_offer_radius',
            field=models.FloatField(blank=True, default=10, verbose_name='Search radius for local offers (km)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='local_offer_receive',
            field=models.BooleanField(default=True, verbose_name='I would like to receive newsletters with local offers'),
        ),
    ]
