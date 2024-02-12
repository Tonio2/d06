from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(CustomUser, related_name="upvotes")
    downvotes = models.ManyToManyField(CustomUser, related_name="downvotes")

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote"),
        ]
