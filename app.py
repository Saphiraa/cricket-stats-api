import flask
from flask import request, jsonify
import mysql.connector
from mysql.connector import connect, cursor
from configparser import ConfigParser

app = flask.Flask(__name__)

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


def make_relative_player(players):
    for i in range(len(players)):
        players[i]["country_code"] = request.host_url + "api/v1/resources/countries/" + str(players[i]["country_code"])
        players[i]["team_id"] = request.host_url +"api/v1/resources/teams/" + str(players[i]["team_id"])
    return players


def make_relative_venue(venues):
    for i in range(len(venues)):
        venues[i]["country_code"] = request.host_url + "api/v1/resources/countries/" + str(venues[i]["country_code"])
    return venues

    
def make_relative_match(matches):
    for i in range(len(matches)):
        matches[i]["winner"] = request.host_url + "api/v1/resources/teams/" + str(matches[i]["winner"])
        matches[i]["loser"] = request.host_url + "api/v1/resources/teams/" + str(matches[i]["loser"])
        matches[i]["man_of_the_match"] = request.host_url + "api/v1/resources/players/" + str(matches[i]["man_of_the_match"])
        matches[i]["bowler_of_the_match"] = request.host_url + "api/v1/resources/players/" + str(matches[i]["bowler_of_the_match"])
        matches[i]["best_fielder"] = request.host_url + "api/v1/resources/players/" + str(matches[i]["best_fielder"])
    return matches


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cricket API</h1><p>Cricket League Tournament Application</p>"

