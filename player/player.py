from pprint import pprint
import requests
import json

                #IMPORTANT INFO: playerID is max 9 characters, 1-firstname, 8-lastnameMAX
ufa_teams = {
    "hustle": "Atlanta Hustle",
    "sol": "Austin Sol",
    "glory": "Boston Glory",
    "flyers": "Carolina Flyers",
    "union": "Chicago Union",
    "summit": "Colorado Summit",
    "legion": "Dallas Legion",
    "breeze": "DC Breeze",
    "mechanix": "Detroit Mechanix",
    "havoc": "Houston Havoc",
    "alleycats": "Indianapolis AlleyCats",
    "aviators": "Los Angeles Aviators",
    "radicals": "Madison Radicals",
    "windchill": "Minnesota Wind Chill",
    "royal": "Montreal Royal",
    "empire": "New York Empire",
    "spiders": "Oakland Spiders",
    "phoenix": "Philadelphia Phoenix",
    "thunderbirds": "Pittsburgh Thunderbirds",
    "steel": "Oregon Steel",
    "shred": "Salt Lake Shred",
    "growlers": "San Diego Growlers",
    "cascades": "Seattle Cascades",
    "rush": "Toronto Rush"
}




def get_player_data(player="Jack Williams", year="2023"):
    url = "https://www.backend.ufastats.com/api/v1/playerStats"

    playerArray = player.split(" ")
    firstName = playerArray[0]
    lastName = " ".join(playerArray[1:]) if len(playerArray) > 1 else playerArray[1:]

    
    playerID = playerArray[0][0:1] 

    

    urlForPlayer = f"https://www.backend.ufastats.com/api/v1/players?years={year}"


    try:
            # Send GET request
            playerResponse = requests.get(urlForPlayer)  # Set a timeout to avoid hanging requests
            playerJson = playerResponse.json()  # Parse JSON response
            teamName = ""
            for p in playerJson["data"]:
                if p["firstName"] == firstName and p["lastName"] == lastName:
                    teamID = p["teams"][0]["teamID"]
                    playerID = p["playerID"]
                    try: 
                        teamName = ufa_teams[teamID]
                        break
                    except KeyError:
                        teamName = "Unknown"
                        break
                        
            url = f"{url}?playerIDs={playerID}&years={year}"
            response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging requests
            json_obj = response.json()  # Parse JSON response
            json_obj["data"][0]["player"]["team"] = teamName
            return json_obj
    
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch data from API: {e}")
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON response from API")
    


if __name__ == "__main__":
    player = input("\nenter player name(make sure it is correct): ")
    year = input("\nenter year(REQUIRED)\n: ")

    if not bool(year.strip()):
        year = " "
    if not bool(player.strip()):
        player = "Jack Williams"
    player_data = get_player_data(player, year)

    print("\n")
    pprint(player_data)

