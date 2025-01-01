from pprint import pprint
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
     
def get_team_map(years):
    url = f"{BASE_URL}teams?years={years}"
    listOfTeams = {}
    response = requests.get(url)
    json_obj = response.json()
    for team in json_obj["data"]:
        listOfTeams[team["teamID"]] = team["fullName"]
    return listOfTeams

                #IMPORTANT INFO: playerID is max 9 characters, 1-firstname, 8-lastnameMAX

def get_team_data(team="Raleigh Flyers", year="2023"):
    url = f"{BASE_URL}teams"
    url = f'{url}?years={year}&teamIDs={team}'
    
    try:
            # Send GET request
            response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging requests
            json_obj = response.json()  # Parse JSON response
            return json_obj
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch data from API: {e}")
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON response")
    
if __name__ == "__main__":
    team = input("\nenter team name(make sure it is correct): ")
    year = input("\nenter year(REQUIRED)\n: ")

    if not bool(year.strip()):
        year = " "
    if not bool(team.strip()):
        team = "Raleigh Flyers"
    team_data = get_team_data(team, year)

    print("\n")
    pprint(team_data)