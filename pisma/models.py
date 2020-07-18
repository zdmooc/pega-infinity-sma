from django.db import models
from django.contrib.auth.models import User


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


