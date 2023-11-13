
from conncect_db import connect_to_database, close_database_connection



# 1. Get all players by the team
def get_players_by_team(team_name):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players WHERE "Tm" = ?', (team_name,))
    players = cursor.fetchall()
    close_database_connection(conn)
    return players

# 2. Get all stats for a particular player
def get_player_stats(player_name):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players WHERE "Player" = ?', (player_name,))
    player_stats = cursor.fetchall()
    close_database_connection(conn)
    return player_stats

# 3. Get only selected stats for a particular player
def get_selected_player_stats(player_name, selected_columns):
    conn, cursor = connect_to_database()

    # Create a string of selected columns for the SQL query
    selected_cols_str = ', '.join(selected_columns)
    query = f'SELECT {selected_cols_str} FROM Players WHERE "Player" = ?'

    cursor.execute(query, (player_name,))
    selected_stats = cursor.fetchall()
    
    close_database_connection(conn)
    return selected_stats

# 1. Get Players by Position
def get_players_by_position(position):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players WHERE "Pos" = ?', (position,))
    players = cursor.fetchall()
    close_database_connection(conn)
    return players

# 2. Get Top Scorers
def get_top_scorers(num_players):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players ORDER BY "PTS" DESC LIMIT ?', (num_players,))
    top_scorers = cursor.fetchall()
    close_database_connection(conn)
    return top_scorers

# 3. Get Players by Age Range
def get_players_by_age_range(min_age, max_age):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players WHERE "Age" BETWEEN ? AND ?', (min_age, max_age))
    players = cursor.fetchall()
    close_database_connection(conn)
    return players

# 4. Get Players by Performance Metric
def get_players_by_performance_metric(metric_column, min_value):
    conn, cursor = connect_to_database()
    cursor.execute(f'SELECT * FROM Players WHERE "{metric_column}" >= ?', (min_value,))
    high_performance_players = cursor.fetchall()
    close_database_connection(conn)
    return high_performance_players

# 5. Get Team Roster
def get_team_roster(team_name):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT "Player", "Pos" FROM Players WHERE "Tm" = ?', (team_name,))
    team_roster = cursor.fetchall()
    close_database_connection(conn)
    return team_roster

# 6. Get Team Stats (Average Points Scored per Game)
def get_team_stats(team_name):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT AVG("PTS") FROM Players WHERE "Tm" = ?', (team_name,))
    avg_points = cursor.fetchone()
    close_database_connection(conn)
    return avg_points[0]  # Extract the average points scored per game

# 7. Get Player Rankings (Points per Game)
def get_player_rankings_by_ppg(num_players):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT "Player", "PTS" FROM Players ORDER BY "PTS" DESC LIMIT ?', (num_players,))
    player_rankings = cursor.fetchall()
    close_database_connection(conn)
    return player_rankings

# 8. Get Players by Conference or Division
def get_players_by_conference_or_division(conference, division):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players WHERE "Conference" = ? AND "Division" = ?', (conference, division))
    players = cursor.fetchall()
    close_database_connection(conn)
    return players

# 9. Get Player Statistics by Game Date Range
def get_player_stats_by_date_range(player_name, start_date, end_date):
    conn, cursor = connect_to_database()
    cursor.execute('SELECT * FROM Players WHERE "Player" = ? AND "Date" BETWEEN ? AND ?', (player_name, start_date, end_date))
    player_stats = cursor.fetchall()
    close_database_connection(conn)
    return player_stats