from api import get_matches, get_team_details_by_id, get_team_rating_by_team_id
from time import sleep


def run(details_dict, params):
    matches_data = get_matches(params)
    for num, match in enumerate(matches_data):
        radiant_team_id = match["radiant_team_id"]
        dire_team_id = match["dire_team_id"]

        if radiant_team_id is not None and dire_team_id is not None:
            dire_team_details = get_team_details_by_id(team_id=dire_team_id)
            radiant_team_details = get_team_details_by_id(team_id=radiant_team_id)

            dire_team_rating = get_team_rating_by_team_id(team_id=dire_team_id)
            radiant_team_rating = get_team_rating_by_team_id(team_id=radiant_team_id)

            if (dire_team_details != '' and radiant_team_details != '') and \
                    (radiant_team_rating != {} and dire_team_rating != {}):
                details_dict["id"].append(match["match_id"])

                details_dict["duration"].append(match["duration"])
                details_dict["start_time"].append(match["start_time"])

                details_dict["radiant_team_id"].append(radiant_team_id)
                details_dict["dire_team_id"].append(dire_team_id)

                details_dict["league_id"].append(match["leagueid"])
                details_dict["series_id"].append(match["series_id"])

                details_dict["radiant_score"].append(match["radiant_score"])
                details_dict["dire_score"].append(match["dire_score"])

                details_dict["radiant_win"].append(match["radiant_win"])

                details_dict["dire_team_rating"].append(dire_team_details["rating"])
                details_dict["radiant_team_rating"].append(radiant_team_details["rating"])

                details_dict["games_won_by_dire_team"].append(dire_team_details["wins"])
                details_dict["games_lost_by_dire_team"].append(dire_team_details["losses"])
                details_dict["games_won_by_radiant_team"].append(radiant_team_details["wins"])
                details_dict["games_lost_by_radiant_team"].append(radiant_team_details["losses"])

                details_dict["radiant_team_elo32_rating"].append(radiant_team_rating["ratingELO32_rating"])
                details_dict["radiant_team_elo64_rating"].append(radiant_team_rating["ratingELO64_rating"])
                details_dict["radiant_team_glicko1_rating"].append(radiant_team_rating["ratingGLICKO1_rating"])
                details_dict["radiant_team_glicko2_rating"].append(radiant_team_rating["ratingGLICKO2_rating"])

                details_dict["radiant_team_elo32_mu"].append(radiant_team_rating["ratingELO32_mu"])
                details_dict["radiant_team_elo64_mu"].append(radiant_team_rating["ratingELO64_mu"])
                details_dict["radiant_team_glicko1_mu"].append(radiant_team_rating["ratingGLICKO1_mu"])
                details_dict["radiant_team_glicko2_mu"].append(radiant_team_rating["ratingGLICKO2_mu"])

                details_dict["radiant_team_elo32_phi"].append(radiant_team_rating["ratingELO32_phi"])
                details_dict["radiant_team_elo64_phi"].append(radiant_team_rating["ratingELO64_phi"])
                details_dict["radiant_team_glicko1_phi"].append(radiant_team_rating["ratingGLICKO1_phi"])
                details_dict["radiant_team_glicko2_phi"].append(radiant_team_rating["ratingGLICKO2_mu"])

                details_dict["radiant_team_elo32_sigma"].append(radiant_team_rating["ratingELO32_sigma"])
                details_dict["radiant_team_elo64_sigma"].append(radiant_team_rating["ratingELO64_sigma"])
                details_dict["radiant_team_glicko1_sigma"].append(radiant_team_rating["ratingGLICKO1_sigma"])
                details_dict["radiant_team_glicko2_sigma"].append(radiant_team_rating["ratingGLICKO2_sigma"])

                details_dict["dire_team_elo32_rating"].append(dire_team_rating["ratingELO32_rating"])
                details_dict["dire_team_elo64_rating"].append(dire_team_rating["ratingELO64_rating"])
                details_dict["dire_team_glicko1_rating"].append(dire_team_rating["ratingGLICKO1_rating"])
                details_dict["dire_team_glicko2_rating"].append(dire_team_rating["ratingGLICKO2_rating"])

                details_dict["dire_team_elo32_mu"].append(dire_team_rating["ratingELO32_mu"])
                details_dict["dire_team_elo64_mu"].append(dire_team_rating["ratingELO64_mu"])
                details_dict["dire_team_glicko1_mu"].append(dire_team_rating["ratingGLICKO1_mu"])
                details_dict["dire_team_glicko2_mu"].append(dire_team_rating["ratingGLICKO2_mu"])

                details_dict["dire_team_elo32_phi"].append(dire_team_rating["ratingELO32_phi"])
                details_dict["dire_team_elo64_phi"].append(dire_team_rating["ratingELO64_phi"])
                details_dict["dire_team_glicko1_phi"].append(dire_team_rating["ratingGLICKO1_phi"])
                details_dict["dire_team_glicko2_phi"].append(dire_team_rating["ratingGLICKO2_mu"])

                details_dict["dire_team_elo32_sigma"].append(dire_team_rating["ratingELO32_sigma"])
                details_dict["dire_team_elo64_sigma"].append(dire_team_rating["ratingELO64_sigma"])
                details_dict["dire_team_glicko1_sigma"].append(dire_team_rating["ratingGLICKO1_sigma"])
                details_dict["dire_team_glicko2_sigma"].append(dire_team_rating["ratingGLICKO2_sigma"])

                print("match id: {match_id}/ {dire_name} vs. {radiant_name} Parsed"
                      .format(match_id=match["match_id"],
                              dire_name=match["dire_name"],
                              radiant_name=match["radiant_name"]))
        sleep(1)
    print(min(details_dict["id"]))
    params = {"less_than_match_id": min(details_dict["id"])}
    return details_dict, params
