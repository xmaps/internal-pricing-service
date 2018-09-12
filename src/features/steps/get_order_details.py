import json

from behave import then


@then(u'it should contain the order details: content {details_response}')
def it_should_be_the_order_details(context, details_response):
    api_response = json.loads(context.response.content)
    test_response = json.loads(details_response)
    print(api_response)
    print(test_response)
    assert api_response == test_response
