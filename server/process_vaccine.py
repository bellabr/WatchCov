from typing import Dict
import csv, datetime, os

def load_vaccine_data(d: dict, filename: str):
    """add total case entry for respective province
    """
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # set the date key as a datetime object
            # currDateTime = datetime.datetime.strptime(currDate, "%Y-%m-%d")
            # row['data » date'] = currDateTime
            province = filename[5:7]
            currDate = row['data » date']
            if currDate not in d:
                d[currDate] = {province : row['data » total_tests']}
            else:
                d[currDate][province] = row['data » total_tests']

def load_vac_folder(dir: str):
    """iterate through the specified folder and convert the vaccine datasets
    """
    d= {}
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            load_vaccine_data(d, file)
    return d



if __name__ == '__main__':
    d = load_vaccine_data('datasets-vaccine/Data-AB.csv')
