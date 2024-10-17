import configparser

def config(filename='database.ini', section='postgresql'):
    parser = configparser.ConfigParser()
    with open(filename, 'r', encoding='utf-8') as f:
        parser.read_file(f)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} is not found in the {filename} file.')

    return db
