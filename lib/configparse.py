
import configparser
from typing import (
    Dict,
    Optional,
)


class ConfigParse():

    def __init__(self, config_path) -> object:
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(config_path)

    def read_database(self) -> Dict[str, str, Optional[str], Optional[str]]:
        # Parses the config file for database and returns as a dictionary
        database = self._config_parser['DATABASE']
        db_type = database['dbType']
        if db_type == 'postgresql':
            db_details = {
                'dbType': db_type,
                'dbName': database['dbName'],
                'username': database['username'],
                'password': database['password'],
            }
            return db_details
        elif db_type == 'sqlite':
            db_details = {
                'dbType': db_type,
                'dbLoc': database['dbLoc'],
            }
            return db_details

    def read_common(self) -> Dict[str]:
        # Parses the config file for common configurations
        common = self._config_parser['Common']
        common_details = {'serverHost': common['host']}
        return common_details
