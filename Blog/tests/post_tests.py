import json
from datetime import datetime

from django.test import TestCase, Client
from model_mommy import mommy

from Blog.models import Post
from Blog.serializers import PostWithTagsSerializer
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


class EditPostContentTest(TestCase):
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
            'title': self.post.title,
            'markdown_content': self.new_markdown_content,
            'created_date': '2008-10-25',
        })

    def initialize_edit_content_setup(self):
        self.read_new_markdown_content()
        self.create_post()
        self.create_request_body()

    def setup_url(self):
        url = reverse_url("post-detail", {'pk': self.post.id})
        url += '?action=save'
        return url

    def submit_edit_post_content_url(self):
        return self.client.put(self.url, self.request_body, content_type="application/json")

    @classmethod
    def setUpClass(cls):
        super(EditPostContentTest, cls).setUpClass()
        edit_post_content = cls()
        cls.client = authorization_setup()
        cls.new_markdown_content = cls.read_new_markdown_content(edit_post_content)
        cls.post = cls.create_post(edit_post_content)
        cls.request_body = cls.create_request_body(edit_post_content)
        cls.url = cls.setup_url(edit_post_content)
        cls.response = cls.submit_edit_post_content_url(edit_post_content)

    def test_edit_post_content_status(self):
        self.assertEqual(self.response.status_code, 200)

    # def get_post_markdown_content(self):
    #     return Post.objects.filter(id=self.post.pk).first().markdown_content
    #
    # def test_post_has_the_edited_markdown_content(self):
    #     updated_markdown_content = self.get_post_markdown_content()
    #     self.assertEqual(updated_markdown_content, self.new_markdown_content)

    def get_post_html_content(self):
        return Post.objects.filter(id=self.post.pk).first().parsed_html_content

    def get_new_html_content(self):
        return markdown2.markdown(self.new_markdown_content)

    def test_post_has_the_edited_html_content(self):
        updated_html_content = self.get_post_html_content()
        new_html_content = self.get_new_html_content()
        self.assertEqual(updated_html_content, new_html_content)


class EditPostTagsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(EditPostTagsTest, cls).setUpClass()
        edit_post_tags = cls()
        cls.client = authorization_setup()
        cls.post = cls.create_post(edit_post_tags)
        cls.post = cls.associate_post_with_tags(edit_post_tags)
        cls.url = cls.setup_url(edit_post_tags)
        cls.request_body_content = cls.create_request_body(edit_post_tags)
        cls.response = cls.submit_url(edit_post_tags)

    def create_post(self):
        return create_dummy_instance(Post, False)

    def associate_post_with_tags(self):
        tags = create_dummy_instances(Tag, 3, False)
        self.post.tags.add(*tags)
        return self.post

    def setup_url(self):
        return reverse_url("update_post_tags", {})

    def create_request_body(self):
        return create_request_body({
            'id': self.post.id,
            'tag_ids': self.get_new_tags_ids()
        })

    def get_new_tags_ids(self):
        new_tags = create_dummy_instances(Tag, 3, False)
        return [tag.id for tag in new_tags]

    def submit_url(self):
        return self.client.put(self.url, self.request_body_content, content_type="application/json")

    def test_edit_post_tags_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_post_has_right_number_of_tags(self):
        tags_count = self.get_post_tags_count()
        self.assertEqual(tags_count, 6)

    def get_post_tags_count(self):
        return Post.objects.filter(id=self.post.id).first().tags.count()


class RetrievePostsDescendinglyByDateTest(TestCase):
    url = None
    tags = None
    posts = []
    client = None
    response = None
    post_2019 = None
    post_2020 = None
    post_2021 = None

    @classmethod
    def setUpClass(cls):
        super(RetrievePostsDescendinglyByDateTest, cls).setUpClass()
        cls.client = Client()
        retrieve_posts = cls()
        cls.post_2019, cls.post_2020, cls.post_2021 = cls.create_posts(retrieve_posts)
        cls.tags = cls.create_tags(retrieve_posts)
        cls.post_2019, cls.post_2020, cls.post_2021 = cls.associate_posts_with_tags(retrieve_posts)
        cls.posts = cls.save_posts_in_list_in_desc_order(retrieve_posts)
        cls.url = cls.setup_url(retrieve_posts)
        cls.response = cls.submit_url(retrieve_posts)

    def create_posts(self):
        post_2019 = mommy.make(Post, created_date=datetime(2019, 6, 1).date(), make_m2m=True)
        post_2020 = mommy.make(Post, created_date=datetime(2020, 6, 1).date(), make_m2m=True)
        post_2021 = mommy.make(Post, created_date=datetime(2021, 6, 1).date(), make_m2m=True)
        return post_2019, post_2020, post_2021

    def create_tags(self):
        return create_dummy_instances(Tag, 3, False)

    def associate_posts_with_tags(self):
        self.post_2019.tags.add(*self.tags)
        self.post_2020.tags.add(*self.tags)
        self.post_2021.tags.add(*self.tags)
        return self.post_2019, self.post_2020, self.post_2021

    def save_posts_in_list_in_desc_order(self):
        return [self.post_2021, self.post_2020, self.post_2019]

    def setup_url(self):
        url = reverse_url("post-list", {})
        url += "?action=retrieve&ordering=-created_date"
        return url

    def submit_url(self):
        return self.client.get(self.url)

    def test_retrieve_posts_status(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_data_in_desc_order(self):
        response_content = self.get_response_content()
        serialized_posts = self.serialize_post_list()
        self.assertEqual(response_content, serialized_posts)

    def get_response_content(self):
        return json.loads(self.response.content)

    def serialize_post_list(self):
        return PostWithTagsSerializer(self.posts, many=True).data


class FilterPostsByTags(TestCase):
    url = None
    tags = []
    posts = []
    client = None
    response = None

    def create_posts(self):
        return mommy.make(Post, 3)

    def create_tags(self):
        software_engineer_tag = mommy.make(Tag, name='swe')
        backend_tag = mommy.make(Tag, name='BE')
        return [software_engineer_tag, backend_tag]

    def associate_posts_to_tags(self):
        self.add_tag_to_post(self.posts[0], self.tags[0])
        self.add_tag_to_post(self.posts[1], self.tags[0])
        self.add_tag_to_post(self.posts[0], self.tags[1])
        self.add_tag_to_post(self.posts[2], self.tags[1])
        return self.posts

    def add_tag_to_post(self, post, tag):
        post.tags.add(tag)

    def setup_url(self):
        url = reverse_url("post-list", {})
        url += "?action=retrieve&tags__name=" + self.tags[0].name
        return url

    def submit_url(self):
        return self.client.get(self.url)

    def get_response_content(self):
        return json.loads(self.response.content)

    @classmethod
    def setUpClass(cls):
        super(FilterPostsByTags, cls).setUpClass()
        filter_posts_by_tags = cls()
        cls.client = Client()
        cls.posts = cls.create_posts(filter_posts_by_tags)
        cls.tags = cls.create_tags(filter_posts_by_tags)
        cls.posts = cls.associate_posts_to_tags(filter_posts_by_tags)
        cls.url = cls.setup_url(filter_posts_by_tags)
        cls.response = cls.submit_url(filter_posts_by_tags)
        cls.response_content = cls.get_response_content(filter_posts_by_tags)

    def test_filter_tags_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_has_right_count_of_tags(self):
        self.assertEqual(len(self.response_content), 2)

    def test_response_returned_right_tags(self):
        self.assertEqual(self.response_content[0]['title'], self.posts[0].title)
        self.assertEqual(self.response_content[1]['title'], self.posts[1].title)
