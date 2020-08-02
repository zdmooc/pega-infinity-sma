from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class PegaNode(models.Model):
    class ProductionLevels(models.IntegerChoices):
        SANDBOX = 1
        DEVELOPMENT = 2
        QA = 3
        PRELIVE = 4
        PRODUCTION = 5

    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    production_level = models.IntegerField(choices=ProductionLevels.choices)

    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@receiver(post_save, sender=PegaNode)
def peganode_post_save(sender, instance: PegaNode, created: bool, *args, **kwargs):
    """
    When new PegaNode created - create permission associated with it
    """
    if created:
        content_type = ContentType.objects.get_for_model(sender)
        permission = Permission.objects.create(
            codename='can_access_{}'.format(instance.pk),
            name='Can access {}'.format(instance.name),
            content_type=content_type,
        )


@receiver(post_delete, sender=PegaNode)
def peganode_post_delete(sender, instance: PegaNode, *args, **kwargs):
    """
    When PegaNode deleted - delete permission associated with it
    """
    content_type = ContentType.objects.get_for_model(sender)
    Permission.objects.filter(
        codename='can_access_{}'.format(instance.pk),
        content_type=content_type,
    ).delete()
