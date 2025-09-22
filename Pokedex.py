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
        try:
            self.shinyimg = Data['sprites']['other']['official-artwork']['front_shiny']
        except:
            self.shinyimg = "NA"

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
            self.color = SpecData['color']['name']
            self.evochain = SpecData['evolution_chain']['url']
            for x in SpecData['flavor_text_entries']:
                if x['language']['name'] == 'en':
                    self.entry = x['flavor_text']
                    break #grabs first english entry

def Guess_Prompt(Mon=Pokemon,Level = 0):
    if Level == 0:
        print(f'This pokemon first appeared in : Pokemon {Mon.debut}')
        print(f'It is {Mon.shape} shaped and coloured {Mon.color}')
    if Level == 1:
        StatNames = []
        StatVals = []
        for x in Mon.stats:
            #print(x)
            stats = x.split(':')
            StatNames.append(stats[0])
            StatVals.append(int(stats[1]))
        print(f'Its highest stat is {StatNames[StatVals.index(max(StatVals))]}')
        print(f'Its lowest stat is {StatNames[StatVals.index(min(StatVals))]}')
    if Level == 2:
        print(f'It is {round(Mon.height,1)}m ({round(Mon.height*3.281,1)}ft) tall and weighs {round(Mon.weight,1)}kg ({round(Mon.weight*2.2046,1)}lbs)')
        if len(Mon.egggroups) > 1:
            print(f'It is a member of the following egg groups :')
            for x in Mon.egggroups:
                print(x)
        else:
            print(f'It is a member of the {Mon.egggroups[0]} egg group')
    if Level == 3:
        if len(Mon.abilities) > 1:
            print(f'It has the following abilities:')
            for x in Mon.abilities:
                print(x)
        else:
            print(f'It has the {Mon.abilities[0]} ability')
    if Level == 4:
        CensorEntry = Mon.entry.lower().replace(Mon.name.lower(),"*"*len(Mon.name))
        CensorEntry = CensorEntry.replace("\n"," ")
        CensorEntry = CensorEntry.replace("\u000c"," ")
        print(f'It has the following dex entry: "{CensorEntry}"')
    if Level > 4:
        print(f'You ran out of guesses, the pokemon was {Mon.name}')


DexId = random.randint(1,151)
Mon = Pokemon(DexId)
Level = 0
guessing = True
while guessing:
    Guess_Prompt(Mon,Level)
    name = input()
    if name.upper() == Mon.name.upper():
        print("You got it!")
        guessing = False
        ShinyRoll = random.randint(1,4096)
        if ShinyRoll == 2048:
            urllib.request.urlretrieve(Mon.shinyimg,f"{Mon.name}Shiny.png")
            print("You got a shiny!")
            img = Image.open(f"{Mon.name}Shiny.png")
            img.show()
        else:
            urllib.request.urlretrieve(Mon.img,f"{Mon.name}.png")
            img = Image.open(f"{Mon.name}.png")
            img.show()
        break
    else:
        Response = requests.get(f'{url}-species/{name}')
        if Response.status_code != 200: #additonal data in species 
            print("Please enter a real Pokemon")
            continue
        else:
            evochain = Response.json()['evolution_chain']['url']
        if evochain == Mon.evochain:
            print("Close! It is on the same evolution chain")
            
        else: 
            print("You did not get it")
            Level += 1
        
    if Level > 4:
        guessing = False
        print(f"You ran out of guesses, the pokemon was {Mon.name}")