from configparser import ConfigParser


config = ConfigParser()
config.read("config.ini")
pages = config.getint('values', 'pages')
per_page = config.getint('values', 'per_page')
