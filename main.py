from parse_data import parse_and_add
from get_data import get
from parsing import Parsing


def main_ETL():
    """
    main ETL function
    """
    #parse_and_add()
    #df = get()
    Parsing(match_id=MATCH_ID)


MATCH_ID = "5965367985"

main_ETL()
