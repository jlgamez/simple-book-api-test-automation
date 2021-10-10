import requests


def test_get_all_books_status_code_is_200(define_base_url, load_endpoints):
    end_point = define_base_url + load_endpoints.get('booksEndpoint')
    response = requests.get(end_point)
    assert response.status_code == 200


def test_get_all_books_have_defined_keys(define_base_url, load_endpoints):
    end_point = define_base_url + load_endpoints.get('booksEndpoint')
    response_body = requests.get(end_point).json()
    book = response_body[0]
    for key in ['id', 'name', 'type', 'available']:
        assert key in book.keys(), 'The key %s is missing in book data. ' % key + 'Actual data: %s' % book.keys()


def test_get_all_fiction_books(define_base_url, load_endpoints, load_fiction_test_data):
    fiction_param = load_fiction_test_data
    end_point = define_base_url + load_endpoints.get('booksEndpoint') + '?type=' + fiction_param
    response_body = requests.get(end_point).json()
    for book_dict in response_body:
        book_type = book_dict.get('type')
        assert book_type == fiction_param, 'Book type is not ' + fiction_param + '. %s was found' % book_type


def test_get_all_non_fiction_books(define_base_url, load_endpoints, load_non_fiction_test_data):
    non_fiction_param = load_non_fiction_test_data
    end_point = define_base_url + load_endpoints.get('booksEndpoint') + '?type=' + non_fiction_param
    response_body = requests.get(end_point).json()
    for book_dict in response_body:
        book_type = book_dict.get('type')
        assert book_type == non_fiction_param, 'Book type is not ' + non_fiction_param + '. %s was found' % book_type


def test_get_all_books_limit_with_valid_partition(define_base_url, load_endpoints, load_valid_limit_values_partition):
    # limit query parameter should be an int between 1 and 20
    valid_value_partition = load_valid_limit_values_partition
    for val in valid_value_partition:
        end_point = define_base_url + load_endpoints.get('booksEndpoint') + '?limit=' + str(val)
        response = requests.get(end_point)
        response_body = response.json()
        assert response.status_code == 200
        assert len(response_body) <= val, 'Number of books retrieved higher than the limit(%s)' % str(val)


def test_get_all_books_limit_with_invalid_partition(define_base_url, load_endpoints, load_invalid_limit_values_partition):
    invalid_value_partition = load_invalid_limit_values_partition
    for val in invalid_value_partition:
        end_point = define_base_url + load_endpoints.get('booksEndpoint') + '?limit=' + str(val)
        response = requests.get(end_point)
        response_body = response.json()
        assert response.status_code == 400, 'The limit %s did not yield a 400 code' % str(val)
        assert 'error' in list(response_body.keys()), 'error key missing in response data'


def test_get_book_by_id(define_base_url, load_endpoints, load_specific_book_data):
    id = load_specific_book_data[0]
    title = load_specific_book_data[1]
    end_point = define_base_url + load_endpoints.get('booksEndpoint') + str(id)
    response = requests.get(end_point)
    response_body = response.json()
    assert response.status_code == 200
    assert response_body.get('name') == title


