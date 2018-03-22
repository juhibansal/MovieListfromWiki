# Code to get Wikidata for movie with some properties

from __future__ import print_function

import sys
from operator import add
import datetime
import re
import os
from os.path import isfile,isdir
from pprint import pformat
from sys import argv, exit
from glob import glob
import numpy as np
import pandas as pd
import itertools
import os
import subprocess
import urllib, json
import urllib.request
import requests
import wikipedia
import wikipediaapi
import wptools
import pprint

###########------------#################
if __name__ == "__main__":

#Function to get movie data by catagories using wikkipediaapi module; search 2 levels
    def print_categorymembers(categorymembers, level=0, max_level=2):
        for c in categorymembers.values():
            if not re.search(r'^category',(c.title).lower()):
                fname.write("%s,%s\n"%(c.pageid,c.title))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level <= max_level:
                print_categorymembers(c.categorymembers, level + 1)

#function to get title of metadata from the property id found for movie
    def movie_properties(property_code,moviedict,movieid):
        code_title = []
        #dictionary from https://www.wikidata.org/wiki/Special:EntityData/<>.json
        if property_code in moviedict["entities"][movieid]["claims"]:
            for i in range(len(moviedict["entities"][movieid]["claims"][property_code])) :
                try:
                    codeid = (moviedict["entities"][movieid]["claims"][property_code][i]["mainsnak"]["datavalue"]["value"]["id"])
                except KeyError:continue
                with urllib.request.urlopen('https://www.wikidata.org/w/api.php?action=wbgetentities&ids=%s&format=json&languages=en'%codeid) as url1:s1 = json.load(url1)
                try:
                    code_title.append(s1["entities"][codeid]["labels"]["en"]["value"])
                except KeyError:continue
        return code_title

    wiki_wiki = wikipediaapi.Wikipedia('en')
#Save movie title with pageid in a file
    fname = open('movie_pageid.csv','w')

# Select films by year CATEGORY (Can choose any category)
    cat = wiki_wiki.page("Category:films by year")
    print("Category members: Category:Film")
    print_categorymembers(cat.categorymembers)

    fname.close()

    f = open('wikibase_movie_metadata.csv','w')
    fname2 = open('movie_pageid.csv','r')
    property_arr = ["P136","P161","P921"]

# Read Movie file and get metadata for all the Movies (look up by pageid)
    for line in fname2:
        line_elems = line.strip().split(',')
        title_list = []
        #convert pageid for movie to id for easy look up
        with urllib.request.urlopen('https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&pageids=%s'%line_elems[0]) as url: s = json.load(url)
        #print(json.dumps(s, indent=4, sort_keys=True))
        pageidstring =str(line_elems[0])
        try:movieid = str(s["query"]["pages"][pageidstring]["pageprops"]["wikibase_item"])
        except KeyError:continue
        #write movie title
        f.write("%s," % str(line_elems[1]))
        #from movie id get meta data of interest loop over the propery
        with urllib.request.urlopen('https://www.wikidata.org/wiki/Special:EntityData/%s.json'%movieid) as murl: sm = json.load(murl)
        for property_code in property_arr:
            title_list = movie_properties(property_code,sm,movieid)
            f.write("|".join(title_list))
            if not property_code == property_arr[len(property_arr)-1]:f.write(",")

        f.write("\n")
