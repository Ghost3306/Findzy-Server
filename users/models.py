import uuid
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.functions import send_account_activation_email


class Profile(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, default=str(uuid.uuid4()), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_profile(sender, instance, created, **kwargs):
        if created:
            print("signal detected")
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email=email,email_token=email_token)
        else:
            pass

