from flask import Flask, render_template, request
from player.player import get_player_data
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/player/player', methods=['GET'])
def player_get():
    player = request.args.get('player')
    year = request.args.get('year')

    """ if not year:
        year = " "
    if not player:
        player = " " """

    if not bool(year.strip()):
        return render_template('player-not-found.html')

    if not bool(player.strip()):
        
        return render_template('player-not-found.html')

    player_data = get_player_data(player, year)

    if len(player_data["data"]) == 0:
        return render_template('player-not-found.html')

    return render_template('player.html', 
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