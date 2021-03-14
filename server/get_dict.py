from typing import Dict
from datetime import datetime
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
    id = 1
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                d[id] = {'latitude': float(row['latitude']), 'longitude': float(row['longitude']), \
                    'healthRegion': row['health_region'], 'ageRange': row['age_group'], 'gender': row['gender'], \
                        'dateReported': datetime.strptime(row['date_reported'][:-3], '%Y/%m/%d %I:%M:%S'), \
                            'exposure': row['exposure'], 'caseStatus': row['case_status'], 'province': row['province']} 
                id += 1
            except ValueError:  # no longitude nor latitude
                pass
    return d

gd = load_dict('server\COVID19_case_details.csv')

def query(ageRange: str = None, gender: str = None) -> Dict:
    """Create a dictionary using <gd> of the cases that fall into the category
    <ageRange> and <gender>, if they are not None, in the format specified:

    Dict['health_region': {'cases', 'latitude', 'longitude'}, ...]

    Where 'cases' refers to the integer number of cases in 'health_region',
    'latitude' refers to the float latitude of 'health_region', and
    'longitude' refers to the float longitude of 'health_region',
    as specified in <filename>.

    If <ageRange> or <gender> is None, there is no restriction on that category
    and so all cases are returned in the dictionary.
    """
    q = {}
    for key in gd:
        if _satisfies_condition(key, ageRange, gender):
            if gd[key]['healthRegion'] not in q:
                q[gd[key]['healthRegion']] = {'cases': 1, \
                    'latitude': float(gd[key]['latitude']), \
                        'longitude': float(gd[key]['longitude'])}
            else:
                q[gd[key]['healthRegion']]['cases'] += 1
    return q

def _satisfies_condition(key, ageRange, gender) -> bool:
    """A helper function for query
    """
    if ageRange is None or gd[key]['ageRange'] == ageRange:
        if gender is None or gd[key]['gender'] == gender:
            return True
    return False

if __name__ == '__main__':
    t = query(gender='Male', ageRange='80+')

    for key in t:
        print(f'{key}: {t[key]}')