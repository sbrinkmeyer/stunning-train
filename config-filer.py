import yaml
import os

tmdb_info = [
    {
        'default':{
            'api_key':'',
            'video_path':'/home/scottb/Videos'
        }
    }
]


path = os.path.join(os.environ['HOME'], '.tmdb')
os.mkdir(path)

the_file = os.path.join(path, 'config')

with open(the_file, 'w') as yamlfile:
    tmdb_info = yaml.dump(tmdb_info, yamlfile)
    print("wrote")