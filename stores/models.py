from django.db import models
from django.contrib.auth import get_user_model


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StoreComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='store_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


