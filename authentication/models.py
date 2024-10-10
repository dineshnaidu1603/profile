from django.db import models
from django.contrib.auth.hashers import make_password
class Member(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    # Add any other fields required for the user's profile

    def save(self, *args, **kwargs):
        # Hash password before saving if not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
