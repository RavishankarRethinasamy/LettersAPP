from config_file import ConfigFile, ParsingError

try:
    args = ConfigFile("/etc/letters/letters.ini")
except ParsingError as e:
    raise Exception(e)
except ValueError as v:
    raise Exception(v)
except FileNotFoundError:
    raise Exception("File does not exist")
