from django.dispatch import receiver, Signal
from .models import CustomUser
from django.shortcuts import get_object_or_404

vote = Signal()

@receiver(vote)
def handle_vote(sender, **kwargs):
    bonus = kwargs.get('bonus', 0)
    user = kwargs.get('user', None)
    if user is not None:
        user.reputation += bonus        
        user.save()

