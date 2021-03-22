from parse_data import run
from pandas import DataFrame
from db import connect_to_db, get_min_match_id
from requests.exceptions import ConnectionError


MATCHES_PARSED = 0
match_details_list = []
cursor = connect_to_db()


def main():
    """
    main ETL algorithm
    """
    try:
        last_match_id = get_min_match_id(cursor=cursor)
        params = {"less_than_match_id": last_match_id}
        run(cursor=cursor, params=params)

    except ConnectionError:
        # if 100 matches has not been parsed because of connection then retry
        main()


if __name__ == "__main__":
    while MATCHES_PARSED < 5000:
        main()
