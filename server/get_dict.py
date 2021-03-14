from typing import Dict
from datetime import datetime
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

def query(ageRange: str = None, gender: str = None, \
    startDate: datetime = None, endDate: datetime = None, \
        exposure: str = None, caseStatus: str = None) -> Dict:
    """Create a dictionary using <gd> of the cases that fall into the category <ageRange>, <gender>, 
    <startDate>, <endDate>, <exposure>, <caseStatus> if they are not None, in the format specified:

    Dict['health_region': {'cases', 'latitude', 'longitude'}, ...]

    Where 'cases' refers to the integer number of cases in 'health_region',
    'latitude' refers to the float latitude of 'health_region', and
    'longitude' refers to the float longitude of 'health_region'.

    If <ageRange>, <gender>, <startDate>, <endDate>, <exposure>, <caseStatus> is None, 
    there is no restriction on that category and so all cases of that category are returned 
    in the dictionary.

    Precondition: 
        - if <startDate> is not None, then <endDate> is not None.
        - if <startDate> and <endDate> are not None, then <startDate> <= <endDate>
    """
    q = {}
    for key in gd:
        if _satisfies_condition(key, ageRange, gender, startDate, endDate, exposure, caseStatus):
            if gd[key]['healthRegion'] not in q:
                q[gd[key]['healthRegion']] = {'cases': 1, \
                    'latitude': float(gd[key]['latitude']), \
                        'longitude': float(gd[key]['longitude'])}
            else:
                q[gd[key]['healthRegion']]['cases'] += 1
    return q

def _satisfies_condition(key, ageRange, gender, startDate, endDate, exposure, caseStatus) -> bool:
    """A helper function for query

    Maps <ageRange> from "A" -> '<20', "B" -> '20-29', ...
    """
    if ageRange is not None:
        agesMap = {"A": '<20', "B": '20-29', "C": '30-39', "D": '40-49', \
        "E": '50-59', "F": '60-69', "G": '70-79', "H": '80+'}
        ageRange = agesMap[ageRange]
    
    if ageRange is None or gd[key]['ageRange'] == ageRange:
        if gender is None or gd[key]['gender'] == gender:
            if startDate is None or startDate <= gd[key]['dateReported'] <= endDate:
                if exposure is None or gd[key]['exposure'] == exposure:
                    if caseStatus is None or gd[key]['caseStatus'] == caseStatus:
                        return True
    return False

if __name__ == '__main__':
    t = query(gender='Female', ageRange="A", startDate=datetime(2020, 4, 8), endDate=datetime(2020, 4, 26), \
        caseStatus='Recovered', exposure='Travel-Related')

    for key in t:
        print(f'{key}: {t[key]}')

    # print(_satisfies_condition(3, "D", 'Female', datetime(2020, 5, 4), datetime(2020, 5, 5)))