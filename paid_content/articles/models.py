from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Article(models.Model):
    title = models.CharField(max_length=128)
    img = models.ImageField(null=True, blank=True)
    text = models.TextField()
    paid_content = models.BooleanField()



