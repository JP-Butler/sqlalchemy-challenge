# sqlalchemy-challenge Module 10
------------------------------------------------------

## Honolulu, Hawaii Vacation Analysis
This challenge used the sql-alchemy concepts learned in Module 10 - Advanced SQL of the Carelton Data Analytics Boot Camp such as creating classes, ORMs, Flask routes and APIs to name a few. Putting these new skills to the test I performed a climate analysis on my desired vacation destination, Honolulu, Hawaii!

## Table of Contents

- [About](#about)
- [Getting Started & Installing](#getting-started--installing)
- [Usage](#usage)
- [Contributing](#contributing)

## About 
As the description above stated, to complete my analysis and make sure I familiarized myself with the climate I performed a thorough analysis of the temperature observation (tobs), precipitation (prcp) and weather station data housed in the sqlite database ***hawaii.sqlite***. In the first portion of the challenge I used functions such as create_engine() and automap_base() to connect to the database and automatically reflect the tables in the database into classes for easy querying later on. A session was then created to query the data, queries such as filtering for data such of the the prcp values for the previous 12 months. Familiar ***Python*** libraries such as pandas and matplotlib were then used to display statistics and visuals like a summary statistics table (using the .describe() function) and a histogram (pd plot method). <br>  
In the second portion, I designed a Climate App in ***Flask API*** format with various routes that can return requested data when accessing the given route in the URL bar. Several static routes were created to return information such as a JSON list of the different stations in the database along with their information. Two dynamic routes were designed to take input from the api user. For e.g. when a start date (in "%m%d%Y" format) was given the min, max and avg of tobs data greater than & equal to that date was provided. The second route accepts a start & end date and provides the same min, max & avg for the tobs date between and including those dates.

## Getting Started & Installing
See [Usage](#usage) for installing guide/links.
The following are needed to run script successfully:  
1. virtual development environment running Python version 3 
2. Python Libraries:
    * matplotlib
    * numpy
    * sqlalchemy
    * datetime
    * flask 
3.**NOTE** verify you are in the folder that contains the app.py file before running. The terminal will likey render an error otherwise, and flask link (http://127.0.0.1:5000) will be inacessible.

## Usage
1. Download and install Anaconda for Python 3.[Download Anaconda](https://www.anaconda.com/distribution/#windows)
2. Most Python libraries should be installed once the Anaconda download is complete. To verify library packages, run the following in the ***Anaconda Prompt***:
```

conda list
```

## Contributing
Justin Butler