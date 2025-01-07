from pprint import pprint
from team.team import get_team_map
import requests
import json

def get_player_szn(player="Jack Williams", year="2023"):
    ufa_teams = get_team_map(year)
    
    url = "https://www.backend.ufastats.com/api/v1/playerStats"

    urlForPlayer = f"https://www.backend.ufastats.com/api/v1/players?years={year}"
    try:
            # Send GET request
            playerResponse = requests.get(urlForPlayer, timeout=10)  # Set a timeout to avoid hanging requests
            playerJson = playerResponse.json()  # Parse JSON response
            teamName = ""
            for p in playerJson["data"]:
                if p["playerID"] == player:
                    teamID = p["teams"][0]["teamID"]
                    try: 
                        teamName = ufa_teams[teamID]
                        break
                    except KeyError:
                        teamName = "Unknown"
                        break
                        
            url = f"{url}?playerIDs={player}&years={year}"
            response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging requests
            json_obj = response.json()  # Parse JSON response
            json_obj["data"][0]["player"]["team"] = teamName
            return json_obj
    
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch data from API: {e}")
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON response from API")

def get_player_game(playerID="blewis",year="2019", game="2019-08-11-DAL-NY"):
    url = f"https://www.backend.ufastats.com/api/v1/playerGameStats?gameID={game}"
    ufa_teams = get_team_map(year)
    try:
            # Send GET request
            response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging requests
            playerJson = response.json()  # Parse JSON response
            for p in playerJson["data"]:
                if p["player"]["playerID"] == playerID:
                   teamID = p["teamID"]
                   p["team"] = ufa_teams[teamID]
                   return p                    
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch data from API: {e}")
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON response from API")
    


if __name__ == "__main__":
    player = input("\nenter player name(make sure it is correct): ")
    year = input("\nenter year(REQUIRED)\n: ")
    game = input("\nenter game id: ")

    if not bool(year.strip()):
        year = " "
    if not bool(player.strip()):
        player = "Jack Williams"
    player_data = get_player_szn(player, year)

    print("\n")
    pprint(player_data)

