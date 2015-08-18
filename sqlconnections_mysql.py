# The MIT License (MIT)
# 
# Copyright © 2015 Glenn Fitzpatrick
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import mysql.connector as mariadb
import logging

from tqdm import *


verbose = False


# dbConnect()
#
# INPUT
# username, password, host IP, database schema
#
# OUTPUT
# database connection object
#
# Opens a connection to the given database

def dbConnect(DB_USER, DB_HOST, DB_SCHEMA, DB_PASSWORD = None):

    if not DB_PASSWORD:

        DB_PASSWORD = input("Enter password: ")

    print("Opening connection to database...", end=" ")
    
    try:
        connection = mariadb.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_SCHEMA)
        print("connected!")
        print()
        
    except:
        print("Unable to connect!")
        
        return False
        
    else:
        return connection


# dbQuery()
#
# INPUT
# connection object, query statement
#
# OUTPUT
# result            = dictionary containing column names and results
# result['columns'] = array of result column names
# result['data']    = array of tuples of results
# result['data'][0] = first result from query as a tuple
#
# Pass in a connection and an arbitrary SQL query, receive the results of that query for parsing

def dbQuery(connection, query):

    result = {}

    if verbose:
        print()
        print("Opening cursor")
    logging.info("Opening cursor")
    cur = connection.cursor()

    if verbose:
        print("Running query...")
        print()
        print(query)

    logging.info("Running query...")
    logging.info(query)
    
    cur.execute(query)

    description = []

    for d in cur.description:
        description.append(d[0])

    result['columns'] = description
    
    reader = cur.fetchall()

    cur.close()

    data = []
    
    for row in reader:
        data.append(row)

    if verbose:
        print()
        print("Cursor closed. Retrieved", str(len(data)), "rows.")
        print()

    logging.info("Cursor closed. Retrieved {} rows.".format(str(len(data))))

    result['data'] = data

    return result


# dbUpdate()
#
# INPUT
# connection object, SQL update/insert statement, data to be inserted/updated as a list of lists
# 
# OUTPUT
# none
#
# Executes the update/insert statement with the provided data on the database associated with the given connection object

def dbUpdate(connection, query, data):

    cursor = connection.cursor()
    
    if verbose:
    
        if query.startswith("INSERT"):
            print("Inserting data...")
        
        elif query.startswith("UPDATE"):
            print("Updating data...")
    
        else:
            print("Changing data...")
    
    if verbose:
        for item in tqdm(data, leave=True):
            cursor.execute(query, item)
        print()
        
    else:
        for item in tqdm(data):
            cursor.execute(query, item)
            
    if verbose:

        if query.startswith("INSERT"):
    
            if len(data) == 1:
                print("1 row inserted")
            
            elif len(data) == None:
                print("0 rows inserted")
            
            else:
                print("{} rows inserted".format(str(len(data))))
            
        elif query.startswith("UPDATE"):
    
            if len(data) == 1:
                print("1 row updated")
            
            elif len(data) == None:
                print("0 rows updated")
            
            else:
                print("{} rows updated".format(str(len(data))))
            
        else:
            if len(data) == 1:
                print("1 row changed")
            
            elif len(data) == None:
                print("0 rows changed")
            
            else:
                print("{} rows changed".format(str(len(data))))
    
    try:
        connection.commit()
        
        if verbose:
            print("Database commit.")
            print()
        
    except:
        print("Unable to commit!")
        print()
        
        return False
    
    else:
        cursor.close()
        
        return


# dbClose()
#
# INPUT
# database connection object
#
# OUTPUT
# none
#
# Closes a given database connection

def dbClose(connection):

    connection.close()
    print("Database connection closed.")
    logging.info("Database connection closed.")
    print()
    
    return
