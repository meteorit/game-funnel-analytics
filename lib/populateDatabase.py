#!/usr/bin/python
import os
import sqlite3
import csv
from sqlite3 import Error
from pathlib import Path


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, table):
    """
    Drop and recreate the specified table
    :param conn: the Connection object
    :param table: the name of table
    :return:
    """
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS {}".format(table))

    if table == 'question1':
        cur.execute("CREATE TABLE IF NOT EXISTS question1 (Time STR,Impressions INT,Clicks INT,CTR STR,'Cohort size' INT,'Click to Install' STR,fCVR STR,'D7 Payers' INT, 'D7 Payer Conversion' STR, PRIMARY KEY (Time))")
        print("Success - " + table + " table was created.")

    elif table == 'question2':
        cur.execute("CREATE TABLE IF NOT EXISTS question2 (country STR,hours_bucket INT,installs INT,country_total_installs INT,share_within_country STR)")
        print("Success - " + table + " table was created.")

    elif table == 'country_mapping':
        cur.execute("CREATE TABLE IF NOT EXISTS country_mapping (alpha_2 STR,Country STR,PRIMARY KEY (alpha_2))")
        print("Success - " + table + " table was created.")

    elif table == 'q2_clean':
        cur.execute("CREATE TABLE IF NOT EXISTS q2_clean (alpha_2 STR,hours_bucket INT,installs INT,country_total_installs INT,share_within_country FLOAT)")
        print("Success - " + table + " table was created.")

    else:
        print("Sorry, this is not possible in current implementation.")


def populate_table(conn, table, to_db):
    """
    Populate the specified table with payload
    :param conn: the Connection object
    :param table: the name of table
    :param to_db: payload to be inserted
    :return:
    """
    cur = conn.cursor()

    if table == 'question1':
        cur.executemany("INSERT INTO question1 VALUES (?,?,?,?,?,?,?,?,?);", to_db)
        print("Success - question1 table was populated from raw CSV dataset question1_dataset.csv.")

    elif table == 'question2':
        cur.executemany("INSERT INTO question2 VALUES (?,?,?,?,?);", to_db)
        print("Success - question2 table was populated from raw CSV dataset question2_dataset.csv.")

    elif table == 'country_mapping':
        cur.executemany("INSERT INTO country_mapping VALUES (?,?);", to_db)
        print("Success - country_mapping table was populated from raw CSV dataset CountryMapping.csv.")

    elif table == 'q2_clean':
        cur.executemany("INSERT INTO q2_clean VALUES(?,?,?,?,?);", to_db)
        print("Success - q2_clean table was populated from question2 table  (with basic data cleaning operations).")

    else:
        print("Sorry, this is not possible in current implementation.")


def clean_table_query(conn, table):
    """
    Query the specified table with SQL to create clean dataset.
    :param conn: the Connection object
    :param table: the name of table
    :return: cleaned rows dataset
    """
    cur = conn.cursor()
    if table == 'question2':
        cur.execute('''SELECT upper(country) as alpha_2, hours_bucket, installs, country_total_installs,
        replace(share_within_country,"%","")  as share_within_country
        FROM question2
        WHERE length(country) = 2''')
        print("Success - table question2 was queried to produce a clean dataset.")
        rows = cur.fetchall()
        return rows
    else:
        print("Sorry, this is not possible in current implementation.")


def main():
    database = os.path.realpath('../db/rannala_project.db')

    # create a database connection
    conn = create_connection(database)

    # create Path mappings to source files (OS-agnostic)
    raw_data_folder = Path(os.path.realpath('../raw data sources/'))

    question1_file = raw_data_folder / "question1_dataset.csv"
    question2_file = raw_data_folder / "question2_dataset.csv"
    countrymapping = raw_data_folder / "CountryMapping.csv"

    # create payloads
    with open(question1_file,'r',encoding="utf-8-sig") as question1_table:
        dr = csv.DictReader(question1_table) # comma is default delimiter
        to_question1 = [(i['Time'], i['Impressions'], i['Clicks'], i['CTR'], i['Cohort size'], i['Click to Install'], i['fCVR'], i['D7 Payers'], i['D7 Payer Conversion']) for i in dr]

    with open(question2_file,'r',encoding="utf-8-sig") as question2_table:
        dr = csv.DictReader(question2_table) # comma is default delimiter
        to_question2 = [(i['country'], i['hours_bucket'], i['installs'], i['country_total_installs'], i['share_within_country']) for i in dr]

    with open(countrymapping,'r') as countrymapping_table:
        dr = csv.DictReader(countrymapping_table) # comma is default delimiter
        to_country_mapping = [(i['alpha_2'], i['Country']) for i in dr]

    # Deploy database with source tables
    with conn:
        print("\n1. Create question1 table:")
        create_table(conn,'question1')

        print("\n2. Populate question1 table:")
        populate_table(conn,'question1',to_question1)

        print("\n3. Create question2 table:")
        create_table(conn,'question2')

        print("\n4. Populate question2 table:")
        populate_table(conn,'question2',to_question2)

        print("\n5. Create country_mapping table:")
        create_table(conn,'country_mapping')

        print("\n6. Populate country_mapping table:")
        populate_table(conn,'country_mapping',to_country_mapping)

        print("\n7. Create q2_clean table:")
        create_table(conn,'q2_clean')

        print("\n8. Clean the question2 dataset with SQL query:")
        to_q2_clean = clean_table_query(conn,'question2')

        print("\n9. Populate q2_clean table:")
        populate_table(conn,'q2_clean',to_q2_clean)

        conn.commit()
        print("\nFINISH: Script successful, enjoy the Notebooks! :)")


if __name__ == '__main__':
    main()
