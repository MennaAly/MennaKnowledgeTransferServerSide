from django.db import models

from MasterData.models import Responsibility
from Portfolio.models import Project


class Job(models.Model):
    company_name = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField(null=True)
    position_name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project)
    responsibilities = models.ManyToManyField(Responsibility)
