import flask
from flask import request, jsonify
import mysql.connector


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


# @app.route('/api/v1/resources/players', methods =['GET'])
# def api_players_id():
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No field is provided. Specify ID."

#     results = []
#     for player in players:
#         if player['id'] == id:
#             results.append(player)

#     return jsonify(results)

# @app.route('/api/v1/resources/teams/all', methods=['GET'])
# def api_teams_all():
#     return jsonify(teams)

# @app.route('/api/v1/resources/teams', methods =['GET'])
# def api_teams_id():
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No field is provided. Specify ID."

#     results = []

#     for team in teams:
#         if team['id'] == id:
#             results.append(team)

#     return jsonify(results)

app.run()
