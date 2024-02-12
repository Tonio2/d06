from django.dispatch import receiver, Signal

vote = Signal()

@receiver(vote)
def handle_vote(sender, **kwargs):
    bonus = kwargs.get('bonus', 0)
    user = kwargs.get('user', None)
    if user is not None:
        user.reputation += bonus        
        user.save()

