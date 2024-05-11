import os
from configparser import ConfigParser


root_gir = os.path.dirname(__file__)
API_HH_RU_VACANCIES = 'https://api.hh.ru/vacancies'
API_HH_RU_EMPLOYERS = 'https://api.hh.ru/employers'
DIR_CONFIG_CONNECT = os.path.join(root_gir, 'connect_db.ini')


def config_connectdb(filename=DIR_CONFIG_CONNECT, section="postgresql"):
    print(filename)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db



