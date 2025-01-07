from flask import Flask, render_template, request
from player.player import *
from team.team import get_team_data
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/player-input.html')
def player_input():
    return render_template('player/player-input.html')

@app.route('/team-input.html')
def team_input():
    return render_template('team/team-input.html')

@app.route('/team', methods=['GET'])
def team_get():
    year = request.args.get('year')
    team = request.args.get('team')
    team_data = get_team_data(team, year)
    
    return render_template('team/team.html', 
                           title=team_data["data"][0]["fullName"], 
                           year=team_data["data"][0]["year"],
                           city=team_data["data"][0]["city"],
                           division=team_data["data"][0]["division"]["name"],
                           wins=team_data["data"][0]["wins"],
                           losses=team_data["data"][0]["losses"],
                           ties=team_data["data"][0]["ties"],
                           standing=team_data["data"][0]["standing"])



@app.route('/player', methods=['GET'])
def player_get():
    player = request.args.get('player')
    year = request.args.get('year')
    sznOrGame = request.args.get('sznOrGame')
    if sznOrGame == "season":
        player_data = get_player_szn(player, year)
        return render_template('player/playerSzn.html', 
                            title=player_data["data"][0]["player"]["firstName"] + " " + player_data["data"][0]["player"]["lastName"],
                            player=player_data["data"][0]["player"]["firstName"] + " " + player_data["data"][0]["player"]["lastName"], 
                            team=player_data["data"][0]["player"]["team"],
                            year=player_data["data"][0]["year"], 
                            assists=player_data["data"][0]["assists"], 
                            goals=player_data["data"][0]["goals"], 
                            hockeyAssists=player_data["data"][0]["hockeyAssists"], 
                            throwaways=player_data["data"][0]["throwaways"])
    else:

        game = request.args.get('games')
        player_data = get_player_game(player,year, game)
        return render_template('player/playerGame.html', 
                            title=player_data["player"]["firstName"] + " " + player_data["player"]["lastName"],
                            number=player_data["jerseyNumber"],
                            team=player_data["team"],
                            year=year,
                            assists=player_data["assists"],
                            goals=player_data["goals"],
                            hockeyAssists=player_data["hockeyAssists"],
                            completions=player_data["completions"],
                            throwAttempts=player_data["throwAttempts"],
                            throwaways=player_data["throwaways"],
                            stalls=player_data["stalls"],
                            callahansThrown=player_data["callahansThrown"],
                            yardsReceived=player_data["yardsReceived"],
                            yardsThrown=player_data["yardsThrown"],
                            hucksAttempted=player_data["hucksAttempted"],
                            hucksCompleted=player_data["hucksCompleted"],
                            catches=player_data["catches"],
                            drops=player_data["drops"],
                            blocks=player_data["blocks"],
                            callahans=player_data["callahans"],
                            pulls=player_data["pulls"],
                            obPulls=player_data["obPulls"],
                            oPointsPlayed=player_data["oPointsPlayed"],
                            oPointsScored=player_data["oPointsScored"],
                            dPointsPlayed=player_data["dPointsPlayed"],
                            dPointsScored=player_data["dPointsScored"]
                            )

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)