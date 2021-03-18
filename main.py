from api import get_matches, get_team_details_by_id, get_team_rating_by_team_id
from pandas import DataFrame
from time import sleep


details_dict = {
    "id": [],
    "duration": [],
    "start_time": [],
    "radiant_team_id": [],
    "dire_team_id": [],
    "league_id": [],
    "series_id": [],
    "radiant_score": [],
    "dire_score": [],
    "dire_team_rating": [],
    "games_won_by_dire_team": [],
    "games_lost_by_dire_team": [],
    "games_won_by_radiant_team": [],
    "games_lost_by_radiant_team": [],
    "radiant_win": [],
    "radiant_team_rating": []
}


if __name__ == "__main__":
    matches_data = get_matches()
    for num, match in enumerate(matches_data):
        dire_team_details = get_team_details_by_id(match["dire_team_id"])
        radiant_team_details = get_team_details_by_id(match["radiant_team_id"])
        if dire_team_details != '' and radiant_team_details != '':
            radiant_team_id = match["radiant_team_id"]
            dire_team_id = match["dire_team_id"]
            radiant_team_rating = get_team_rating_by_team_id(team_id=radiant_team_id)
            dire_team_rating = get_team_rating_by_team_id(team_id=dire_team_id)

            details_dict["id"].append(match["match_id"])
            details_dict["duration"].append(match["duration"])
            details_dict["start_time"].append(match["start_time"])
            details_dict["radiant_team_id"].append(radiant_team_id)
            details_dict["dire_team_id"].append(dire_team_id)
            details_dict["league_id"].append(match["leagueid"])
            details_dict["series_id"].append(match["series_id"])
            details_dict["radiant_score"].append(match["radiant_score"])
            details_dict["dire_score"].append(match["dire_score"])

            details_dict["dire_team_rating"].append(dire_team_details["rating"])
            details_dict["games_won_by_dire_team"].append(dire_team_details["wins"])
            details_dict["games_lost_by_dire_team"].append(dire_team_details["losses"])
            details_dict["radiant_win"].append(match["radiant_win"])

            details_dict["radiant_team_rating"].append(radiant_team_details["rating"])
            details_dict["games_won_by_radiant_team"].append(radiant_team_details["wins"])
            details_dict["games_lost_by_radiant_team"].append(radiant_team_details["losses"])



            radiant_team_name = match["radiant_name"]
            dire_team_name = match["dire_name"]


            print("parse #{}/ radiant team name: {}/ dire team name: {}"
                  .format(num, radiant_team_name, dire_team_name))
        sleep(1)
    df = DataFrame({
        details_dict
    })
    df.to_excel("dota_data.xlsx")
    print(df)
