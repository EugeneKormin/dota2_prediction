from pymysql import connect


def connect_to_db():
    """
    establishing connection to mysql DB
    :return: db
    """
    db = connect(host="188.120.249.59", 
                 user="resolweru",
                 passwd="qdxk7pdpd",
                 db="mydb",
                 autocommit=True)
    return db


def get_list_of_matches_parsed():
    """
    Get number of matches that has already been added to DB
    :param cursor: cursor
    :return: num of matches currently in DB
    """
    db = connect_to_db()
    cursor = db.cursor()
    query = """SELECT id FROM dota2"""
    cursor.execute(query)
    match_id_list = cursor.fetchall()
    return match_id_list


def get_min_match_id():
    """
    Get match id to start from in next 'get data' iteration
    :return: last match ID added to our DB or zero if our DB is empty for now
    """
    db = connect_to_db()
    cursor = db.cursor()
    query = """SELECT id FROM dota2"""
    cursor.execute(query)
    matches_list = cursor.fetchone()
    print("min match id: ", min(matches_list))
    if matches_list is None:
        return 0
    else:
        return min(matches_list)


def add_many_to_db(matches_list: list):
    """
    Method is used for adding parsed match detailed data to DB
    :param cursor: cursor
    :param matches_list: list of matches that are to be added to DB
    """
    print("start adding to db")
    db = connect_to_db()
    cursor = db.cursor()
    list_of_matches_parsed = get_list_of_matches_parsed()
    query = """INSERT INTO dota2(
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
        %s, %s, %s)"""

    is_connected = False
    db = connect_to_db()

    if not db:
        while is_connected:
            db = connect_to_db()
            if db:
                is_connected = True
    cursor.executemany(query, matches_list)
    print("success")
