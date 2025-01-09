from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    image = models.ImageField(upload_to="users", null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    province = models.CharField(max_length=256, null=True, blank=True)
    zip_code = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
