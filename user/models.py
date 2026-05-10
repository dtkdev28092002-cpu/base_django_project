from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Tag(models.Model):
    name = models.CharField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="tags", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "tags"

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = "posts"

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id} on {self.post_id}"
    class Meta:
        db_table = "comments"

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