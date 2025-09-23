import requests
import urllib.request
import random 

from PIL import Image

url = "https://pokeapi.co/api/v2/pokemon"
GenList = ["1-151","152-251","252-386","387-493","494-649","650-721","722-809","810-905","906-1025"] #note that some of the later generations seems to have info missing that will not return the info necesseary

class Pokemon:
    def __init__(self,id):
        Response = requests.get(f'{url}/{id}')
        if Response.status_code != 200:
            print(f"No Pokémon found (ERROR: {Response.status_code})")
            return(ValueError)
        Data = Response.json()
        self.name = Data['name']
        self.id = Data['id']
        self.weight = Data['weight'] * 0.1
        self.height = Data['height'] * 0.1
        self.img = Data['sprites']['other']['official-artwork']['front_default']
        try:
            self.shinyimg = Data['sprites']['other']['official-artwork']['front_shiny']
        except:
            self.shinyimg = "NA"

        self.abilities = []
        for x in Data['abilities']:
            self.abilities.append(x['ability']['name'])
        
        self.types = []
        for x in Data['types']:
            self.types.append(x['type']['name'])
        
        self.stats = []
        for x in Data['stats']:
            self.stats.append(f'{x['stat']['name']} : {x['base_stat']}')

        Response = requests.get(f'{url}-species/{self.id}')
        if Response.status_code != 200: #additonal data in species 
            print(f"Unable to retrieve species data from {url}-species/{self.id}")
            return(ValueError)
        else:
            SpecData = Response.json()
            self.egggroups = []
            for x in SpecData['egg_groups']:
                self.egggroups.append(x['name'])
            self.shape = SpecData['shape']['name']
            self.color = SpecData['color']['name']
            self.evochain = SpecData['evolution_chain']['url']
            self.baby = SpecData['is_baby']
            self.legend = SpecData['is_legendary']
            self.myth = SpecData['is_mythical']
            for x in SpecData['flavor_text_entries']:
                if x['language']['name'] == 'en':
                    self.entry = x['flavor_text']
                    break #grabs first english entry
            self.gen = SpecData["generation"]["name"]
            genurl = SpecData["generation"]["url"]
            Response = requests.get(f'{genurl}')
            if Response.status_code != 200:
                print(f"Unable to retrieve data from {genurl}")
                return(ValueError)
            else:
                GenData = Response.json()
                GameVers = GenData["version_groups"][0]["name"]
                GameReg = GenData["main_region"]["name"]
                self.debut = f"{GameVers} ({GameReg} region)"




def Guess_Prompt(Mon=Pokemon,Level = 0):
    if Level == 0:
        print(f'This Pokémon first appeared in : Pokémon {Mon.debut}')
        print(f'It is {Mon.shape} shaped and coloured {Mon.color}')
    if Level == 1:
        StatNames = []
        StatVals = []
        for x in Mon.stats:
            stats = x.split(':')
            StatNames.append(stats[0])
            StatVals.append(int(stats[1]))
        print(f'Its lowest stat is {StatNames[StatVals.index(min(StatVals))]}')
        print(f'Its highest stat is {StatNames[StatVals.index(max(StatVals))]}')
        if len(Mon.egggroups) > 1:
            print(f'It is a member of the following egg groups :')
            for x in Mon.egggroups:
                if x == "ground":
                    x = "field"
                print(x)
        else:
            if Mon.egggroups[0] == "ground":
                print(f'It is a member of the field egg group')
            else:
                print(f'It is a member of the {Mon.egggroups[0]} egg group')
    if Level == 2:
        if len(Mon.types) > 1:
            print(f'It is a {Mon.types[0]}-{Mon.types[1]} type')
        else:
            print(f'It is a {Mon.types[0]} type')
        print(f'It is {round(Mon.height,1)}m ({round(Mon.height*3.281,1)}ft) tall and weighs {round(Mon.weight,1)}kg ({round(Mon.weight*2.2046,1)}lbs)')

    if Level == 3:
        if len(Mon.abilities) > 1:
            print(f'It has the following abilities:')
            for x in Mon.abilities:
                print(x)
        else:
            print(f'It has the {Mon.abilities[0]} ability')
    if Level == 4:
        if Mon.baby:
            print("This Pokémon is a baby")    
        if Mon.myth:
            print("This Pokémon is mthical")
        if Mon.legend:
            print("This Pokémon is legendary")
        CensorEntry = Mon.entry.lower().replace(Mon.name.lower(),"*"*len(Mon.name))
        CensorEntry = CensorEntry.replace("\n"," ")
        CensorEntry = CensorEntry.replace("\u000c"," ")
        print(f'It has the following dex entry: "{CensorEntry}"')
    if Level > 4:
        print(f'You ran out of guesses, the Pokémon was {Mon.name}')

def play_game(Generation):
    Min = int(GenList[Generation-1].split("-")[0])
    Max = int(GenList[Generation-1].split("-")[1])

    playing = True
    while playing:
        DexId = random.randint(Min,Max)
        try:
            Mon = Pokemon(DexId)
        except:
            print("Failed to find pokemon.")
            return
        Level = 0
        guessing = True
        while guessing:
            Guess_Prompt(Mon,Level)
            name = input()
            name = name.replace(" ","-")
            name = name.replace(".","-") #filter for cases where the name is odd (such as mr.mime)
            if name.lower() == "nidoran":
                print("Please specify gender of nidoran with -f or -m")
                name = input()
            if name.upper() == Mon.name.upper():
                print("You got it!")
                guessing = False
                ShinyRoll = random.randint(1,100)
                if ShinyRoll == 100:
                    print("You got a shiny!")
                print("Would you like to add this to your dex? (y/n)")
                Add = input()
                if Add.upper() == "N":
                    break
                else:
                    pass
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
                    print("Please enter a real Pokémon")
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
                print(f"You ran out of guesses, the Pokémon was {Mon.name}")

        print("Would you like to play again? (y/n)")
        ans = input()
        try:
            ans = ans[0] #in case of user writing "no" instead, likely a good idea to do similar elsewhere
        except:
            ans = "N"
        if ans.upper() == "N":
            return

play_game(6)

#play_game(1)