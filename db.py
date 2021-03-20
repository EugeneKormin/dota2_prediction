from pymysql import connect
from pymysql.cursors import Cursor


def connect_to_db():
    db = connect(host="188.120.249.59", 
                         user="resolweru", 
                         passwd="qdxk7pdpd", 
                         db="mydb",
                         autocommit=True)
    cursor = db.cursor()
    return cursor


def add_to_db(cursor: Cursor, data: list):
    data = [data]
    cursor.executemany("""INSERT INTO dota2(
        id, duration, year, hour_sin, day_sin, min_sin, 
        radiant_team_id, dire_team_id, 
        league_id, series_id, radiant_score, dire_score, radiant_win, 
        dire_team_rating, radiant_team_rating, 
        games_won_by_dire_team, games_lost_by_dire_team, games_won_by_radiant_team, games_lost_by_radiant_team, 
        radiant_team_elo32_rating, radiant_team_elo64_rating, radiant_team_glicko1_rating, radiant_team_glicko2_rating, 
        radiant_team_elo32_mu, radiant_team_elo64_mu, radiant_team_glicko1_mu, radiant_team_glicko2_mu, 
        radiant_team_elo32_phi, radiant_team_elo64_phi, radiant_team_glicko1_phi, radiant_team_glicko2_phi, 
        radiant_team_elo32_sigma, radiant_team_elo64_sigma, radiant_team_glicko1_sigma, radiant_team_glicko2_sigma, 
        dire_team_elo32_rating, dire_team_elo64_rating, dire_team_glicko1_rating, dire_team_glicko2_rating, 
        dire_team_elo32_mu, dire_team_elo64_mu, dire_team_glicko1_mu, dire_team_glicko2_mu, 
        dire_team_elo32_phi, dire_team_elo64_phi, dire_team_glicko1_phi, dire_team_glicko2_phi, 
        dire_team_elo32_sigma, dire_team_elo64_sigma, dire_team_glicko1_sigma, dire_team_glicko2_sigma
        ) 
        VALUES (
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, 
        %s, %s, %s,
        %s, %s, %s, %s, %s, 
        %s, %s, %s)""", data)
    pass
