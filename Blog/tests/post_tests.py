from django.test import TestCase

from Blog.models import Post
from MasterData.models import Tag
from helper import authorization_setup, create_dummy_instances, reverse_url, create_request_body, get_response_content, \
    create_dummy_instance
import os
import markdown2


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


class EditPostContent(TestCase):
    url = None
    post = None
    client = None
    response = None
    request_body = None
    new_markdown_content = None

    def read_new_markdown_content(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        post_content_markdown_file = open(os.path.join(THIS_FOLDER, 'post_updated_markdown_content.txt'), 'r')
        return post_content_markdown_file.read()

    def create_post(self):
        return create_dummy_instance(Post, False)

    def create_request_body(self):
        return create_request_body({
            'markdown_content': self.new_markdown_content,
        })

    def initialize_edit_content_setup(self):
        self.read_new_markdown_content()
        self.create_post()
        self.create_request_body()

    def setup_url(self):
        url = reverse_url("post-detail", {'pk': self.post.id})
        url += 'action=save'
        return url

    def submit_edit_post_content_url(self):
        return self.client.put(self.url, self.request_body, content_type="application/json")

    @classmethod
    def setUpClass(cls):
        super(EditPostContent, cls).setUpClass()
        edit_post_content = cls()
        cls.client = authorization_setup()
        cls.new_markdown_content = cls.read_new_markdown_content(edit_post_content)
        cls.post = cls.create_post(edit_post_content)
        cls.request_body = cls.create_request_body(edit_post_content)
        cls.url = cls.setup_url(edit_post_content)
        cls.response = cls.submit_edit_post_content_url(edit_post_content)

    def test_edit_post_content_status(self):
        self.assertEqual(self.response.status_code, 200)

    def get_post_markdown_content(self):
        return Post.objects.filter(id=self.post.pk).first().markdown_content

    def test_post_has_the_edited_markdown_content(self):
        updated_markdown_content = self.get_post_markdown_content()
        self.assertEqual(updated_markdown_content, self.new_markdown_content)

    def get_post_html_content(self):
        return Post.objects.filter(id=self.post.pk).first().parsed_html_content

    def get_new_html_content(self):
        return markdown2.markdown(self.new_markdown_content)

    def test_post_has_the_edited_html_content(self):
        updated_html_content = self.get_post_html_content()
        new_html_content = self.get_new_html_content()
        self.assertEqual(updated_html_content, new_html_content)
