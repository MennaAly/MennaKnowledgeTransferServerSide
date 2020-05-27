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

    def create_dummy_tags(self):
        self.tags = create_dummy_instances(Tag, self.number_of_dummy_tags, False)
        self.tag_ids = [tag.id for tag in self.tags]

    def create_post_request_body(self):
        self.post_request_body = create_request_body({
            'title': 'how to effectively study clean code book',
            'markdown_content': '# 5 Effective Ways to Combat Impostor Syndrome' +
                       '>Have you ever caught yourself in moments of overwhelming self-doubt, feelingincompetent? Do you find yourself attributing your stellar track record to mere chance as opposed to merit, not internalizing your achievements? Do you often dread being ‘found out’ for the fraud you think you are? If you’re perceived by people as a high achiever, yet you see yourself as anything except that, there’s a high chance you may be struggling with impostor syndrome.' +
                       '>Over the years I have struggled with my own share of impostor syndrome. I remember how relieved I was when I found out that the seemingly irrational inner conflict I had has a name! I was even more surprised to learn that many of my acquaintances, people who I consider to be absolute geniuses at their pinnacle of success, are also often blinded by how impressive their skill-set is. For that reason I’d chosen to write about how I navigated my way around impostor syndrome, highlighting what has been working best for me.' +
                       '>**1. Embrace the positive feedback**' +
                       '>We preach not caring what other people think of us, but it’s not always a bad thing when you take in the positive feedback, especially when you know it’s genuine. I used to consider any praise as an added burden of elevated expectations, but by time I realized that people don’t commend you on your potential, rather on what you have showcased. So next time a coworker praises your work, know that you in fact have done a good job.' +
                       '![alternativetext](https://placebear.com/300/300)'
        })

    def setup_url(self):
        self.url = reverse_url("post-list", {})
        self.url += '?action=save'

    def initialize_creation_process_setup(self):
        self.create_dummy_tags()
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
        return Post.objects.latest('id')

    def get_created_post_parsed_html_attribute(self):
        created_post = self.get_created_post()
        return created_post.parsed_html_content

    def convert_markdown_content_to_html(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        post_content_markdown_file = open(os.path.join(THIS_FOLDER, 'post_content_markdown.txt'), 'r')
        post_content_markdown = post_content_markdown_file.read()
        return markdown2.markdown(post_content_markdown)

    def test_create_post_has_right_parsed_html(self):
        parsed_html_content = self.get_created_post_parsed_html_attribute()
        converted_html = self.convert_markdown_content_to_html()
        self.assertEqual(parsed_html_content, converted_html)

    def get_created_post_tags(self):
        created_post = self.get_created_post()
        return created_post.tags

    def test_create_post_has_right_number_of_tags(self):
        tags = self.get_created_post_tags()
        self.assertEqual(len(tags), self.number_of_dummy_tags)
