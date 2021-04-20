from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")

host = config.get('DB', 'host')
user = config.get('DB', 'user')
passwd = config.get('DB', 'passwd')
db_name = config.get('DB', 'db_name')
