# MovieListfromWiki
Goal:  Create a service to pull movie metadata into data store (in the form of a load ready file). The source of metadata considered here is  Wikidata
For each movie, following dimensions are provided:
● title
● genre(s)
● main subject(s) ● actor(s)
Code file name:  python movies_from_wikibase.py

Solution:  Written in Python3.6 using wikipedia-api. Wikipedia-api is a Python library that makes it easy to access and parse data from Wikidata. In-order to run the code user need to download
‘pip install wikipedia-api’

Code is divided into 2 parts:

Part 1 generates list of movies + ‘pageid’ based on ‘Category’
Code uses “Category” function from the API to get all the Movies by selecting “Category:films by year”. Category can be changed based on requirement. Part 1 typically runs within 10-15 mins and lists all movies with ‘pageid’. The output is saved as ‘wikibase_movie_pageid.csv’.
With this category, code generates ~180K movies.

Part 2 takes output from Part 1 ie list of all movies with ‘pageid’ and generates ‘metadata’ for it.
The ‘pageid’ of each movie is used as source to derive wikidata ‘wikibase item id’. Following function is used for same: “https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&pageids=<>” The ‘wikibase item ids’ then provides look up for ‘metadata ids’ using following function: ‘https://www.wikidata.org/wiki/Special:EntityData/<>.json'
The ‘metadata ie genre, main subject, actor(s) ’ then is derived from ‘metadata ids’.
Final output is movie tile along with respective ‘metadata’.
The code is currently running on local machine and can be parallelized as next step.

Alternate approaches:
1. Part 1 code is currently is used to get movie (by year) + pageid. It can also be used to get genre, actor(s), main subject and other such metadata information as well. This can then be joined with movie data at the end.
2. Additionally I played around with SPARQL towards the end but didn’t get around time to put the code together.
References:   https://pypi.python.org/pypi/Wikipedia-API
