from django.db import models


class ImplementationTool(models.Model):
    name = models.CharField(max_length=225)