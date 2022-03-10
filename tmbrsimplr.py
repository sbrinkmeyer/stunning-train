#!/usr/bin/env python3
from ast import parse
import tmdbsimple as tmdb
import datetime
import argparse
import os
from pathlib import Path


parser = argparse.ArgumentParser(description="make a plex compatible folder name for movies or tv shows")
parser.add_argument("-q", "--query", help="what to search for")
args = parser.parse_args()
if args.query:
    query_string = args.query
else:
    query_string = input('Query String: ')
    

tmdb.API_KEY ='fdb3ac55490a1827c64d9abe1b9c9fd0'
search = tmdb.Search()
responses = search.tv(query=query_string)
name_dict = dict()

#for show in search.results:
for bob in range(0, len(search.results)):
    show = search.results[bob]
    try:
        show_year = str(datetime.datetime.fromisoformat(show['first_air_date']).year)
    except:
        print("something went wrong: ")
        show_year = str(1970)
    
    show_text = "{} ({}) {{tmdb-{}}}".format( show['name'], show_year, show['id'])
    #    print( "{}) {}".format(bob+1, show_text.replace(':','').replace('\'','') ))
    clean_show_text= show_text.replace(':','').replace('\'','').replace('?','')
    print( clean_show_text )
    name_dict[str(show['id'])]=clean_show_text

for show_id, show_naming in name_dict.items():
    print(show_id, " : ", show_naming)

item_index = input('which name number?: ')
print( name_dict[item_index])
tmdb_tv=tmdb.TV(item_index)
response = tmdb_tv.info()
# pretty = json.dumps(response, indent=4)
# print (pretty)
# print(response['number_of_seasons'])
episode_list=list()
for season_count in range(1, response['number_of_seasons'] + 1):
    season_info = tmdb.TV_Seasons(item_index, season_count).info()
    for episode in season_info.get('episodes'):
        episode_year = str(datetime.datetime.fromisoformat(episode['air_date'] or show['first_air_date']).year) 
        episode_name_text = "{} ({}) - s{:02n}e{:02n} - {}".format(response['name'], episode_year, season_count, \
            episode['episode_number'], episode['name'])
        episode_clean_name=episode_name_text.replace(':','').replace('\'','').replace('?','')
        #print(episode_clean_name)
        episode_list.append(episode_clean_name)


parent_dir="/home/scottb/Videos"
path = os.path.join(parent_dir, name_dict[item_index])
os.mkdir(path)
for episode_item in episode_list:
    the_file = os.path.join(path, episode_item)
    os.mknod(the_file)
