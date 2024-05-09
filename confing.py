from configparser import ConfigParser

API_HH_RU_VACANCIES = 'https://api.hh.ru/vacancies'
API_HH_RU_EMPLOYERS = 'https://api.hh.ru/employers'


def config(filename="connect_db.ini", section="postgresql"):
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
