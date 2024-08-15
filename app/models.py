from django.db import models
from django.urls.base import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

class BankPayout(models.Model):
    status_code = models.TextField(blank=True)
    status = models.TextField(blank=True)
    message = models.TextField(blank=True)
    payout_id = models.TextField(blank=True)
    reference = models.TextField(blank=True)
    code = models.TextField(blank=True)
    type = models.TextField(blank=True)

class UpiId(models.Model):
    upi_id = models.TextField(blank=True)
    usage_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)