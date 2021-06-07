import flask
from flask import request, jsonify
import mysql.connector
from mysql.connector import cursor
from configparser import ConfigParser


def connect_db():
    """
    Connect to db and return connection object
    """
    config = ConfigParser()
    config.read('database.ini')
    conn = mysql.connector.connect(
        host = config['database']['host'],
        database = config['database']['database'],
        user = config['database']['user'],
        password = config['database']['password'],
    )
    return conn


def check_conditions(item, conditions):
    """
    Function for checking conditions using a list of conditions. 
    """
    for condition in conditions:
        if item[condition[0]] != condition[1]:
            return False
    return True

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cricket API</h1><p>Cricket League Tournament Application</p>"

# RESOURCE BY ID
@app.route('/api/v1/resources/players/<id>', methods = ['GET'])
def api_players_id(id):

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from player where id = %s;", (id,)) 
    # Trailing comma is required.
    # example - python treates (7) as 7 so to have a tuple of length 1, it has to be (7,)
    # using mysqldb hence %s. use ? for sqlite 3.
    # better check documentation of module
    player = cursor.fetchall()
    return jsonify(player)

# ALL
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


# FILTERS
@app.route('/api/v1/resources/players', methods = ['GET'])
def api_players():

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

    result = []
    for player in players:
        if check_conditions(player, conditions):
            result.append(player)
        if len(result) >= count:
            return jsonify(result)

    return jsonify(result)
    

@app.route('/api/v1/resources/teams', methods = ['GET'])
def api_teams():

    conditions = []
    count = 20

    if 'id' in request.args:
        value = int(request.args['id'])
        conditions.append(("id", value))
    
    if 'name' in request.args:
        value = str(request.args['name'])
        conditions.append(("name", value))

    if 'matches_played' in request.args:
        value = int(request.args['matches_played'])
        conditions.append(("matches_played", value))

    if 'wins' in request.args:
        value = int(request.args['wins'])
        conditions.append(("wins", value))

    if 'losses' in request.args:
        value = int(request.args['losses'])
        conditions.append(("losses", value))

    if 'count' in request.args:
        count = int(request.args['count'])

    if len(conditions) == 0:
        return "No filters provided"

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from team;")
    teams = cursor.fetchall()

    result = []
    for team in teams:
        if check_conditions(team, conditions):
            result.append(team)
        if len(result) >= count:
            return jsonify(result)
    
    return jsonify(result)


@app.route('/api/v1/resources/matches', methods = ['GET'])
def api_matches(): 

    conditions = []
    count = 20

    if 'id' in request.args:
        value = int(request.args['id'])
        conditions.append(("id", value))
    
    if 'winner' in request.args:
        value = str(request.args['winner'])
        conditions.append(("winner", value))

    if 'loser' in request.args:
        value = int(request.args['loser'])
        conditions.append(("loser", value))

    if 'man_of_the_match' in request.args:
        value = int(request.args['man_of_the_match'])
        conditions.append(("man_of_the _match", value))

    if 'bowler_of_the_match' in request.args:
        value = int(request.args['bowler_of_the_match'])
        conditions.append(("bowler_of_the_match", value))

    if 'best_fielder' in request.args:
        value = int(request.args['best_fielder'])
        conditions.append(("best_fielder", value))

    if 'count' in request.args:
        count = int(request.args['count'])

    if len(conditions) == 0:
        return "No filters provided"

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from `match`;")
    matches = cursor.fetchall()

    result = []
    for match in matches:
        if check_conditions(match, conditions):
            result.append(match)
        if len(result) >= count:
            return jsonify(result)

    # TODO -> change referenced values to linked vaalues 
    # example - 
    # man_of_the_match: 3
    # becomes
    # man_of_the_match: /api/v1/resources/players/3 or something

    return jsonify(result)


app.run()
