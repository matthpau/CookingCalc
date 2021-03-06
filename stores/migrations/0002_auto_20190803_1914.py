# Generated by Django 2.2.3 on 2019-08-03 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='storecomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='store_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='storecomment',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store'),
        ),
        migrations.AddField(
            model_name='storecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='OSM_storetype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stores.StoreType'),
        ),
        migrations.AddField(
            model_name='store',
            name='authorised_editors',
            field=models.ManyToManyField(related_name='authorised_editors', through='stores.AuthorisedEventEditors', to=settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name='event',
            name='created_by_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store'),
        ),
        migrations.AddField(
            model_name='authorisedeventeditors',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store'),
        ),
        migrations.AddField(
            model_name='authorisedeventeditors',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='authorisedeventeditors',
            constraint=models.UniqueConstraint(fields=('store', 'user'), name='Uniqueperstore'),
        ),
    ]
