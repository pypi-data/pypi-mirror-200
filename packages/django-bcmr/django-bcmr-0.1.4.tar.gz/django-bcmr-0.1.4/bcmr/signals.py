from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db.models import F

from bcmr.models import Token, Registry


@receiver(post_save, sender=Token)
def token_post_save(sender, instance=None, created=False, **kwargs):
    if not created:
        token_registries = instance.registry_set.all()
        token_registries.update(patch=F('patch') + 1)


@receiver(m2m_changed, sender=Registry.tokens.through)
def registry_tokens_changed(sender, **kwargs):
    action = kwargs['action']
    instance = kwargs['instance']

    if action == 'pre_remove':
        instance.major += 1
        instance.save()
    elif action == 'pre_add':
        instance.minor += 1
        instance.save()
