from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db import models
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    fulfilled = models.BooleanField(default=False)


