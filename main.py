from parse_data import parse
from get_data import get


MATCHES_PARSED = 0
match_details_list = []


# TODO create decorator for 'connect_to_db' function in 'db.py' module.
#      Decorator will check if connection is established. If so return db, if not reconnect

# TODO make class for current match

if __name__ == "__main__":
    parse()
    df = get()
    print(df)
