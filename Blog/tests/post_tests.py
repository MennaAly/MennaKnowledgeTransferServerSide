from django.test import TestCase

from Blog.models import Post
from MasterData.models import Tag
from helper import authorization_setup, create_dummy_instances, reverse_url, create_request_body, get_response_content
import codecs
import os
from markdownify import markdownify as md
import markdown2


class ConvertHtmlToMarkDownThirdLibraryTest(TestCase):
    def setUp(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        post_content_html_file = codecs.open(os.path.join(THIS_FOLDER, 'post_content_test.html'))
        post_content_markdown_file = open(os.path.join(THIS_FOLDER, 'post_content_markdown.txt'), 'r')
        self.original_html_post_content = post_content_html_file.read()
        self.post_content_markdown = post_content_markdown_file.read()

    def test_convert_html_tomarkdown(self):
        html_converted_from_markdown = markdown2.markdown(self.post_content_markdown)
        # print('the converted html ', html_converted_from_markdown)
        # print('the original html ', self.original_html_post_content)


class CreatePostTest(TestCase):
    url = None
    tags = []
    tag_ids = []
    client = None
    response = None
    post_request_body = None
    number_of_dummy_tags = 4
    markdown_content = None

    def create_dummy_tags(self):
        self.tags = create_dummy_instances(Tag, self.number_of_dummy_tags, False)
        self.tag_ids = [tag.id for tag in self.tags]

    def read_markdown_content_from_file(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        post_content_markdown_file = open(os.path.join(THIS_FOLDER, 'post_content_markdown.txt'), 'r')
        self.markdown_content = post_content_markdown_file.read()

    def create_post_request_body(self):
        self.post_request_body = create_request_body({
            'title': 'how to effectively study clean code book',
            'markdown_content': self.markdown_content,
            'tag_ids': self.tag_ids
        })

    def setup_url(self):
        self.url = reverse_url("post-list", {})
        self.url += '?action=save'

    def initialize_creation_process_setup(self):
        self.create_dummy_tags()
        self.read_markdown_content_from_file()
        self.create_post_request_body()
        self.setup_url()

    def submit_create_post_url(self):
        self.response = self.client.post(self.url, self.post_request_body,
                                         content_type="application/json")

    def setUp(self):
        self.client = authorization_setup()
        self.initialize_creation_process_setup()
        self.submit_create_post_url()

    def test_creation_process_status(self):
        self.assertEqual(self.response.status_code, 200)

    def get_created_post(self):
        return Post.objects.last()

    def get_created_post_parsed_html_attribute(self):
        created_post = self.get_created_post()
        return created_post.parsed_html_content

    def convert_markdown_content_to_html(self):
        return markdown2.markdown(self.markdown_content)

    def test_create_post_has_right_parsed_html(self):
        parsed_html_content = self.get_created_post_parsed_html_attribute()
        converted_html = self.convert_markdown_content_to_html()
        self.assertEqual(parsed_html_content, converted_html)

    def get_created_post_tags_count(self):
        created_post = self.get_created_post()
        return created_post.tags.count()

    def test_create_post_has_right_number_of_tags(self):
        tags_count = self.get_created_post_tags_count()
        self.assertEqual(tags_count, self.number_of_dummy_tags)
