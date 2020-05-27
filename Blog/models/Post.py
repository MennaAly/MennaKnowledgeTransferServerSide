from django.db import models
from MasterData.models import Tag

import datetime


class Post(models.Model):
    title = models.CharField(max_length=225)
    markdwon_content = models.TextField()
    created_date = models.DateField(default=datetime.date.today())
    tags = models.ManyToManyField(Tag)
    parsed_html_content = models.TextField()
