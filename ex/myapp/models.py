from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        can_downvote_perm = Permission.objects.get(codename="can_downvote")
        can_delete_perm = Permission.objects.get(codename="delete_tip")

        if self.reputation >= 15:
            self.user_permissions.add(can_downvote_perm)
        else:
            self.user_permissions.remove(can_downvote_perm)

        if self.reputation >= 30:
            self.user_permissions.add(can_delete_perm)
        else:
            self.user_permissions.remove(can_delete_perm)



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

    def delete(self, *args, **kwargs):
        # Calculate reputation change
        reputation_loss = 5 * self.upvotes.count()
        reputation_gain = 2 * self.downvotes.count()
        reputation_change = reputation_gain - reputation_loss

        # Update author's reputation
        self.author.reputation += reputation_change
        self.author.save()

        # Proceed with the standard delete process
        super().delete(*args, **kwargs)
