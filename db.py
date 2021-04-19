from pymysql import connect
from read_config import host, user, passwd, db_name
from time import sleep


def connect_to_db() -> dict:
    """
    establishing connection to mysql DB\n
    :return: dict with conn & cursor as keys
    """
    conn = connect(host=host,
                 user=user,
                 passwd=passwd,
                 db=db_name,
                 autocommit=True)

    cursor = conn.cursor()
    mysql = {
        "conn": conn,
        "cursor": cursor
    }
    return mysql


def get_parsed_match() -> list:
    """
    Get number of matches that has already been added to DB\n
    :param cursor: cursor\n
    :return: num of matches currently in DB
    """
    mysql = connect_to_db()
    cursor = mysql["cursor"]
    query = """SELECT id FROM dota2"""
    cursor.execute(query)
    match_id_list = cursor.fetchall()
    match_id_list_temp = []
    [match_id_list_temp.append(match_id[0]) for match_id in match_id_list]

    return match_id_list_temp


def add_many_to_db(matches_list: list):
    """
    Method is used for adding parsed match detailed data to DB\n
    :param cursor: cursor\n
    :param matches_list: list of matches that are to be added to DB
    """
    print("start adding to db")

    query = """INSERT IGNORE INTO dota2(
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
        dire_team_elo32_sigma, dire_team_elo64_sigma, dire_team_glicko1_sigma, dire_team_glicko2_sigma, 
        comments
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
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s)"""

    # establishing DB connection
    mysql = connect_to_db()
    conn = mysql["conn"]
    # if connection was not established. Reconnecting with 3 second interval.
    while not conn.open:
        mysql = connect_to_db()
        sleep(3)

    cursor = mysql["cursor"]

    # executing query
    cursor.executemany(query, matches_list)

    cursor.close()
    print("add to DB. Success")
