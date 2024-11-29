import requests
import json

url = input("enter url: ")
team_input = input("enter team name: ").upper()
response = requests.get(url)
json_obj = response.json()

file = open("team.txt", "w")

for team in json_obj["data"]:
    if team["fullName"].upper() == team_input:
        json.dump(team, file,indent=4)

file.close()

