import markdown2
from django.db import models
from MasterData.models import Tag

import datetime


class Post(models.Model):
    title = models.CharField(max_length=225)
    markdown_content = models.TextField()
    created_date = models.DateField(default=datetime.date.today())
    tags = models.ManyToManyField(Tag)
    parsed_html_content = models.TextField()

    def convert_content_from_markdown_to_html(self, markdown_content):
        return markdown2.markdown(markdown_content)

    def save(self, *args, **kwargs):
        self.parsed_html_content = self.convert_content_from_markdown_to_html(self.markdown_content)
        super(Post, self).save(*args, **kwargs)
