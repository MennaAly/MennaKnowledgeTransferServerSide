from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    github_account = models.CharField(max_length=255)
    linkdin_account = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
