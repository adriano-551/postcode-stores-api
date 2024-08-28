import json


def test_get_stores(client, mocker):
    with open('/store-postcodes-api/tests/longlat_response.json') as file:
        postcodes_with_latitude_response = json.load(file)

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = postcodes_with_latitude_response

    mocker.patch('requests.post', return_value=mock_response)

    response = client.get('main/stores')

    assert response.status_code == 200
    assert b"St_Albans" in response.data
    assert b"AL1 2RJ" in response.data
    assert b"Borehamwood" in response.data
    assert b"WD6 4PR" in response.data


def test_stores_failure(client, mocker):
    failure_mock_response = {
        "status": 404
    }

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = failure_mock_response

    mocker.patch('requests.post', return_value=mock_response)

    response = client.get('main/stores')

    assert response.status_code == 404


def test_stores_nearest_happy(client, mocker):
    with open('/store-postcodes-api/tests/outcodes_response.json') as file:
        outcodes_response = json.load(file)

    with open('/store-postcodes-api/tests/lat_response.json') as file:
        lat_response = json.load(file)

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = outcodes_response

    mocker.patch('requests.get', return_value=mock_response)

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = lat_response

    mocker.patch('requests.post', return_value=mock_response)

    response = client.get('api/v1/stores/SW4 8LD/25000')

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['postcode'] == 'SW11 3RX'
    assert response.json[1]['postcode'] == 'SW17 0BW'
