from api import get_matches, get_team_rating_by_team_id, get_team_details_by_id
from numpy import sin, pi
from datetime import datetime
from db import add_many_to_db, get_list_of_matches_parsed


def parse_time(date_time_to_parse):
    """
    Parsing datetime to algorithm understanding form (sin)
    :param date_time_to_parse:
    :return: list of sin
    """
    date_time = datetime.fromtimestamp(date_time_to_parse).strftime("%A, %B %d, %Y %I:%M:%S")

    year = int(date_time.split(', ')[2].split(' ')[0])
    day = int(date_time.split(', ')[1].split(' ')[1])
    hour = int(date_time.split(', ')[2].split(' ')[1].split(':')[0])
    min = int(date_time.split(', ')[2].split(' ')[1].split(':')[1])

    day_sin = sin(2 * pi * day / 31)
    hour_sin = sin(2 * pi * hour / 24)
    min_sin = sin(2 * pi * min / 60)

    return year, day_sin, hour_sin, min_sin


def parse(params: dict):
    """
    Parse & adding data to DB
    :param cursor: cursor
    :param params: match id to start fetching from
    """
    match_details_list = []
    matches_list = []
    # TODO while latest match in BD is not reached do parse (check if is in BD else parse)
    matches_data = get_matches(params)
    list_of_parsed_matches = get_list_of_matches_parsed()
    for num, match in enumerate(matches_data):
        match_id = match["match_id"]
        params = {"less_than_match_id": match_id}
        if match_id not in list_of_parsed_matches:
            print("parsing: {match_id}".format(match_id=match["match_id"]))
            radiant_team_id = match["radiant_team_id"]
            dire_team_id = match["dire_team_id"]

            if radiant_team_id is not None and dire_team_id is not None:
                dire_team_details = get_team_details_by_id(team_id=dire_team_id)
                radiant_team_details = get_team_details_by_id(team_id=radiant_team_id)

                dire_team_rating = get_team_rating_by_team_id(team_id=dire_team_id)
                radiant_team_rating = get_team_rating_by_team_id(team_id=radiant_team_id)

                if (dire_team_details != '' and radiant_team_details != '') and \
                        (radiant_team_rating != {} and dire_team_rating != {}):
                    match_details_list.append(match["match_id"])

                    match_details_list.append(match["duration"])
                    time_to_parse = match["start_time"]
                    parsed_date = parse_time(time_to_parse)
                    match_details_list.append(parsed_date[0])
                    match_details_list.append(parsed_date[1])
                    match_details_list.append(parsed_date[2])
                    match_details_list.append(parsed_date[3])

                    match_details_list.append(radiant_team_id)
                    match_details_list.append(dire_team_id)

                    match_details_list.append(match["leagueid"])
                    match_details_list.append(match["series_id"])

                    match_details_list.append(match["radiant_score"])
                    match_details_list.append(match["dire_score"])

                    match_details_list.append(match["radiant_win"])

                    match_details_list.append(dire_team_details["rating"])
                    match_details_list.append(radiant_team_details["rating"])

                    match_details_list.append(dire_team_details["wins"])
                    match_details_list.append(dire_team_details["losses"])
                    match_details_list.append(radiant_team_details["wins"])
                    match_details_list.append(radiant_team_details["losses"])

                    match_details_list.append(radiant_team_rating["ratingELO32_rating"])
                    match_details_list.append(radiant_team_rating["ratingELO64_rating"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO1_rating"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO2_rating"])

                    match_details_list.append(radiant_team_rating["ratingELO32_mu"])
                    match_details_list.append(radiant_team_rating["ratingELO64_mu"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO1_mu"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO2_mu"])

                    match_details_list.append(radiant_team_rating["ratingELO32_phi"])
                    match_details_list.append(radiant_team_rating["ratingELO64_phi"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO1_phi"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO2_mu"])

                    match_details_list.append(radiant_team_rating["ratingELO32_sigma"])
                    match_details_list.append(radiant_team_rating["ratingELO64_sigma"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO1_sigma"])
                    match_details_list.append(radiant_team_rating["ratingGLICKO2_sigma"])

                    match_details_list.append(dire_team_rating["ratingELO32_rating"])
                    match_details_list.append(dire_team_rating["ratingELO64_rating"])
                    match_details_list.append(dire_team_rating["ratingGLICKO1_rating"])
                    match_details_list.append(dire_team_rating["ratingGLICKO2_rating"])

                    match_details_list.append(dire_team_rating["ratingELO32_mu"])
                    match_details_list.append(dire_team_rating["ratingELO64_mu"])
                    match_details_list.append(dire_team_rating["ratingGLICKO1_mu"])
                    match_details_list.append(dire_team_rating["ratingGLICKO2_mu"])

                    match_details_list.append(dire_team_rating["ratingELO32_phi"])
                    match_details_list.append(dire_team_rating["ratingELO64_phi"])
                    match_details_list.append(dire_team_rating["ratingGLICKO1_phi"])
                    match_details_list.append(dire_team_rating["ratingGLICKO2_mu"])

                    match_details_list.append(dire_team_rating["ratingELO32_sigma"])
                    match_details_list.append(dire_team_rating["ratingELO64_sigma"])
                    match_details_list.append(dire_team_rating["ratingGLICKO1_sigma"])
                    match_details_list.append(dire_team_rating["ratingGLICKO2_sigma"])

                    matches_list.append(match_details_list)
                    match_details_list = []
        else:
            print("{match_id} is in DB".format(match_id=match["match_id"]))

    add_many_to_db(matches_list=matches_list)

    MATCHES_PARSED_TOTAL = len(get_list_of_matches_parsed())
    MATCHES_LEFT = 15000 - MATCHES_PARSED_TOTAL

    print(f"matches left: {MATCHES_LEFT}\\matches parsed total: {MATCHES_PARSED_TOTAL}"
          .format(MATCHES_LEFT=MATCHES_LEFT, MATCHES_PARSED_TOTAL=MATCHES_PARSED_TOTAL))
