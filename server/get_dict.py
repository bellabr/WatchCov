from typing import Dict
import csv

def load_dict(filename: str) -> Dict:
    """Create a dictionary using <filename> in the format specified:

    Dict['health_region': {'cases', 'latitude', 'longitude'}, ...]

    Where 'cases' refers to the integer number of cases in 'health_region',
    'latitude' refers to the float latitude of 'health_region', and
    'longitude' refers to the float longitude of 'health_region',
    as specified in <filename>.
    """
    d = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['health_region'] not in d:
                    d[row['health_region']] = {'cases': 1, \
                        'latitude': float(row['latitude']), \
                            'longitude': float(row['longitude'])}
                else:
                    d[row['health_region']]['cases'] += 1
            except ValueError:  # no longitude nor latitude
                pass
    return d

def load_dict_by_age(filename: str, age_group: str) -> Dict:
    """Create a dictionary containing only data of the specified age category, <age_group>
    in <filename> in the format specified:

    Dict['health_region': {'cases', 'latitude', 'longitude'}, ...]

    Where 'cases' refers to the integer number of cases in 'health_region',
    'latitude' refers to the float latitude of 'health_region', and
    'longitude' refers to the float longitude of 'health_region',
    as specified in <filename>.

    If <age_group> is not a specified key in <filename>, an empty dictionary is returned.
    """
    d = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['age_group'] == age_group:
                    if row['health_region'] not in d:
                        d[row['health_region']] = {'cases': 1, \
                            'latitude': float(row['latitude']), \
                                'longitude': float(row['longitude'])}
                    else:
                        d[row['health_region']]['cases'] += 1
            except ValueError:  # no longitude nor latitude
                pass
    return d

def load_dict_by_gender(filename: str, gender: str) -> Dict:
    """Create a dictionary containing only data of the specified age category, <gender>
    in <filename> in the format specified:

    Dict['health_region': {'cases', 'latitude', 'longitude'}, ...]

    Where 'cases' refers to the integer number of cases in 'health_region',
    'latitude' refers to the float latitude of 'health_region', and
    'longitude' refers to the float longitude of 'health_region',
    as specified in <filename>.

    If <gender> is not a specified key in <filename>, an empty dictionary is returned.
    """
    d = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['gender'] == gender:
                    if row['health_region'] not in d:
                        d[row['health_region']] = {'cases': 1, \
                            'latitude': float(row['latitude']), \
                                'longitude': float(row['longitude'])}
                    else:
                        d[row['health_region']]['cases'] += 1
            except ValueError:  # no longitude nor latitude
                pass
    return d

if __name__ == '__main__':
    d = load_dict_by_age('server\COVID19_case_details.csv', '80+')
    for key in d:
        print(f'{key}: {d[key]}')