from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    email   = models.EmailField()
    activat = models.BooleanField(default=True)
    update  = models.DateTimeField(auto_now=True)
    time    = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email

def user_create_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_create_receiver, sender=User)
