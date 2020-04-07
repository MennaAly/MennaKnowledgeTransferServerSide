from django.db import models
from MasterData.models import Category, ImplementationTool


class Project(models.Model):
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    implementation_tools = models.ManyToManyField(ImplementationTool)
    categories = models.ManyToManyField(Category)
    url = models.CharField(max_length=225)
    github_url = models.CharField(max_length=225)
    created_date = models.DateField(auto_now_add=True)
