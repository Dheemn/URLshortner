
import configparser

class ConfigParse():

    def __init__(self, configPath):
        self._cP = configparser.ConfigParser()
        self._cP.read(configPath)

    def readDB(self):
        #Parses the config file for database and returns as a dictionary
        db = self._cP['DATABASE']
        dbType = db['dbType']
        if ( dbType == 'postgresql' ):
            dbDetails = { 'dbType': dbType,
                    'dbName': db['dbName'],
                    'username': db['username'],
                    'password': db['password']}
            return dbDetails
        elif ( dbType == 'sqlite' ):
            dbDetails = { 'dbType': dbType,
                    'dbLoc': db['dbLoc']}
            return dbDetails


    def readCommon(self):
        #Parses the config file for common configurations
        common = self._cP['Common']
        cDetails = {'serverHost': common['host']}
        return cDetails
