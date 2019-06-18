from django.db import models
from django.contrib.auth import get_user_model


class Converter(models.Model):
    system_choices = [
        ('imp', 'Imperial'),
        ('met', 'Metric'),
        ]

    unit_source_name = models.CharField(max_length=60, unique=True)
    unit_source_type = models.CharField(max_length=10, choices=system_choices)
    unit_source_keys = models.CharField(max_length=500)
    unit_dest_name = models.CharField(max_length=60)
    unit_conversion = models.FloatField()

    def __str__(self):
        return str(self.unit_source_name) + ' to ' + str(self.unit_dest_name)


class Conversion(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    conversion_name = models.CharField(max_length=100, default='No name given')
    user_comments = models.CharField(max_length=500)
    original_text = models.TextField()
    original_ingredients = models.TextField()
    original_method = models.TextField()
    converted_ingredients = models.TextField()
    converted_method = models.TextField()
    converted_success = models.TextField()
    converted_fails = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + str(self.user) + str(self.created_at)




