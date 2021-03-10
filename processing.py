from requests import get
import json
from pandas import DataFrame, read_excel, concat

match_id_list = []
radiant_team_id_list = []
radiant_name_list = []
dire_team_id_list = []
dire_name_list = []
league_id_list = []
league_name_list = []
series_id_list = []
series_type_list = []
radiant_score_list = []
dire_score_list = []
radiant_win_list = []


class Run(object):
    def __init__(self):
        self.last_match_id = 0
        self.matches_parsed = 0
        initial_parsing = "https://api.opendota.com/api/proMatches"
        continuing_parsing = "https://api.opendota.com/api/proMatches?less_than_match_id="

        data = self.get_data(initial_parsing)
        self.parsing_data(data)
        self.df_creation()

        while self.matches_parsed <= 5000:
            print(self.matches_parsed)
            data = self.get_data(continuing_parsing)
            self.parsing_data(data)
            self.df_creation()

    def get_data(self, url_to_parse):
        if "less_than_match_id" in url_to_parse:
            url_to_parse = url_to_parse + str(self.last_match_id)
        response = get(url_to_parse).text
        data = json.loads(response)
        return data

    @staticmethod
    def parsing_data(data):
        for a_piece_of_data in data:
            match_id_list.append(a_piece_of_data["match_id"])
            radiant_team_id_list.append(a_piece_of_data["radiant_team_id"])
            radiant_name_list.append(a_piece_of_data["radiant_name"])
            dire_team_id_list.append(a_piece_of_data["dire_team_id"])
            dire_name_list.append(a_piece_of_data["dire_name"])
            league_id_list.append(a_piece_of_data["leagueid"])
            league_name_list.append(a_piece_of_data["league_name"])
            series_id_list.append(a_piece_of_data["series_id"])
            series_type_list.append(a_piece_of_data["series_type"])
            radiant_score_list.append(a_piece_of_data["radiant_score"])
            dire_score_list.append(a_piece_of_data["dire_score"])
            radiant_win_list.append(a_piece_of_data["radiant_win"])

    def df_creation(self):
        try:
            df_old = read_excel("matches.csv")
        except FileNotFoundError:
            df_old = DataFrame({})
        df_new = DataFrame({
            "match_id": match_id_list,
            "radiant_team_id": radiant_team_id_list,
            "radiant_name_list": radiant_name_list,
            "dire_team_id": radiant_team_id_list,
            "dire_name": dire_name_list,
            "league_id": league_id_list,
            "league_name": league_name_list,
            "series_id": series_id_list,
            "series_name": series_type_list,
            "dire_score": dire_score_list,
            "radiant_win": radiant_win_list
        })
        if df_old.shape[0] == 0:
            df = df_new
        else:
            df = concat([df_old, df_new], ignore_index=True)
        self.last_match_id = df.iloc[-1]["match_id"]
        self.matches_parsed = df.shape[0]
        df.to_csv("matches.xlsx")


