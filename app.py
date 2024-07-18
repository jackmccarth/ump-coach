from flask import Flask, request, jsonify, render_template
import pyodbc
import datetime

app = Flask(__name__)

# Database connection details
server = 'localhost,1433'
database = 'AFL_Umpiring'
username = 'SA'
password = 'YourStrong@Passw0rd'
driver = '{ODBC Driver 17 for SQL Server}'

# Helper function to execute SQL query and fetch results
def fetch_results(query):
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Helper function to execute SQL insert
def execute_query(query, params):
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_options')
def get_options():
    leagues = fetch_results("SELECT id, league_description FROM dimLeagues")
    rounds = fetch_results("SELECT id, round_description FROM dimRounds")
    grounds = fetch_results("SELECT id, ground_description FROM dimGrounds")
    teams = fetch_results("SELECT id, team_description FROM dimTeams")

    return jsonify({
        'leagues': [{'id': row.id, 'description': row.league_description} for row in leagues],
        'rounds': [{'id': row.id, 'description': row.round_description} for row in rounds],
        'grounds': [{'id': row.id, 'description': row.ground_description} for row in grounds],
        'teams': [{'id': row.id, 'description': row.team_description} for row in teams]
    })

@app.route('/insert_game', methods=['POST'])
def insert_game():
    date = request.form['date']
    league_id = request.form['league']
    round_id = request.form['round']
    ground_id = request.form['ground']
    home_team_id = request.form['home_team']
    away_team_id = request.form['away_team']

    query = """
    INSERT INTO dimGame (game_date, league_id, round_id, ground_id, home_team_id, away_team_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    params = (date, league_id, round_id, ground_id, home_team_id, away_team_id)
    execute_query(query, params)

    return 'Game inserted successfully'

if __name__ == '__main__':
    app.run(debug=True)
