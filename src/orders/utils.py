import json
import urlfetch
from memoize import memoize
from rest_framework.views import exception_handler
import time


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status'] = 'error'
        response.data['status_code'] = response.status_code

    return response


@memoize()  # default 300
def get_currency_rate(main_currency, requested_currency):
    """
    Gets the current rate from one currency to the other.
    Documentation: https://www.currencyconverterapi.com/docs
    :param main_currency: The currency of the system. Usually the system is in GBP
    :param requested_currency:
    :return: the current rate
    """

    conversion_key = main_currency + '_' + requested_currency
    url = f'https://free.currencyconverterapi.com/api/v6/convert?' \
          f'q={conversion_key}&compact=ultra'

    rate = None
    for i in range(1, 4):  # retries
        try:
            result = urlfetch.get(url=url, deadline=(5 + i))
            resp = json.loads(result.content)
            rate = resp.get(conversion_key)
            # retry in case of 'Internal Server Error' status code
            if result.status_code == 500:
                time.sleep(1)
                continue
            break
        except urlfetch.UrlfetchException as e:
            print(e)
            time.sleep(1)
            continue

    return rate
