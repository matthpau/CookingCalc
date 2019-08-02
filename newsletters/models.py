from django.db import models
from users.models import Country
from django.utils.translation import gettext_lazy as _

class SendHistory(models.Model):
    date = models.DateTimeField()
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    recipient_count = models.PositiveIntegerField()

