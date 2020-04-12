from django.db import models

class Responsibility(models.Model):
    name = models.CharField(max_length=255)
