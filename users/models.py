from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


#https://wsvincent.com/django-custom-user-model-tutorial/
#https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    # add additional fields in here

    def __str__(self):
        return self.email