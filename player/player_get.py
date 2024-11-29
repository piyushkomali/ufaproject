import requests
import json
import os
import sys
                #IMPORTANT INFO: playerID is max 9 characters, 1-firstname, 8-lastnameMAX
config = {} # Store the config variables

# Check if `config.json` contains the environment variable that we need
try:
    # Check if the config file exists in the current working directory
    CONFIG_PATH = '../config.json'
    if not os.path.exists(CONFIG_PATH):
        # Check if the config file exists in the same directory as this script
        CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.json')
    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_json:
        config = json.load(config_json)
# Case if the config file do not exist, go to the input section
except FileNotFoundError:
    print("\033[91mCannot find the config file, please make sure the config.json file is in the \
          same directory as this script or in the current working directory.\033[0m",
          file=sys.stderr)
# Case if the config file is not a valid json file(eg. empty file, corrupted file)
except json.decoder.JSONDecodeError:
    print("\033[91mThe config file is corrupted, please make sure the config.json file is in the\
        correct format.\033[0m", file=sys.stderr)
    

if "BASE_URL" not in config:
    config['BASE_URL'] = input('Please input your UFASTATS base url: ')

BASE_URL = config['BASE_URL']



url = f"{BASE_URL}playerStats"
playerID = input("\nenter player name(make sure it is correct): ").lower()
playerArray = playerID.split(" ")
lastName  = "".join(playerArray[1:]).replace("-","")[0:8]
playerID = playerArray[0][0:1] + lastName
year = input("\nenter year(OPTIONAL - press enter if not needed)\n[SEPARATE YEARS BY COMMAS IF MORE THAN ONE]: ")

url = f"{url}?playerIDs={playerID}"

if year != "":
    url = f"{url}&years={year}"


response = requests.get(url)
json_obj = response.json()

file = open("player.txt", "w")

for player in json_obj["data"]:
    
    returnString = json.dumps(player, indent=4)

    file.write(returnString)

file.close()
