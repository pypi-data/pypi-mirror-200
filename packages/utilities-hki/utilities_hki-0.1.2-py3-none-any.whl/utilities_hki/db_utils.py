"""
Database utility functions.
Copyright (C) 2022 Humankind Investments
"""

import boto3
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2 import sql


def database_connect(dbname, db_dict):
    """
    Connect to database with given name.

    Parameters
    ----------
    dbname : str
        Name of database to query.
    db_dict : dict
        Dictionary of credentials for all databases. For example:
        db_dict = {'hkisocial' : cred.hkisocial,
                    'hkiweb' : cred.hkiweb,
                    'hkimarket' : cred.hkimarket,
                    'hkiads' : cred.hkiads,
                    }

    Returns
    -------
    psycopg2.connection.cursor
        Database connection cursor object.
    psycopg2.connection
        Database connection object.
    """

    session = boto3.Session(profile_name = 'default')
    client = boto3.client('rds')

    conn = psycopg2.connect(host = db_dict[dbname]['endpoint'],
                            port = db_dict[dbname]['port'],
                            database = dbname,
                            user = db_dict[dbname]['username'],
                            password = db_dict[dbname]['pw'],
                            )

    return conn.cursor(), conn


def database_write(dbname, db_dict, table_query, df, table_name):
    """
    Write data to table in database.

    Parameters
    ----------
    dbname : str
        Name of database to which to write the data.
    db_dict : dict
        Dictionary of credentials for database(s).
    table_query : str
        Initial table creation query.
    df : pd.DataFrame
        Dataframe to insert into table in database.
    table_name : str
        Name of table in which to insert data.
    """

    # connect to database
    cursor, conn = database_connect(dbname, db_dict)

    # create initial table
    cursor.execute(table_query)
    conn.commit()

    # write data to table in DB
    tdict = df.to_dict(orient='records')
    tname = '%s' % table_name
    tcolumns = list(df)
    query = insert_data(tname, tcolumns)
    execute_batch(cursor, query, tdict)
    conn.commit()

    cursor.close()
    conn.close()

    
def insert_data(table, columns):
    """
    Create insert query.

    Parameters
    ----------
    table : str
        Name of table in which to insert data.
    columns : list of str
        List of column names in table.
    
    Returns
    -------
    insert : sql query
        SQL insert query.
    """

    insert = sql.SQL('INSERT INTO {} ({}) VALUES({});').format(
        sql.Identifier(table),
        sql.SQL(',').join(map(sql.Identifier, columns)),
        sql.SQL(',').join(map(sql.Placeholder, columns))
        )

    return insert

