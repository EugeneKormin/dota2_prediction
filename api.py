from requests import get
from json import loads, decoder
from time import sleep


def get_matches(params: dict) -> dict:
    """
    Method for API call creation to DatDota DB to retrieve raw data\n
    :param params: match id to fetch from\n
    :return: raw data
    """
    if params["less_than_match_id"] == 0:
        response = get("https://api.opendota.com/api/proMatches").text
    else:
        response = get("https://api.opendota.com/api/proMatches", params=params).text
    response_dict = loads(response)
    sleep(2)
    return response_dict


def get_team_details_by_id(team_id: int) -> dict:
    """
    Method for retrieving detailed raw data about a team by team's ID\n
    :param team_id: team_id\n
    :return: detailed info / empty dictionary if no info in DatDota DB
    """
    response = get(f"https://api.opendota.com/api/teams/{team_id}".format(team_id=team_id)).text
    sleep(2)
    if response != '':
        response_dict = loads(response)
        return response_dict
    else:
        return {}


def get_team_rating_by_team_id(team_id: int) -> dict:
    """ Method for retrieving detailed raw data about a team by team's ID\n
    :param team_id: team_id\n
    :return: team_rating
    """
    team_rating = {}

    url = f"http://datdota.com/api/teams/{team_id}".format(team_id=team_id)
    try:
        team_rating_info = loads(get(url).text)
        sleep(2)
        # check if any data was returned from datDota server and enough data was returned
        if team_rating_info["data"]["ratings"] != {} and len(team_rating_info["data"]["ratings"]) == 4:
            rating_elo_32 = team_rating_info["data"]["ratings"]["ELO_32"]
            rating_elo_64 = team_rating_info["data"]["ratings"]["ELO_64"]
            rating_glicko_1 = team_rating_info["data"]["ratings"]["GLICKO_1"]
            rating_glicko_2 = team_rating_info["data"]["ratings"]["GLICKO_2"]

            team_rating["ratingELO32_startPeriod"] = rating_elo_32["startPeriod"]
            team_rating["ratingELO64_startPeriod"] = rating_elo_64["startPeriod"]
            team_rating["ratingGLICKO1_startPeriod"] = rating_glicko_1["startPeriod"]
            team_rating["ratingGLICKO2_startPeriod"] = rating_glicko_2["startPeriod"]
            team_rating["ratingELO32_rating"] = rating_elo_32["rating"]
            team_rating["ratingELO64_rating"] = rating_elo_64["rating"]
            team_rating["ratingGLICKO1_rating"] = rating_glicko_1["rating"]
            team_rating["ratingGLICKO2_rating"] = rating_glicko_2["rating"]
            team_rating["ratingELO32_mu"] = rating_elo_32["mu"]
            team_rating["ratingELO64_mu"] = rating_elo_64["mu"]
            team_rating["ratingGLICKO1_mu"] = rating_glicko_1["mu"]
            team_rating["ratingGLICKO2_mu"] = rating_glicko_2["mu"]
            team_rating["ratingELO32_phi"] = rating_elo_32["phi"]
            team_rating["ratingELO64_phi"] = rating_elo_64["phi"]
            team_rating["ratingGLICKO1_phi"] = rating_glicko_1["phi"]
            team_rating["ratingGLICKO2_phi"] = rating_glicko_2["phi"]
            team_rating["ratingELO32_sigma"] = rating_elo_32["sigma"]
            team_rating["ratingELO64_sigma"] = rating_elo_64["sigma"]
            team_rating["ratingGLICKO1_sigma"] = rating_glicko_1["sigma"]
            team_rating["ratingGLICKO2_sigma"] = rating_glicko_2["sigma"]
        else:
            team_rating = {}
    except decoder.JSONDecodeError:
        # return empty dict if no data is returned from outer datDota server
        return {}
    return team_rating
