from parse_data import parse_and_add
from get_data import get


# TODO estimate how much to wait until adding is completed. (max match_id - min_match_id) / latest_current_match_id


def main_ETL():
    """
    main function
    """
    parse_and_add()
    df = get()
    print(df)


main_ETL()
