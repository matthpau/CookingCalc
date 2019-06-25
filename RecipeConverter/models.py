from django.db import models
from django.contrib.auth import get_user_model


class Converter(models.Model):
    system_choices = [
        ('imp', 'Imperial'),
        ('met', 'Metric'),
        ('none', 'None')  # for cups and spoons
        ]

    unit_source_name = models.CharField(max_length=60, unique=True)
    spoon_type = models.BooleanField(default=False)
    cup_type = models.BooleanField(default=False)
    test_can_delete_add_suffix = models.BooleanField(default=False)
        #this is needed for measures which can have the same keys in both systems
        # set = True where you expect this to be the case, eg teaspoons, cups, tablespoons
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
    source_url = models.URLField()
    original_text = models.TextField()
    converted_text = models.TextField()
    conversion_type = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + str(self.user) + str(self.created_at)




