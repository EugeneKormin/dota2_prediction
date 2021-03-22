from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")
BATCHES_FOR_ADDING_TO_DB = config.getint('values', 'batches_for_adding_to_DB')
