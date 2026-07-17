from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):


    ROLE_CHOICES=(
        ('user', 'User'),
        ('artists','Artists'),
        ('admin','Admin')
    )

    role=models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    profile_image=models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )


    bio=models.TextField(blank=True,null=True)


    profile_image = models.URLField(
        blank=True,
        null=True
    )

    favorite_genre = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )


    # following = models.ManyToManyField(
    # "self",
    # symmetrical=False,
    # related_name="followers",
    # blank=True
    # )

    def __str__(self):
        return self.username
    



class Follow(models.Model):

    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.follower.username} follows {self.following.username}"
