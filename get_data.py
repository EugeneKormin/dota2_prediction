from db import connect_to_db
from pandas import DataFrame, read_sql_query


def get() -> DataFrame:
    """
    Get data from DB

    :returns: (DataFrame) # data with all sensible matches
    """
    # establishing connection to mysql DB
    mysql = connect_to_db()
    conn = mysql["conn"]
    cursor = mysql["cursor"]

    # query from pandas library
    query = read_sql_query(
    """
        SELECT 
            * 
        FROM mydb.dota2 
        WHERE comments = 'no comments';
    """,
        conn)
    cursor.execute("""SHOW columns FROM dota2""")
    # get column names for df creation
    columns = [column[0] for column in cursor.fetchall()]
    df = DataFrame(query, columns=columns)
    # deleting useless columns
    del df["id"]
    del df["radiant_score"]
    del df["dire_score"]
    del df["duration"]
    del df["comments"]
    columns_to_str = [
        "year", "hour_sin", "day_sin", "min_sin", "radiant_team_id", "dire_team_id", "league_id", "series_id",
        "games_won_by_dire_team", "games_lost_by_dire_team", "games_won_by_radiant_team", "games_lost_by_radiant_team",
    ]
    for column in columns_to_str:
        df[column + "_str"] = df[column].astype(str)
    return df
