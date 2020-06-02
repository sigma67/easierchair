### usage

This package consists of a Python 3 script to pull data about a paper list from a conference (as PC chair). 
It pulls information such as abstract, decision etc. from the individual paper pages.

## Setup
Copy settings.ini.example to settings.ini and put in your auth cookie from the browser. 
Additionally, set the conference's id from the submission URL.

Then, run `scrape_easychair.py` to receive a JSON file.