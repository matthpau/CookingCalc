# Generated by Django 2.2.1 on 2019-06-23 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RecipeConverter', '0010_converter_add_suffix'),
    ]

    operations = [
        migrations.RenameField(
            model_name='converter',
            old_name='add_suffix',
            new_name='test_can_delete_add_suffix',
        ),
    ]