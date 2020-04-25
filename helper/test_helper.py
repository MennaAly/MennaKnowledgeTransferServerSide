import json

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from model_mommy import mommy
from rest_framework.authtoken.models import Token


def reverse_url(url, query_params_dict):
    return reverse(url, kwargs=query_params_dict)


def authorization_setup():
    user = User.objects.create_user(
        username='test',
        email='test@email.com',
        password='test',
    )
    token, created = Token.objects.get_or_create(user=user)
    return Client(HTTP_AUTHORIZATION='Token ' + token.key)


def create_request_body(request_data):
    return json.dumps(request_data)


def create_dummy_instances(model_name, quantity, many_to_many_flag):
    return mommy.make(model_name, _quantity=quantity, make_m2m=many_to_many_flag)


def create_dummy_instance(model_name, many_to_many_flag):
    return mommy.make(model_name, make_m2m=many_to_many_flag)


# def validate_status_code(response, status_code_number):
#     return response.status_code == status_code_number