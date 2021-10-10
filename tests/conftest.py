import json
import uuid
import pytest
import requests

from tests.support.load_file import load_data_from_file

config_data = load_data_from_file('tests/config/test_data.json')


@pytest.fixture(scope="session")
def define_base_url():
    return config_data.get('baseUri')


@pytest.fixture(scope="session")
def load_endpoints():
    return config_data.get('endpoints')


@pytest.fixture(scope="session")
def load_headers():
    return config_data.get('generalHeaders')


@pytest.fixture()
def create_new_usr_data():
    new_usr_name = str(uuid.uuid4())
    new_usr_email = new_usr_name + '@example.com'
    new_usr_data = json.dumps({
        'clientName': new_usr_name,
        'clientEmail': new_usr_email
    })
    return new_usr_data


@pytest.fixture()
def load_fiction_test_data():
    return config_data.get('booksRetrievalTestData').get('fictionParameter')


@pytest.fixture()
def load_non_fiction_test_data():
    return config_data.get('booksRetrievalTestData').get('nonFictionParameter')


@pytest.fixture()
def load_valid_limit_values_partition():
    return config_data.get('booksRetrievalTestData').get('validLimitValues')


@pytest.fixture()
def load_invalid_limit_values_partition():
    return config_data.get('booksRetrievalTestData').get('invalidLimitValues')


@pytest.fixture(scope="session")
def load_specific_book_data():
    specific_book = config_data.get('booksRetrievalTestData').get('getBookByIdData')
    book_id = specific_book.get('id')
    book_title = specific_book.get('title')
    return [book_id, book_title]


@pytest.fixture(scope="session")
def load_existing_user_data():
    user_info = config_data.get('userInfo')
    name = user_info.get('clientName')
    email = user_info.get('clientEmail')
    access_token = user_info.get('accessToken')
    updated_client_name = user_info.get('updatedClientName')
    return [name, email, access_token, updated_client_name]


@pytest.fixture(scope="session")
def load_order_ids(define_base_url, load_existing_user_data):
    end_point = define_base_url + '/orders'
    access_token = load_existing_user_data[2]
    headers = {'Authorization': 'Bearer ' + access_token}
    orders = list((requests.get(url=end_point, headers=headers)).json())
    orders_ids = []
    for order in orders:
        orders_ids.append(order.get('id'))
    return orders_ids









