# Hi

This is some stuff to compile bike racing results to make announcing easier, so I don't have to click around on a bunch of shit the night before the race.

Requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## racer-history.py

Writes CSVs of top predicted racers (by field) and their recent results (up to the maximum placing).

CSVs are written to a script-level folder called "output".

Directory is not cleared by this script, so you'll have to do that manually.

Arguments:
- `--event_id` (requird): BikeReg event ID. 
- `--years` (required): comma separated list of years to include in results. eg, 2017,2018
- `--type` (required): type of event. `road` or `cross`. Required to get results from the correct site and handle some formatting differences.
- `--predictor_depth` (optional): 0-indexed depth of the predicted riders to get info on. So, `9` would return the top 10 predicted finishers. Defaults to 9.
- `--results_depth` (optional): 0-indexed depth of results to capture. Defaults to 4.
