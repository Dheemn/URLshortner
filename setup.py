#!/usr/bin/env python3

import configparser
import getpass
import os
import sqlite3
import sys

import psycopg2


def config_write(common, db_details) -> None:
    """
    The config_write method writes the general details such as hosting and
    database details
    @params:\n
    common - contains the server accessiblity such as whether its on localhost
                etc
    db_details - contains all the database details such as its location, port
                number, etc
    """
    config_parser = configparser.ConfigParser()
    config_parser['Common'] = common
    config_parser['DATABASE'] = db_details
    with open('config.ini', 'w', encoding='utf-8') as config_file:
        config_parser.write(config_file)


def main():
    """
    The main function
    @params:
    None
    """
    choice = sys.argv[1]
    if (choice == 1):
        host = str(input("Should the 1)server be hosted public facing(0.0.0" +
                         ".0) or 2)server should be hosted locally" +
                         "(localhost): "))
        dbhost = str(input("Enter hostname for PostgreSQL server. Press " +
                           "ENTER for default(Default is localhost): "))
        if not dbhost:
            dbhost = ''
        dbport = str(input("Enter port for PostgreSQL server. Press ENTER" +
                           " for default(Default is 5432): "))
        dbname = str(input("Enter database name if created. Press ENTER " +
                           "for default(Default is urlshortner): "))
        uname = str(input("Enter username for PostgreSQL server. Press " +
                          "ENTER for default(Default will be your " +
                          "username): "))
        password = str(input("Enter password for PostgreSQL server: "))

        if not dbport:
            dbport = 5432
        if not dbname:
            dbname = "urlshortner"
        if not uname:
            uname = getpass.getuser()

        common = {'host': host}
        db_details = {
            'dbType': 'postgresql',
            'dbName': dbname,
            'username': uname,
            'password': password,
            'host': dbhost,
            'port': dbport,
        }

        os.system(f"sudo -u postgres psql -c 'create database {dbname}'")
        os.system(f"sudo -u postgres psql -c 'create user {uname} with" +
                  f" encrypted password {password}'")
        os.system("sudo -u postgres psql -c 'grant all privileges on " +
                  f"database {dbname} to {uname}'")

        conn = psycopg2.connect(database=dbname, user=uname, password=password)
        cur = conn.cursor()
        cur.execute("create table urlshortner(time timestamp not null, path " +
                    "varchar(6) primary key, link text);")
        conn.commit()
        cur.close()
        conn.close()
        print("[+]Writing to config file....")
        config_write(common, db_details)
        print("[+]Done writing to config file")
    elif (choice == 2):
        host = str(input("Should the 1)server be hosted public facing(0.0.0" +
                         ".0) or 2)server should be hosted locally" +
                         "(localhost): "))
        if (host == '1'):
            host = '0.0.0.0'
        elif (host == '2'):
            host = 'localhost'
        dbname = str(input("Enter the name of the database you want to give." +
                           "Press ENTER for default(Default is database): "))
        if not dbname:
            dbname = "database.db"
        else:
            dbname = dbname+'.db'

        if (getpass.getuser() == 'root'):
            db_location = "/root/.config/urlshortner/" + dbname
        else:
            username = getpass.getuser()
            db_location = "/home/"+username+"/.config/"+dbname

        common = {'host': host}
        db_details = {
            'dbType': 'sqlite',
            'dbLoc': db_location,
        }

        conn = sqlite3.connect(db_location)
        cur = conn.cursor()
        cur.execute("create table urlshorter(time TEXT, path varchar(6)" +
                    "primary key, link TEXT);")
        conn.commit()
        cur.close()
        conn.close()
        print("[+]Writing configuration to config file...")
        config_write(common, db_details)
        print("[+]Done...!!")


if __name__ == "__main__":
    main()
