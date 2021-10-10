import requests


def test_new_user_can_login(define_base_url, load_endpoints, load_headers, create_new_usr_data):
    end_point = define_base_url + load_endpoints.get('authenticationEndpoint')
    new_usr_data = create_new_usr_data
    # register the new user in a separate function and assert its creation in this test
    user_creation_response = create_new_user(end_point, new_usr_data, load_headers)
    user_creation_response_body = user_creation_response.json()
    # assert user creation
    assert user_creation_response.status_code == 201, 'Status code is not 201. Instead, %s was returned' % \
                                                      user_creation_response.status_code
    assert 'accessToken' in list(user_creation_response_body.keys()), 'Access token not returned'


def create_new_user(end_point, new_usr_data, headers):
    response = requests.post(url=end_point, data=new_usr_data, headers=headers)
    return response





