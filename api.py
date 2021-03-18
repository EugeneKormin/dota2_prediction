from requests import get
from json import loads
from numpy import mean
from time import sleep


def get_matches():
    response = get("https://api.opendota.com/api/proMatches").text
    response_dict = loads(response)
    return response_dict


def get_team_details_by_id(team_id):
    response = get(f"https://api.opendota.com/api/teams/{team_id}".format(team_id=team_id)).text
    if response != '':
        response_dict = loads(response)
        return response_dict
    else:
        return ''


def get_team_rating_by_team_id(team_id):
    team_rating = {}

    url = f"http://datdota.com/api/teams/{team_id}".format(team_id=team_id)
    team_rating_info = loads(get(url).text)
    ratingELO32 = team_rating_info["data"]["ratings"]["ELO_32"]
    ratingELO64 = team_rating_info["data"]["ratings"]["ELO_64"]
    ratingGLICKO1 = team_rating_info["data"]["ratings"]["GLICKO_1"]
    ratingGLICKO2 = team_rating_info["data"]["ratings"]["GLICKO_2"]

    team_rating["ratingELO32_startPeriod"] = ratingELO32["startPeriod"]
    team_rating["ratingELO64_startPeriod"] = ratingELO64["startPeriod"]
    team_rating["ratingGLICKO1_startPeriod"] = ratingGLICKO1["startPeriod"]
    team_rating["ratingGLICKO2_startPeriod"] = ratingGLICKO2["startPeriod"]
    team_rating["ratingELO32_rating"] = ratingELO32["rating"]
    team_rating["ratingELO64_rating"]= ratingELO64["rating"]
    team_rating["ratingGLICKO1_rating"] = ratingGLICKO1["rating"]
    team_rating["ratingGLICKO2_rating"] = ratingGLICKO2["rating"]
    team_rating["ratingELO32_mu"] = ratingELO32["mu"]
    team_rating["ratingELO64_mu"] = ratingELO64["mu"]
    team_rating["team_rating"] = ratingGLICKO1["mu"]
    team_rating["ratingGLICKO2_mu"] = ratingGLICKO2["mu"]
    team_rating["ratingELO32_phi"] = ratingELO32["phi"]
    team_rating["ratingELO64_phi"] = ratingELO64["phi"]
    team_rating["ratingGLICKO1_phi"] = ratingGLICKO1["phi"]
    team_rating["ratingGLICKO2_phi"] = ratingGLICKO2["phi"]
    team_rating["ratingELO32_sigma"] = ratingELO32["sigma"]
    team_rating["ratingELO64_sigma"] = ratingELO64["sigma"]
    team_rating["ratingGLICKO1_sigma"] = ratingGLICKO1["sigma"]
    team_rating["ratingGLICKO2_sigma"] = ratingGLICKO2["sigma"]
    return team_rating
