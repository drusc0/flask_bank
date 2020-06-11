import json


def test_home_page(test_client):
    response = test_client.get('/')
    assert (response.status_code == 200)


def test_get_accounts(test_client, init_db):
    response = test_client.get('/accounts')
    json_data = json.loads(response.data)
    assert (response.status_code == 200)
    assert ('account_test' in json_data[0]['account_num'])
    assert (json_data[0]['frozen'] == False)
    assert (json_data[0]['balance'] == 20.0)


def test_get_transactions(test_client, init_db):
    response = test_client.get('/transactions')
    json_data = json.loads(response.data)
    assert (response.status_code == 200)
    assert (len(json_data) == 0)
