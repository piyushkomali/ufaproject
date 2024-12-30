from flask import Flask, render_template, request
from player.player import get_player_data
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
    player_data = get_player_data(player, year)

    return render_template('player/player.html', 
                           title=player_data["data"][0]["player"]["firstName"] + " " + player_data["data"][0]["player"]["lastName"],
                           player=player_data["data"][0]["player"]["firstName"] + " " + player_data["data"][0]["player"]["lastName"], 
                           team=player_data["data"][0]["player"]["team"],
                           year=player_data["data"][0]["year"], 
                           assists=player_data["data"][0]["assists"], 
                           goals=player_data["data"][0]["goals"], 
                           hockeyAssists=player_data["data"][0]["hockeyAssists"], 
                           throwaways=player_data["data"][0]["throwaways"])

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)