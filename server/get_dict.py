from typing import Dict
from datetime import datetime, date
import csv

def load_dict(filename: str) -> Dict:
    """Create a global dictionary of <filename> containing only values in Canada.
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

def query(ageRange: str = None, gender: str = None, 
startDate: datetime = None, endDate: datetime = None) -> Dict:
    """Create a dictionary using <gd> of the cases that fall into the category <ageRange>, <gender>, 
    <startDate>, <endDate>, if they are not None, in the format specified:

    Dict['health_region': {'cases', 'latitude', 'longitude'}, ...]

    Where 'cases' refers to the integer number of cases in 'health_region',
    'latitude' refers to the float latitude of 'health_region', and
    'longitude' refers to the float longitude of 'health_region'.

    If <ageRange>, <gender>, <startDate>, <endDate>, is None, there is no restriction on that category 
    and so all cases of that category are returned in the dictionary.

    Precondition: 
        - if <startDate> is not None, then <endDate> is not None.
        - if <startDate> and <endDate> are not None, then <startDate> <= <endDate>
    """
    q = {}
    for key in gd:
        if _satisfies_condition(key, ageRange, gender, startDate, endDate):
            if gd[key]['healthRegion'] not in q:
                q[gd[key]['healthRegion']] = {'cases': 1, \
                    'latitude': float(gd[key]['latitude']), \
                        'longitude': float(gd[key]['longitude'])}
            else:
                q[gd[key]['healthRegion']]['cases'] += 1
    return q

def _satisfies_condition(key, ageRange, gender, startDate, endDate) -> bool:
    """A helper function for query
    """
    if ageRange is None or gd[key]['ageRange'] == ageRange:
        if gender is None or gd[key]['gender'] == gender:
            if startDate is None or startDate <= gd[key]['dateReported'] <= endDate:
                return True
    return False

if __name__ == '__main__':
    t = query(gender='Female', ageRange='70-79', startDate=datetime(2020, 3, 11), endDate=datetime(2020, 3, 11))

    for key in t:
        print(f'{key}: {t[key]}')