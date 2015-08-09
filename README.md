# sql-connections
Functions to handle MySQL database connections and queries

----
## dbConnect()

#### INPUT

username, password, host IP, database schema

#### OUTPUT

database connection object


Opens a connection to the given database


----
## dbQuery()

#### INPUT

connection object, query statement


#### OUTPUT

`result`            = dictionary containing column names and results

`result['columns']` = array of result column names

`result['data']`    = array of tuples of results

`result['data'][0]` = first result from query as a tuple


Pass in a connection and an arbitrary SQL query, receive the results of that query for parsing

----
## dbUpdate()

#### INPUT

connection object, SQL update/insert statement, data to be inserted/updated as a list of lists

#### OUTPUT

none


Executes the update/insert statement with the provided data on the database associated with the given connection object


----
## dbClose()

#### INPUT

database connection object

#### OUTPUT

none


Closes a given database connection
