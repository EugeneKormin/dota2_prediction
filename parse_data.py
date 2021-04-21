from api import get_matches, get_team_rating_by_team_id, get_team_details_by_id
from numpy import sin, pi
from datetime import datetime
from db import add_many_to_db, get_parsed_match


def parse_time(timestamp_to_parse: float) -> (int, float, float, float):
    """
    Parsing datetime to NN algorithm understanding form (sin)

    :param timestamp_to_parse: (float) # original timestamp from datDota server
    :returns: (int, float, float, float) # list of sins
    """
    date_time = datetime.fromtimestamp(timestamp_to_parse).strftime("%A, %B %d, %Y %I:%M:%S")

    year = int(date_time.split(', ')[2].split(' ')[0])
    day = int(date_time.split(', ')[1].split(' ')[1])
    hour = int(date_time.split(', ')[2].split(' ')[1].split(':')[0])
    min = int(date_time.split(', ')[2].split(' ')[1].split(':')[1])

    day_sin = float(sin(2 * pi * day / 31))
    hour_sin = float(sin(2 * pi * hour / 24))
    min_sin = float(sin(2 * pi * min / 60))

    return year, day_sin, hour_sin, min_sin


def parse_and_add():
    """
    Parse & adding data to DB
    """
    # first iteration is done with less_than_match_id = 0 to get latest match available
    match_id = 0
    params = {"less_than_match_id": match_id}
    # list for temporal data
    match_details_list = []
    matches_list = []

    list_match_id_in_BD = get_parsed_match()
    latest_match_id_in_BD = list_match_id_in_BD[0]
    # we check if enough matches were parsed
    while latest_match_id_in_BD < match_id or match_id == 0:
        # use params from previous iteration or 0 if iteration is first
        matches_data = get_matches(params)
        # update latest parsed match_id to start new iteration from AND
        # list of current matches id because they were added in previous iteration
        latest_match_id_in_current_iteration = matches_data[-1]["match_id"]
        params = {"less_than_match_id": latest_match_id_in_current_iteration}
        list_of_parsed_matches = get_parsed_match()
        for num, match in enumerate(matches_data):
            done = round((num / len(matches_data)) * 100, 4)
            match_id = match["match_id"]
            # check if data about match has already been added to DB
            if match_id not in list_of_parsed_matches:
                radiant_team_id = match["radiant_team_id"]
                dire_team_id = match["dire_team_id"]
                # check if both teams are on outer dataDota server side
                if radiant_team_id is not None and dire_team_id is not None:
                    dire_team_details = get_team_details_by_id(team_id=dire_team_id)
                    radiant_team_details = get_team_details_by_id(team_id=radiant_team_id)

                    dire_team_rating = get_team_rating_by_team_id(team_id=dire_team_id)
                    radiant_team_rating = get_team_rating_by_team_id(team_id=radiant_team_id)
                    # check if outer dataDota server has enough data about teams
                    if (dire_team_details != {} and radiant_team_details != {}) and \
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

                        match_details_list.append("no comments")
                    else:
                        # creating dumb list if check is failed
                        match_details_list = [None] * 51
                        # change first element with match id to keep track of this kind of matches
                        match_details_list[0] = match_id
                        # change last element with comment to keep track of reason for skipping
                        match_details_list += ["not enough data about one of teams"]
                else:
                    # creating dumb list if check is failed
                    match_details_list = [None] * 51
                    # change first element with match id to keep track of this kind of matches
                    match_details_list[0] = match_id
                    # change last element with comment to keep track of reason for skipping
                    match_details_list += ["one of teams is not known enough"]

                # updating current list of matches
                matches_list.append(match_details_list)
                # drop current data from temporal list
                match_details_list = []
            else:
                # no action is required, because match has already been added to DB
                pass

        matches_in_current_iter_count = len(matches_list)

        if matches_in_current_iter_count > 0:
            if matches_in_current_iter_count == 1:
                print("1 match is about to be added to DB")
            else:
                print("{} matches are about to be added to DB".format(matches_in_current_iter_count))
            add_many_to_db(matches_list=matches_list)
            # drop current data from matches list
            matches_list = []
        else:
            print("nothing to add to DB")
