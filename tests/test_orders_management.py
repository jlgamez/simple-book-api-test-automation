import json
import requests
import random


def test_submit_an_order(define_base_url, load_endpoints, load_headers, load_existing_user_data, load_specific_book_data):
    end_point = define_base_url + load_endpoints.get('ordersEndpoint')
    customer_name = load_existing_user_data[0]
    access_token = load_existing_user_data[2]
    book_id = load_specific_book_data[0]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    body_data = {'bookId': book_id, 'customerName': customer_name}
    body = json.dumps(body_data)
    response = requests.post(url=end_point, data=body, headers=headers)
    status_code = response.status_code
    response_body = response.json()
    assert status_code == 201, 'Order not created. Status response code is %s' % str(status_code)
    assert response_body.get('created') is True, 'Created val id not True. Value: %s' % str(response_body.get('created'))
    assert 'orderId' in list(response_body.keys()), 'orderId is missing in response data'


def test_get_all_orders_made_by_user(define_base_url, load_endpoints, load_headers, load_existing_user_data):
    end_point = define_base_url + load_endpoints.get('ordersEndpoint')
    access_token = load_existing_user_data[2]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    response = requests.get(url=end_point, headers=headers)
    status_code = response.status_code
    response_body = response.json()
    random_order = random.choice(response_body)
    required_order_keys = {'id', 'bookId', 'customerName', 'createdBy', 'quantity', 'timestamp'}
    actual_order_keys = set(random_order.keys())
    assert status_code == 200, 'Status code is %s instead of 200' % status_code
    assert required_order_keys == actual_order_keys, 'Order data does not match the required data. Current elements: %s'\
                                                     % str(list(actual_order_keys))


def test_get_order_by_id(define_base_url, load_endpoints, load_headers, load_order_ids, load_existing_user_data):
    random_order_id = random.choice(load_order_ids)
    end_point = define_base_url + load_endpoints.get('ordersEndpoint') + random_order_id
    access_token = load_existing_user_data[2]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    response = requests.get(url=end_point, headers=headers)
    status_code = response.status_code
    orders = [response.json()]
    required_order_keys = {'id', 'bookId', 'customerName', 'createdBy', 'quantity', 'timestamp'}
    actual_order_keys = set(orders[0].keys())
    assert status_code == 200, 'Status code is %s instead of 200' % str(status_code)
    assert len(orders) == 1, 'Number of orders returned is not 1. Actual number: %s' % str(len(orders))
    assert required_order_keys == actual_order_keys, 'Order data does not match the required data. Current elements: %s'\
                                                     % str(list(actual_order_keys))


def test_no_orders_returned_with_invalid_id(define_base_url, load_endpoints, load_headers, load_existing_user_data):
    invalid_id = 'theresNoWayThisIdExists'
    end_point = define_base_url + load_endpoints.get('ordersEndpoint') + invalid_id
    access_token = load_existing_user_data[2]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    response = requests.get(url=end_point, headers=headers)
    status_code = response.status_code
    response_body = response.json()
    assert status_code == 404, 'Status code is not 404. %s was returned' % status_code
    assert response_body.get('error') == 'No order with id ' + invalid_id + '.', \
        'Error message missing or malformed: %s' % response_body.get('error')


def test_update_an_order(define_base_url, load_endpoints, load_headers, load_order_ids, load_existing_user_data):
    random_order_id = random.choice(load_order_ids)
    end_point = define_base_url + load_endpoints.get('ordersEndpoint') + random_order_id
    access_token = load_existing_user_data[2]
    updated_client_name = load_existing_user_data[3]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    # modify customer name in the order
    body = json.dumps({'customerName': updated_client_name})
    response = requests.patch(url=end_point, headers=headers, data=body)
    status_code = response.status_code
    # get the order updated to check its customer name has changed
    get_order_response = requests.get(url=end_point, headers=headers)
    get_order_body = get_order_response.json()
    assert status_code == 204, 'The order was not modified. Status code: %s' % status_code
    assert get_order_body.get('customerName') == updated_client_name, 'Client name not updated. Expected %s. Current' \
                                                                      'name: %s' % (updated_client_name,
                                                                                    get_order_body.get('customerName'))


def test_delete_order(define_base_url, load_endpoints, load_headers, load_order_ids, load_existing_user_data):
    random_order_id = random.choice(load_order_ids)
    end_point = define_base_url + load_endpoints.get('ordersEndpoint') + random_order_id
    access_token = load_existing_user_data[2]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    response = requests.delete(url=end_point, headers=headers)
    status_code = response.status_code
    assert status_code == 204, 'Order not deleted. Status code: %s' % status_code


def test_delete_non_existing_order(define_base_url, load_endpoints, load_headers, load_existing_user_data):
    invalid_id = 'theresNoWayThisIdExists'
    end_point = define_base_url + load_endpoints.get('ordersEndpoint') + invalid_id
    access_token = load_existing_user_data[2]
    headers = load_headers
    headers.update({'Authorization': 'Bearer ' + access_token})
    print(headers)
    response = requests.delete(url=end_point, headers=headers)
    status_code = response.status_code
    error_message = response.json().get('error')
    assert status_code == 404
    assert error_message == 'No order with id ' + invalid_id + '.', 'Error message missing or malformed: %s' % error_message

