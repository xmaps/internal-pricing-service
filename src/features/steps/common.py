import json

from behave import when, given, then
from rest_framework.test import APIClient

from factories.products import StandardVatBandFactory, ZeroVatBandFactory


@given('the system contains pricing data')
def create_data(context):
    standard_rate = StandardVatBandFactory()
    standard_rate.save()
    zero_rate = ZeroVatBandFactory()
    zero_rate.save()


@when(u'I make a post request to "{url}" with {data}')
def visit(context, url, data):
    client = APIClient()
    context.response = client.post(url, data, format='json')


@then(u'it should return response an OK status code')
def it_should_be_the_correct_status_code(context):
    assert context.response.status_code == 200


@then(u'it should return an error status code {status_code}')
def it_should_be_the_correct_status_code(context, status_code):
    assert context.response.status_code == int(status_code)


@then(u'it should return an informative error message {error_response}')
def it_should_be_an_informative_error(context, error_response):
    api_response = json.loads(context.response.content)
    test_response = json.loads(error_response)
    assert api_response == test_response
