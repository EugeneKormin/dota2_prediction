from api import get_matches, get_team_details_by_id, get_team_rating_by_team_id
from time import sleep
from numpy import sin, pi
from datetime import datetime
from db import add_to_db


def parse_time(date_time_to_parse):
    date_time = datetime.fromtimestamp(date_time_to_parse).strftime("%A, %B %d, %Y %I:%M:%S")

    year = int(date_time.split(', ')[2].split(' ')[0])
    day = int(date_time.split(', ')[1].split(' ')[1])
    hour = int(date_time.split(', ')[2].split(' ')[1].split(':')[0])
    min = int(date_time.split(', ')[2].split(' ')[1].split(':')[1])

    day_sin = sin(2 * pi * day / 31)
    hour_sin = sin(2 * pi * hour / 24)
    min_sin = sin(2 * pi * min / 60)

    return year, day_sin, hour_sin, min_sin


def run(cursor, details_list, params):
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
                details_list.append(match["match_id"])

                details_list.append(match["duration"])
                time_to_parse = match["start_time"]
                parsed_date = parse_time(time_to_parse)
                details_list.append(parsed_date[0])
                details_list.append(parsed_date[1])
                details_list.append(parsed_date[2])
                details_list.append(parsed_date[3])

                details_list.append(radiant_team_id)
                details_list.append(dire_team_id)

                details_list.append(match["leagueid"])
                details_list.append(match["series_id"])

                details_list.append(match["radiant_score"])
                details_list.append(match["dire_score"])

                details_list.append(match["radiant_win"])

                details_list.append(dire_team_details["rating"])
                details_list.append(radiant_team_details["rating"])

                details_list.append(dire_team_details["wins"])
                details_list.append(dire_team_details["losses"])
                details_list.append(radiant_team_details["wins"])
                details_list.append(radiant_team_details["losses"])

                details_list.append(radiant_team_rating["ratingELO32_rating"])
                details_list.append(radiant_team_rating["ratingELO64_rating"])
                details_list.append(radiant_team_rating["ratingGLICKO1_rating"])
                details_list.append(radiant_team_rating["ratingGLICKO2_rating"])

                details_list.append(radiant_team_rating["ratingELO32_mu"])
                details_list.append(radiant_team_rating["ratingELO64_mu"])
                details_list.append(radiant_team_rating["ratingGLICKO1_mu"])
                details_list.append(radiant_team_rating["ratingGLICKO2_mu"])

                details_list.append(radiant_team_rating["ratingELO32_phi"])
                details_list.append(radiant_team_rating["ratingELO64_phi"])
                details_list.append(radiant_team_rating["ratingGLICKO1_phi"])
                details_list.append(radiant_team_rating["ratingGLICKO2_mu"])

                details_list.append(radiant_team_rating["ratingELO32_sigma"])
                details_list.append(radiant_team_rating["ratingELO64_sigma"])
                details_list.append(radiant_team_rating["ratingGLICKO1_sigma"])
                details_list.append(radiant_team_rating["ratingGLICKO2_sigma"])

                details_list.append(dire_team_rating["ratingELO32_rating"])
                details_list.append(dire_team_rating["ratingELO64_rating"])
                details_list.append(dire_team_rating["ratingGLICKO1_rating"])
                details_list.append(dire_team_rating["ratingGLICKO2_rating"])

                details_list.append(dire_team_rating["ratingELO32_mu"])
                details_list.append(dire_team_rating["ratingELO64_mu"])
                details_list.append(dire_team_rating["ratingGLICKO1_mu"])
                details_list.append(dire_team_rating["ratingGLICKO2_mu"])

                details_list.append(dire_team_rating["ratingELO32_phi"])
                details_list.append(dire_team_rating["ratingELO64_phi"])
                details_list.append(dire_team_rating["ratingGLICKO1_phi"])
                details_list.append(dire_team_rating["ratingGLICKO2_mu"])

                details_list.append(dire_team_rating["ratingELO32_sigma"])
                details_list.append(dire_team_rating["ratingELO64_sigma"])
                details_list.append(dire_team_rating["ratingGLICKO1_sigma"])
                details_list.append(dire_team_rating["ratingGLICKO2_sigma"])

                add_to_db(cursor, details_list)

                print("match id: {match_id}/ {dire_name} vs. {radiant_name} Parsed"
                      .format(match_id=match["match_id"],
                              dire_name=match["dire_name"],
                              radiant_name=match["radiant_name"]))
        sleep(1)
    print(min(details_list[0]))
    params = {"less_than_match_id": min(details_list[0])}
    return details_list, params
