# Generated by Django 2.2.3 on 2019-07-14 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20190712_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='add_1',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Address 1'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='add_city',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='add_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='local_offer_radius',
            field=models.FloatField(blank=True, default=5, verbose_name='Search radius for local offers (km)'),
        ),
    ]