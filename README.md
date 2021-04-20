# WatchCov

## Overview

![Example image](/images/example.png)

WatchCov provides a simple case visualization tool for anyone curious about the distribution of COVID-19 cases in Canada. WatchCov allows users to filter COVID-19 case data by any combination of age range, gender, case report date interval, method of exposure and case status providing useful visuals to represent the data of interest.

This project was submitted to the [BioHacks 2021](https://biohacks-2021.devpost.com/) competition hosted by the University of Toronto Bioinformatics and Computational Biology Student Union. WatchCov finished in [2nd place](https://devpost.com/software/watchcov).

A demo is hosted on [Heroku](https://watch-cov.herokuapp.com) (due to the memory limit of the free Heroku servers, only a subset of the data is visualized).



## Getting Started

Install the requirements and run the server.
```
pip install -r requirements.txt
python3 run.py
```
Note that the dataset is downloaded when the server is started so it may take longer than a typical Flask application.

## Dataset

COVID-19 case details are provided by Ersi Canada. Since the data is compiled from several sources, some cases are missing fields such as gender and case status. Click [here](https://hub.arcgis.com/datasets/4dabb4afab874804ba121536efaaacb4_0) for more details.


## Contributors

* **Christopher Ma**
* **Sunny Xiao**
* **Annabella Bregazzi**
