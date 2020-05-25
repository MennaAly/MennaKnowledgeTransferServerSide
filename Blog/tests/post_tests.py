from django.test import TestCase

from MasterData.models import Tag
from helper import authorization_setup, create_dummy_instances
import codecs
import os
from markdownify import markdownify as md
import markdown2

class ConvertHtmlToMarkDownThirdLibraryTest(TestCase):
    def setUp(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        post_content_html_file = codecs.open(os.path.join(THIS_FOLDER, 'post_content_test.html'))
        post_content_markdown_file = open(os.path.join(THIS_FOLDER, 'post_content_markdown.txt'), 'r')
        self.html_post_content = post_content_html_file.read()
        self.post_content_markdown = post_content_markdown_file.read()

    def test_convert_html_tomarkdown(self):
        markdown_converted_from_html = md(self.html_post_content)
        html_converted_from_markdown = markdown2.markdown(self.post_content_markdown)
        print('the markdown ', markdown_converted_from_html)
        print('the converted html ', html_converted_from_markdown)
        print('the original html ', self.html_post_content)
        self.assertEqual(html_converted_from_markdown,self.html_post_content)

# class CreatePostTest(TestCase):
#     def create_post_setup(self):
#         self.tags = create_dummy_instances(Tag, 4, False)
#         self.tag_ids = [tag.id for tag in self.tags]
#         self.html_post_content = codecs.open('post_content_test.html')
#         self.post_request_body = {
#             'title': 'how to effectively study clean code book',
#             'content': self.html_post_content
#         }
#
#     def setUp(self):
#         self.client = authorization_setup()
#         self.create_post_setup()
#
#     def test_create_post(self):
#         pass
