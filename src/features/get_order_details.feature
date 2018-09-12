Feature: Get Order Details
    As a user of the system I want to get the order details for the order
    i requested.

    Scenario Outline: Access order details

        Given the system contains pricing data
        When I make a post request to "<url>" with <request_data>
        Then it should return response an OK status code
        And it should contain the order details: content <details_response>

    Examples: First Order
       | url |  request_data   | details_response |
       | /orders/price/   | {"order": {"id": 12345, "customer": {}, "items": [{"product_id": 101, "quantity": 1}, {"product_id": 102, "quantity": 5}, {"product_id": 103, "quantity": 1}]}} | {"id": 12345, "items": [{"id": 1, "quantity": 1, "price": 599, "vat": 0.2}, {"id": 3, "quantity": 5, "price": 250, "vat": 0.0}, {"id": 4, "quantity": 1, "price": 250, "vat": 0.0}], "total_price": 2219, "total_vat": 120, "customer": {}} |
       | /orders/price/   | {"order": {"id": 1234, "currency": "BZD", "customer": {}, "items": [{"product_id": 101, "quantity": 1}, {"product_id": 102, "quantity": 5}, {"product_id": 103, "quantity": 1}]}} | {"id": 1234, "items": [{"id": 6, "quantity": 1, "price": 599, "vat": 0.2},{"id": 8, "quantity": 5, "price": 250, "vat": 0.0}, {"id": 9, "quantity": 1, "price": 250, "vat": 0.0}], "currency": "BZD", "total_price": 5797, "total_vat": 313, "customer": {}} |


    Scenario Outline: Get informative error messages

        Given the system contains pricing data
        When I make a post request to "<url>" with <request_data>
        Then it should return an error status code <status_code>
        And it should return an informative error message <error_response>

    Examples: Wrong format on request
       | url  | request_data  | status_code | error_response |
       | /orders/price/ | {} | 400 | {"detail": "Request does not contain the required information. Send an order id and some items in the order.", "status": "error", "status_code": 400} |

    Examples: Wrong product id format
       | url  | request_data   | status_code | error_response |
       | /orders/price/ | {"order": {"id": 9554, "customer": {}, "items": [{}, {}, {}]}} | 400 | {"detail": "Each item in the request needs to have a `product_id` and a `quantity`", "status": "error", "status_code": 400} |
       | /orders/price/ | {"order": {"id": 9658, "customer": {}, "items": [{"product_id": "aaa", "quantity": "zzz"}]}} | 400 | {"detail": "Product id and quantity of items need to be numbers", "status": "error", "status_code": 400} |

    Examples: No product id for request
       | url  | request_data  | status_code | error_response |
       | /orders/price/ | {"order": {"id": 3456, "customer": {}, "items": [{"product_id": 10, "quantity": 10}]}} | 404 | {"detail": "Please check if the product id 10 is in the system", "status": "error", "status_code": 404} |
