# Hi

This is a bunch of stuff to compile bike racing results to make announcing easier, so I don't have to click around on a bunch of shit the night before the race.

## racer-history.py

Define:

	- An event URL
	- Maximum predicted placing
	- Maximum historical result placing
	- Results years
	- Field names to ignore (waitlist, tent space, etc)

Writes a .csv of top predicted racers (by field) and their recent results (up to the maximum placing)

## race-count.py

Define:

	- An event URL
	- Field names to ignore (waitlist, tent space, etc)

Writes a .csv of racers who are doing two or more races at the event
