from api import get_matches, get_team_rating_by_team_id, get_team_details_by_id
from numpy import sin, pi
from datetime import datetime
from db import add_many_to_db, get_parsed_match


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


def parse():
    """
    Parse & adding data to DB
    :param cursor: cursor
    :param params: match id to start fetching from
    """
    # first iteration is done with less_than_match_id = 0 to get latest match available
    match_id = 0
    params = {"less_than_match_id": match_id}
    # list for temporal data
    match_details_list = []
    matches_list = []

    latest_match_id_in_BD = get_parsed_match(details="first")
    # we check if enough matches were parsed
    while latest_match_id_in_BD < match_id or match_id == 0:
        # use params from previous iteration or 0 if iteration is first
        matches_data = get_matches(params)
        # update latest parsed match_id to start new iteration from AND
        # list of current matches id because they were added in previous iteration
        latest_match_id_in_current_iteration = matches_data[-1]["match_id"]
        print("latest current match id: {}".format(latest_match_id_in_current_iteration))
        params = {"less_than_match_id": latest_match_id_in_current_iteration}
        list_of_parsed_matches = get_parsed_match(details="all")
        print("---***---")
        for num, match in enumerate(matches_data):
            done = round((num / len(matches_data)) * 100, 2)
            print("done: {}%".format(done))
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
                    if (dire_team_details != '' and radiant_team_details != '') and \
                            (radiant_team_rating != {} and dire_team_rating != {}):
                        print("passed. Both teams have enough statistics data\n"
                              "parsing: {match_id}".format(match_id=match["match_id"]))

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
                        print("check Failed. Not enough data about one of teams")
                        # creating dumb list if check is failed
                        match_details_list = [None] * 51
                        # change first element with match id to keep track of this kind of matches
                        match_details_list[0] = match_id
                        # change last element with comment to keep track of reason for skipping
                        match_details_list += ["not enough data about one of teams"]
                else:
                    print("check Failed. One of teams is not known enough")
                    # creating dumb list if check is failed
                    match_details_list = [None] * 51
                    # change first element with match id to keep track of this kind of matches
                    match_details_list[0] = match_id
                    # change last element with comment to keep track of reason for skipping
                    match_details_list += "one of teams is not known enough"

                # updating current list of matches
                matches_list.append(match_details_list)
                # drop current data from temporal list
                match_details_list = []
            else:
                # no action is required, because match has already been added to DB
                print("Failed. Match is in DB")

            print("---***---")
        add_many_to_db(matches_list=matches_list)

        MATCHES_PARSED_TOTAL = len(get_parsed_match(details="all"))
        MATCHES_LEFT = 15000 - MATCHES_PARSED_TOTAL

        print(f"matches left: {MATCHES_LEFT}\\matches parsed total: {MATCHES_PARSED_TOTAL}"
              .format(MATCHES_LEFT=MATCHES_LEFT, MATCHES_PARSED_TOTAL=MATCHES_PARSED_TOTAL))
