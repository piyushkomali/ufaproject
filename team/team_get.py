import requests
import json
import os
import sys
                
def get_team_list(yearsString):
    url = f"{BASE_URL}teams?years={yearsString}"
    listOfTeams = []
    response = requests.get(url)
    json_obj = response.json()
    for team in json_obj["data"]:
        listOfTeams.append(team["teamID"])
    return listOfTeams

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

url = f"{BASE_URL}teams"



#Minnesota Wind Chill, New York Empire, Carolina Flyers
year = input("\nenter year(required) - this will return data for all teams in that year\n[SEPARATE YEARS BY COMMAS IF MORE THAN ONE]: ")
teams = input("\nenter FULL team name(optional) - this will return data for those team\n[SEPARATE TEAMS BY COMMAS IF MORE THAN ONE]: ").lower()
teamsAppendString = ""

url = f"{url}?years={year}"

teamIdList = get_team_list(year)
if teams != "":
    
    teamsArray = teams.split(",")
    for team in teamsArray:
        teamIteration = team.split(" ")
        if teamIteration[-1] != "chill" and teamIteration[-1] in teamIdList:
            teamsAppendString += teamIteration[-1] + ","
        elif teamIteration[-2] == "wind" and teamIteration[-1] == "chill" and "windchill" in teamIdList:
            teamsAppendString += "windchill,"
        else:
            print("one or more of the teams are invalid, try again.")
            teamsAppendString = "invalid,"
            break
    teamsAppendString = teamsAppendString[:-1]

    url = f"{url}&teamIDs={teamsAppendString}"

if teamsAppendString != "invalid,":
    response = requests.get(url)
    json_obj = response.json()

    file = open("team.txt", "w")

    for team in json_obj["data"]:
        returnString = json.dumps(team, indent=4)

        file.write(returnString)

    file.close()

