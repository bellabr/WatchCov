from typing import Dict
import csv

def load_dict(filename: str) -> Dict:
    """Create a dictionary
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

if __name__ == '__main__':
    d = load_dict('server\COVID19_case_details.csv')
    for key in d:
            print(f'{key}: {d[key]}')