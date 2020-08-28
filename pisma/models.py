from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from pisma.logger import PismaLogger

logger = PismaLogger(__name__)


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
    logger.debug(
        "[peganode_post_save] start. sender: {}. instance: {}. created: {}. args: {}. kwargs: {}".format(
            sender, instance, created, args, kwargs
        )
    )
    if created:
        content_type = ContentType.objects.get_for_model(sender)
        permission = Permission.objects.create(
            codename="can_access_{}".format(instance.pk),
            name="Can access {}".format(instance.name),
            content_type=content_type,
        )
        logger.info(
            "[peganode_post_save] PegaNode {} and permission {} were created".format(
                instance, permission
            )
        )

    logger.debug("[peganode_post_save] end")


@receiver(post_delete, sender=PegaNode)
def peganode_post_delete(sender, instance: PegaNode, *args, **kwargs):
    """
    When PegaNode deleted - delete permission associated with it
    """
    logger.debug(
        "[peganode_post_delete] start. sender: {}. instance: {}. args: {}. kwargs: {}".format(
            sender, instance, args, kwargs
        )
    )
    content_type = ContentType.objects.get_for_model(sender)
    permissions = Permission.objects.filter(
        codename="can_access_{}".format(instance.pk),
        content_type=content_type,
    ).delete()

    logger.info(
        "[peganode_post_delete] PegaNode {} and permission {} were deleted".format(
            instance, permissions
        )
    )

    logger.debug("[peganode_post_delete] end")
