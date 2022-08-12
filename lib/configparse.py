
import configparser
from typing import Dict


class ConfigParse():
    """
    Parses the configuration file to get the various settings

    Params:
    config_path: the path to the configuration file

    P.S - Don't write anything within quotes in the config file
            It won't be recognized and the methods will return None
    """

    def __init__(self, config_path):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(config_path)

    def read_database(self) -> Dict[str, str]:
        """
        Parses the config file for database details and returns the output as
        a dictionary

        Params:
        None
        """
        database = self._config_parser['DATABASE']
        db_type = database['dbType']
        if db_type == 'postgresql':
            db_details = {
                'dbType': db_type,
                'dbName': database['dbName'],
                'username': database['username'],
                'password': database['password'],
                'host': database['host'],
                'port': database['port'],
            }
            return db_details
        elif db_type == 'sqlite':
            db_details = {
                'dbType': db_type,
                'dbLoc': database['dbLoc'],
            }
            return db_details

    def read_common(self) -> Dict[str, str]:
        """
        Reads the common configs such as listening IP address and such and
        and returns the output as an dictionary

        Params:
        None
        """
        # Parses the config file for common configurations
        common = self._config_parser['Common']
        common_details = {'serverHost': common['host']}
        return common_details
