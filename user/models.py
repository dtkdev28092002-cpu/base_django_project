from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Tag(models.Model):
    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "tags"

class Role(models.Model):
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ADMIN, 'Admin'),
    ]
    name = models.CharField(choices=ROLE_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "roles"

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(
        Role,
        related_name="users",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is required for AbstractUser, but we won't use it for authentication

    def __str__(self):
        return self.email
    class Meta:
        db_table = "users"