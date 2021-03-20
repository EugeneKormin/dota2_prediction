from parse_data import run
from pandas import DataFrame
from filenames import get_min_match_id, get_all_matches_parsed_so_far
from db import connect_to_db


matches_parsed = 0

details_list = []

try:
    last_match_id = get_min_match_id()
except:
    last_match_id = 0

params = {"less_than_match_id": last_match_id}


def parse(details_list, params):
        cursor = connect_to_db()
        details_list = []
        details_list, params = run(
            cursor=cursor,
            details_list=details_list,
            params=params)
        matches_parsed = get_all_matches_parsed_so_far()
        matches_left = 5000 - matches_parsed
        Last_match_id = params["less_than_match_id"]
        print(f"matches left: {matches_left}"
              .format(matches_left=matches_left))

        details_list = []
        params = {"less_than_match_id": Last_match_id}
        return details_list, params


if __name__ == "__main__":
    while matches_parsed < 5000:
        details_list, params = parse(details_list, params)
