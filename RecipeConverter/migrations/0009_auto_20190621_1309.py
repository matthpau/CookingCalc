# Generated by Django 2.2.1 on 2019-06-21 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecipeConverter', '0008_auto_20190621_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='converter',
            name='unit_source_type',
            field=models.CharField(choices=[('imp', 'Imperial'), ('met', 'Metric'), ('none', 'None')], max_length=10),
        ),
    ]