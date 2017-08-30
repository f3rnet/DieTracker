README

The D&D Dice Tracker is a python application that tracks dice rolls and plots them on a graph.

To use this application, you will need six tables in a postgres database. It may work with other databases. But no promises - it was only tested with postgres. You will also need plotly, psycopg2, radar, datetime, and random.

It is optimized for Python3. 

This code can easily be modified to accomodate a single die, or as many as you'd like to track. Included is a function that will generate test data for you to experiment with.

To begin:
1. Spin up a database named "dnd". 
2. Run dietrack.py.
3. Select Manual or Auto depending on your use case.
4. That's it!

Best of luck on your adventures,

f3rnet 
August, 2017