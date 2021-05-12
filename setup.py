#!/usr/bin/env python3

import configparser
import getpass
import os
import sys

def configWrite(common, dbdetails):
    configP = configparser.ConfigParser()
    configP['Common'] = common
    configP['DATABASE'] = dbdetails
    with open('config.ini', 'w') as configFile:
        configP.write(configFile)

def main():
    choice = sys.argv[1]
    if ( choice == 1 ):
        import psycopg2
        host = str(input("Should the 1)server be hosted public facing(0.0.0.0) or 2)server should be hosted locally(localhost): "))
        dbhost = str(input("Enter hostname for PostgreSQL server. Press ENTER for default(Default is localhost): "))
        if not dbhost:
            dbhost = ''
        dbport = str(input("Enter port for PostgreSQL server. Press ENTER for default(Default is 5432): "))
        dbname = str(input("Enter database name if created. Press ENTER for default(Default is urlshortner): "))
        uname = str(input("Enter username for PostgreSQL server. Press ENTER for default(Default will be your username): "))
        password = str(input("Enter password for PostgreSQL server: "))
        if not dbport:
            dbport = 5432
        
        if not dbname: 
            dbname = urlshortner
        
        if not uname:
            uname = getpass.getuser()

        common = {'host': host }
        dbDetails = { 'dbType': 'postgresql',
                'dbName': dbname,
                'username': uname,
                'password': password,
                'host': dbhost,
                'port': dbport }
        
        os.system("sudo -u postgres psql -c 'create database %s'", (dbname))
        os.system("sudo -u postgres psql -c 'create user %s with encrypted password %s'", (uname, password))
        os.system("sudo -u postgres psql -c 'grant all privileges on database %s to %s'", (dbname, uname))

        conn = psycopg2.connect( database =dbname, user=uname, password=password)
        cur = conn.cursor()
        cur.execute("create table urlshortner(time timestamp not null, path varchar(6) primary key, link text);")
        conn.commit()
        cur.close()
        conn.close()
        print("[+]Writing to config file....")
        configWrite(common, dbDetails)
        print("[+]Done writing to config file")
    elif ( choice == 2 ):
        import sqlite3
        host = str(input("Should the 1)server be hosted public facing(0.0.0.0) or 2)server should be hosted locally(localhost): "))
        if ( host == '1' ):
            host='0.0.0.0'
        elif ( host == '2' ):
            host='localhost'
        dbname = str(input("Enter the name of the database you want to give. Press ENTER for default(Default is database): "))
        if not dbname:
            dbname = "database.db"
        else:
            dbname = dbname+'.db'

        if ( getpass.getuser() == 'root' ):
            dbLoc = "/root/.config/urlshortner/" + dbname
        else:
            userName = getpass.getuser()
            dbLoc = "/home/"+userName+"/.config/"+dbname

        common = { 'host': host }
        dbDetails = { 'dbType': 'sqlite',
                'dbLoc': dbLoc }

        conn = sqlite3.connect(dbLoc)
        cur = conn.cursor()
        cur.execute("create table urlshorter(time TEXT, path varchar(6) primary key, link TEXT);")
        conn.commit()
        cur.close()
        conn.close()
        print("[+]Writing configuration to config file...")
        configWrite(common, dbDetails)
        print("[+]Done...!!")

if __name__ == "__main__":
    main()
