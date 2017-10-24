# Hi

This is some stuff to compile bike racing results to make announcing easier, so I don't have to click around on a bunch of shit the night before the race.

Requires [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## racer-history.py

Define:
- An event URL
- Maximum predicted placing
- Maximum historical result placing
- Results years
- Field names to ignore (waitlist, tent space, etc)

Writes a .csv of top predicted racers (by field) and their recent results (up to the maximum placing)

## splitStartList.py

For the file created by `racer-history.py` (which is named `start-list.csv`), create individual files per field and put them in an `output` folder.