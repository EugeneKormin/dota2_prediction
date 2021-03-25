from parse_data import parse
from db import get_min_match_id
from requests.exceptions import ConnectionError
from get_data import get


MATCHES_PARSED = 0
match_details_list = []


def main():
    """
    main ETL algorithm
    """
    try:
        last_match_id = get_min_match_id()
        params = {"less_than_match_id": last_match_id}
        parse(params=params)

    except ConnectionError:
        # if 100 matches has not been parsed because of connection then retry
        main()


if __name__ == "__main__":
    df = get()
    print(df)
