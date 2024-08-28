from flask import abort
from . import api
from markupsafe import escape
import json
import requests
import re


@api.route('/stores/<string:postcode>/<int:radius>')
def get_nearest_stores(postcode, radius):
    # escaping input to prevent injection attacks
    postcode = escape(postcode)
    radius = escape(radius)

    # Default to 5000 meters radius if not in bounds, api limit is 25000 meters
    radius = radius if 0 < int(radius) <= 25000 else 5000

    # Verify postcode matches according to UK gov postcode regex
    # Sourced from UK GOV Bulk Data Transfer document
    if not bool(re.match(r"^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|" +
                         r"(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9]" +
                         r"[A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) " +
                         r"[0-9][A-Za-z]{2})$", postcode)):
        return abort(400)

    # Get outcode of given postcode and search nearest outcodes
    outcode = postcode.split(" ")[0]

    outcodes_response = requests.get(
        'https://api.postcodes.io/outcodes/' + outcode + '/nearest?limit=100&radius=' + radius
    ).json()

    if outcodes_response['status'] != 200:
        return abort(outcodes_response['status'])

    outcodes_list = []

    for outcode in outcodes_response['result']:
        outcodes_list.append(outcode['outcode'])

    # Same as other endpoint, would want to store this data in DB for easier accessing
    # Search json file for matching outcodes
    with open('/store-postcodes-api/app/static/stores.json') as file:
        stores_data = json.load(file)

    matches = list(filter(lambda store: store['postcode'].split(" ")[0] in outcodes_list, stores_data))

    if len(matches) == 0:
        return 'No stores found for requested postcode in radius'

    pc_list = []

    # Adding all postcodes to list for api request to get get latitude
    for store in matches:
        pc_list.append(store['postcode'])

    longlat_response = requests.post(
        'https://api.postcodes.io/postcodes',
        json={'postcodes': pc_list}
    ).json()

    if longlat_response['status'] != 200:
        return abort(longlat_response['status'])

    stores_obj = []

    for location in longlat_response['result']:
        stores_obj.append(
            {
                'name': location['result']['nuts'],
                'postcode': location['result']['postcode'],
                'longitude': location['result']['longitude'],
                'latitude': location['result']['latitude']
            }
        )

    # Sort matches north to south using latitude
    sorted_stores = sorted(stores_obj, key=lambda store: int(store['latitude']), reverse=True)

    return sorted_stores
