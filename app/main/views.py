from . import main
from flask import render_template, abort
import json
import requests


@main.route('/stores')
def stores():
    # Likely want to store this data in a database in a real world scenario
    with open('/store-postcodes-api/app/static/stores.json') as file:
        stores_data = json.load(file)

    sort_stores = sorted(stores_data, key=lambda store: store['name'])

    pc_list = []
    pc_indexes = {}

    # Adding all postcodes to list for api request
    # also adding postcodes to dict to help editing later
    for store in sort_stores:
        pc_indexes[store['postcode']] = sort_stores.index(store)
        pc_list.append(store['postcode'])

    longlat_response = requests.post(
        'https://api.postcodes.io/postcodes',
        json={'postcodes': pc_list}
    ).json()

    if longlat_response['status'] != 200:
        return abort(longlat_response['status'])

    for pc in longlat_response['result']:
        # postcodes.io can return null results for the endpoint response

        if pc['result'] is not None:
            sort_stores[pc_indexes[pc['query']]]['longitude'] = pc['result']['longitude']
            sort_stores[pc_indexes[pc['query']]]['latitude'] = pc['result']['latitude']
        else:
            # giving these N/A placeholders for now
            sort_stores[pc_indexes[pc['query']]]['longitude'] = "N/A"
            sort_stores[pc_indexes[pc['query']]]['latitude'] = "N/A"

    return render_template('stores.html', stores=sort_stores)
