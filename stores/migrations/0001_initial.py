# Generated by Django 2.2.1 on 2019-07-09 15:07

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(default='please complete country', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('add_house_number', models.CharField(max_length=100)),
                ('add_street', models.CharField(max_length=100)),
                ('add_postcode', models.CharField(max_length=20)),
                ('add_city', models.CharField(max_length=50)),
                ('add_country', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('my_name', models.CharField(max_length=100)),
                ('my_address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=50)),
                ('opening_hours', models.CharField(max_length=200)),
                ('website', models.CharField(max_length=50)),
                ('OSM_ID', models.BigIntegerField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('type_text', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('icon_text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StoreComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='store_comments', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='OSM_storetype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stores.StoreType'),
        ),
        migrations.AddField(
            model_name='store',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='store_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='my_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stores.Country'),
        ),
        migrations.AddField(
            model_name='store',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
