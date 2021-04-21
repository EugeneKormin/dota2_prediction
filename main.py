from parse_data import parse_and_add
from get_data import get


def main_ETL():
    """
    main ETL function
    """
    #parse_and_add()
    df = get()
    print(df)


main_ETL()
