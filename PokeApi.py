import requests
import urllib.request
import random 

from PIL import Image

url = "https://pokeapi.co/api/v2/pokemon"

class Pokemon:
    def __init__(self,id):
        Response = requests.get(f'{url}/{id}')
        if Response.status_code != 200:
            print(f"No pokemon found (ERROR: {Response.status_code})")
            return
        Data = Response.json()
        self.name = Data['name']
        self.weight = Data['weight'] * 0.1
        self.height = Data['height'] * 0.1
        self.img = Data['sprites']['other']['official-artwork']['front_default']

        self.debut = Data['game_indices'][0]['version']['name']
        self.encounter = []

        self.abilities = []
        for x in Data['abilities']:
            self.abilities.append(x['ability']['name'])
        
        self.types = []
        for x in Data['types']:
            self.types.append(x['type']['name'])
        
        self.stats = []
        for x in Data['stats']:
            self.stats.append(f'{x['stat']['name']} : {x['base_stat']}')

        Response = requests.get(f'{url}-species/{self.name}')
        if Response.status_code != 200: #additonal data in species 
            print("Unable to retrieve species data")
            self.egggroups = []
            self.shape = "friend"
        else:
            SpecData = Response.json()
            self.egggroups = []
            for x in SpecData['egg_groups']:
                self.egggroups.append(x['name'])
            self.shape = SpecData['shape']['name']


DexId = random.randint(1,151)
Mon = Pokemon(387)
#urllib.request.urlretrieve(Mon.img,f'{Mon.name}.png')
#img = Image.open(f'{Mon.name}.png')
#img.show()
print(f'This pokemon first appeared in : Pokemon {Mon.debut}')
print(f'It is {Mon.shape} shaped')
StatNames = []
StatVals = []
for x in Mon.stats:
    #print(x)
    stats = x.split(':')
    StatNames.append(stats[0])
    StatVals.append(int(stats[1]))
print(f'Its highest stat is {StatNames[StatVals.index(max(StatVals))]}')
print(f'Its lowest stat is {StatNames[StatVals.index(min(StatVals))]}')
print(f'It is {round(Mon.height,1)}m ({round(Mon.height*3.281,1)}ft) tall and weighs {round(Mon.weight,1)}kg ({round(Mon.weight*2.2046,1)}lbs)')
if len(Mon.abilities) > 1:
    print(f'It has the following abilities:')
    for x in Mon.abilities:
        print(x)
else:
    print(f'It has the {Mon.abilities[0]} ability')
print(Mon.name)