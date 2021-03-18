from parse_data import run
from pandas import DataFrame


matches_parsed = 0

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
    "radiant_team_rating": [],
    "radiant_team_elo32_rating": [],
    "radiant_team_elo64_rating": [],
    "radiant_team_glicko1_rating": [],
    "radiant_team_glicko2_rating": [],
    "radiant_team_elo32_mu": [],
    "radiant_team_elo64_mu": [],
    "radiant_team_glicko1_mu": [],
    "radiant_team_glicko2_mu": [],
    "radiant_team_elo32_phi": [],
    "radiant_team_elo64_phi": [],
    "radiant_team_glicko1_phi": [],
    "radiant_team_glicko2_phi": [],
    "radiant_team_elo32_sigma": [],
    "radiant_team_elo64_sigma": [],
    "radiant_team_glicko1_sigma": [],
    "radiant_team_glicko2_sigma": [],
    "dire_team_elo32_rating": [],
    "dire_team_elo64_rating": [],
    "dire_team_glicko1_rating": [],
    "dire_team_glicko2_rating": [],
    "dire_team_elo32_mu": [],
    "dire_team_elo64_mu": [],
    "dire_team_glicko1_mu": [],
    "dire_team_glicko2_mu": [],
    "dire_team_elo32_phi": [],
    "dire_team_elo64_phi": [],
    "dire_team_glicko1_phi": [],
    "dire_team_glicko2_phi": [],
    "dire_team_elo32_sigma": [],
    "dire_team_elo64_sigma": [],
    "dire_team_glicko1_sigma": [],
    "dire_team_glicko2_sigma": [],
}

last_match_id = 0
params = {"less_than_match_id": last_match_id}

if __name__ == "__main__":
    while matches_parsed < 5000:
        details_dict, params = run(details_dict=details_dict, params=params)
        matches_parsed = len(details_dict["id"])
        print(f"matches_parsed: {matches_parsed}"
              .format(matches_parsed=matches_parsed))

    df = DataFrame(details_dict)
    df.to_excel("dota_data.xlsx")
