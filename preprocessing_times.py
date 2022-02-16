import json
import pandas as pd

OUTFILE = 'data/Times_geocoding_output.csv'

geo_keys = ['formatted_address',
            'location_type',
            'country',
            'country_short',
            'admin_1',
            'admin_2',
            'locality',
            'colloquial_area',
            'continent',
            'natural_feature',
            'point_of_interest',
            'lat',
            'lon',
            'partial',
            ]


def output_geo_data():
    with open('data/Times1945-1954GPEs_geocoded_complete.json') as f:
        data = json.load(f)
    for i, d in enumerate(data.keys()):
        if i == 0:
            first_doc = True
        formatted = format_geo_info(d, data[d])
        formatted['location'] = d
        output = pd.DataFrame({f: [formatted[f]] for f in formatted.keys()})
        output.to_csv(OUTFILE, mode='a', header=first_doc, index=False)
        first_doc = False


def format_geo_info(place, row):
    """ Adapting code from iPython notebook from ChronicItaly data """
    result = {key: None for key in geo_keys}

    try:
        data = row['raw']
        result['formatted_address'] = data.get('formatted_address')
        result['location_type'] = "+".join(data['types'])
        result['lat'] = data['geometry']['location']['lat']
        result['lon'] = data['geometry']['location']['lng']
        try:
            result['partial'] = result['partial_match']
        except:
            pass
    except:
        print("Problem with geocoding %s" % (place))
        return {}

    try:
        for address in data['address_components']:
            comp_type = address['types'][0]  # first types
            if comp_type == 'locality':
                result['locality'] = address['long_name']
            if comp_type == 'country':
                result['country'] = address['long_name']
                result['country_short'] = address['short_name']
            if comp_type == 'administrative_area_level_1':
                result['admin_1'] = address['long_name']
            if comp_type == 'administrative_area_level_2':
                result['admin_2'] = address['long_name']
            if comp_type == 'colloquial_area':
                result['colloquial_area'] = address['long_name']
            if comp_type == 'natural_feature':
                result['natural_feature'] = address['long_name']
            if comp_type == 'point_of_interest':
                result['point_of_interest'] = address['long_name']
            if comp_type == 'continent':
                result['continent'] = address['long_name']
    except:
        return {}

    return result
