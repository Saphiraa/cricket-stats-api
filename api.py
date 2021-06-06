import flask
from flask import request, jsonify
import mysql.connector
from mysql.connector import cursor


def connect_db():
    """
    Connect to db and return connection object
    """
    conn = mysql.connector.connect(
        host = "localhost",
        database = "cricket",
        user = "root",
        password = ""
    )
    return conn

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cricket API</h1><p>Cricket League Tournament Application</p>"

# route using url and GET from the database
# connect to database 
@app.route ('/api/v1/resources/players/all', methods = ['GET'])
def api_players_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from player;")
    result = cursor.fetchall()
    return jsonify(result)

@app.route ('/api/v1/resources/teams/all', methods = ['GET'])
def api_teams_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from team;")
    result = cursor.fetchall()
    return jsonify(result)

@app.route ('/api/v1/resources/matches/all', methods  = ['GET'])
def api_matches_all(): 
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from `match`;")
    result = cursor.fetchall()
    return jsonify(result)

@app.route ('/api/v1/resources/venues/all', methods = ['GET'])
def api_venues_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM venue;")
    result = cursor.fetchall()
    return jsonify(result)

@app.route ('/api/v1/resources/countries/all', methods = ['GET'])
def api_countries_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM country;")
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/api/v1/resources/players', methods =['GET'])
def api_players_id():

    conditions = []
    count = 20
    if 'id' in request.args:
        id = int(request.args['id'])
        conditions.append(("id", id))

    if 'full_name' in request.args:
        full_name = str(request.args['full_name'])
        conditions.append(("full_name", full_name))

    if 'playing_role' in request.args:
        playing_role = str(request.args['playing_role'])
        conditions.append(("playing_role", playing_role))
    
    if 'team_id' in request.args:
        team_id = int(request.args['team_id'])
        conditions.append(("team_id", team_id))
    
    if 'country_code' in request.args:
        country_code = int(request.args['country_code'])
        conditions.append(("country_code", country_code))
    
    if 'count' in request.args:
        count = int(request.args['count'])

    if len(conditions) == 0:
        return "No filters provided"

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from player;")
    players = cursor.fetchall()

    def check_conditions(player, conditions):
        for condition in conditions:
            if player[condition[0]] != condition[1]:
                return False
        return True

    result = []
    for player in players:
        if check_conditions(player, conditions):
            result.append(player)
        if len(result) >= count:
            return jsonify(result)

    return jsonify(result)
    
app.run()