# RESOURCE BY ID
@app.route('/api/v1/resources/players/<id>', methods = ['GET', 'DELETE', 'PUT'])
def api_players_id(id):

    if request.method == 'DELETE':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("delete from player where id = %s;", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    elif request.method == 'GET': 
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from player where id = %s;", (id,)) 
        # Trailing comma is required.
        # example - python treates (7) as 7 so to have a tuple of length 1, it has to be (7,)
        # using mysqldb hence %s. use ? for sqlite 3.
        # better check documentation of module
        player = cursor.fetchall()
        cursor.close()
        conn.close()
        player = make_relative_player(player)
        resp = jsonify(player)
        resp.status_code = 200
        return resp
    elif request.method == 'PUT':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        # TODO - add checks for keys
        for field, value in request.args.items():
            cursor.execute(
                "UPDATE player SET {} = %s WHERE id = %s;".format(field),
                (value, id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/matches/<id>', methods = ['GET', 'DELETE', 'PUT'])
def api_matches_id(id):

    if request.method == 'DELETE':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("delete from `match` where id = %s;", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    elif request.method == 'GET': 
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from `match` where id = %s;", (id,)) 
        # Trailing comma is required.
        # example - python treates (7) as 7 so to have a tuple of length 1, it has to be (7,)
        # using mysqldb hence %s. use ? for sqlite 3.
        # better check documentation of module
        match = cursor.fetchall()
        match = make_relative_match(match)
        cursor.close()
        conn.close()
        resp = jsonify(match)
        resp.status_code = 200
        return resp
    elif request.method == 'PUT':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        # TODO - add checks for keys
        for field, value in request.args.items():
            cursor.execute(
                "UPDATE `match` SET {} = %s WHERE id = %s;".format(field),
                (value, id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/teams/<id>', methods = ['GET', 'DELETE', 'PUT'])
def api_teams_id(id):

    if request.method == 'DELETE':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("delete from team where id = %s;", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    elif request.method == 'GET': 
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from team where id = %s;", (id,)) 
        # Trailing comma is required.
        # example - python treates (7) as 7 so to have a tuple of length 1, it has to be (7,)
        # using mysqldb hence %s. use ? for sqlite 3.
        # better check documentation of module
        team = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(team)
        resp.status_code = 200
        return resp
    elif request.method == 'PUT':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        # TODO - add checks for keys
        for field, value in request.args.items():
            cursor.execute(
                "UPDATE team SET {} = %s WHERE id = %s;".format(field),
                (value, id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/countries/<id>', methods = ['GET', 'DELETE','PUT'])
def api_countries_id(id):

    if request.method == 'DELETE':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("delete from country where id = %s;", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    elif request.method == 'GET': 
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from country where id = %s;", (id,)) 
        # Trailing comma is required.
        # example - python treates (7) as 7 so to have a tuple of length 1, it has to be (7,)
        # using mysqldb hence %s. use ? for sqlite 3.
        # better check documentation of module
        country = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(country)
        resp.status_code = 200
        return resp
    elif request.method == 'PUT':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        # TODO - add checks for keys
        for field, value in request.args.items():
            cursor.execute(
                "UPDATE country SET {} = %s WHERE id = %s;".format(field),
                (value, id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/venues/<id>', methods = ['GET', 'DELETE', 'PUT'])
def api_venues_id(id):

    if request.method == 'DELETE':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("delete from venue where id = %s;", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    elif request.method == 'GET': 
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from venue where id = %s;", (id,)) 
        # Trailing comma is required.
        # example - python treates (7) as 7 so to have a tuple of length 1, it has to be (7,)
        # using mysqldb hence %s. use ? for sqlite 3.
        # better check documentation of module
        venue = cursor.fetchall()
        venue = make_relative_venue(venue)
        cursor.close()
        conn.close()
        resp = jsonify(venue)
        resp.status_code = 200
        return resp
    elif request.method == 'PUT':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        # TODO - add checks for keys
        for field, value in request.args.items():
            cursor.execute(
                "UPDATE venue SET {} = %s WHERE id = %s;".format(field),
                (value, id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


# ALL
@app.route ('/api/v1/resources/players/all', methods = ['GET'])
def api_players_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from player;")
    result = cursor.fetchall()
    result = make_relative_player(result)
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
    result = make_relative_match(result)
    return jsonify(result)


@app.route ('/api/v1/resources/venues/all', methods = ['GET'])
def api_venues_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM venue;")
    result = cursor.fetchall()
    result = make_relative_venue(result)
    return jsonify(result)


@app.route ('/api/v1/resources/countries/all', methods = ['GET'])
def api_countries_all():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM country;")
    result = cursor.fetchall()
    return jsonify(result)


# RESOURCES
@app.route('/api/v1/resources/players', methods = ['GET', 'POST', 'PUT'])
def api_players():

    if request.method == 'GET':
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
                result = make_relative_player(result)
                return jsonify(result)

        result = make_relative_player(result)
        return jsonify(result)

    elif request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        full_name = request.args["full_name"]
        age = request.args["age"]
        playing_role = request.args["playing_role"]
        team_id = request.args["team_id"]
        country_code = request.args["country_code"]

        cursor.execute(
            "insert into player (full_name, age, playing_role, team_id, country_code)"
            "values (%s, %s, %s, %s, %s);",
            (full_name, age, playing_role, team_id, country_code)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/teams', methods = ['GET', 'POST'])
def api_teams():

    if request.method == 'GET':
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
    
    elif request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        name = request.args["name"]
        matches_played = request.args["matches_played"]
        wins = request.args["wins"]
        losses = request.args["losses"]

        cursor.execute(
            "insert into team (name, matches_played, wins, losses)"
            "values (%s, %s, %s, %s);",
            (name, matches_played, wins, losses)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True)
    
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/matches', methods = ['GET', 'POST'])
def api_matches(): 

    if request.method == 'GET':
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
                result = make_relative_match(result)
                return jsonify(result)

        result = make_relative_match(result)
        return jsonify(result)

    elif request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        
        match_date = request.args["match_date"]
        winner = request.args["winner"]
        loser = request.args["loser"]
        mom = request.args["man_of_the_match"]
        bom = request.args["bowler_of_the_match"]
        bf = request.args["best_fielder"]

        cursor.execute(
            "insert into `match` "
            "(match_date, winner, loser, man_of_the_match, bowler_of_the_match, best_fielder)"
            "values (%s, %s, %s, %s, %s, %s);",
            (match_date, winner, loser, mom, bom, bf)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/countries', methods = ['GET', 'POST'])
def api_countries(): 

    if request.method == 'GET':
        conditions = []
        count = 20

        if 'id' in request.args:
            value = int(request.args['id'])
            conditions.append(("id", value))
        
        if 'name' in request.args:
            value = str(request.args['name'])
            conditions.append(("name", value))

        if 'count' in request.args:
            count = int(request.args['count'])

        if len(conditions) == 0:
            return "No filters provided"

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from country;")
        countries = cursor.fetchall()

        result = []
        for country in countries:
            if check_conditions(country, conditions):
                result.append(country)
            if len(result) >= count:
                return jsonify(result)

        return jsonify(result)

    elif request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        
        id = request.args["id"]
        name = str(request.args["id"]).upper()

        cursor.execute(
            "insert into country "
            "(id, name)"
            "values (%s, %s);",
            (id, name)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/api/v1/resources/venues', methods = ['GET', 'POST'])
def api_venues(): 

    if request.method == 'GET':
        conditions = []
        count = 20

        if 'country_code' in request.args:
            value = int(request.args['country_code'])
            conditions.append(("country_code", value))
        
        if 'id' in request.args:
            value = str(request.args['id'])
            conditions.append(("id", value))
        
        if 'name' in request.args:
            value = str(request.args['name'])
            conditions.append(("name", value))

        if 'count' in request.args:
            count = int(request.args['count'])

        if len(conditions) == 0:
            return "No filters provided"

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from venue;")
        venues = cursor.fetchall()

        result = []
        for venue in venues:
            if check_conditions(venue, conditions):
                result.append(venue)
            if len(result) >= count:
                result = make_relative_venue(result)
                return jsonify(result)
        
        result = make_relative_venue(result)
        return jsonify(result)

    elif request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        
        country_code = request.args["country_code"]
        name = request.args["name"]

        cursor.execute(
            "insert into venue "
            "(country_code, name)"
            "values (%s, %s);",
            (country_code, name)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)
    else:
        return jsonify(success=False)

