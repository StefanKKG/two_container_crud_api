**Welcome to this dockerized Flask locally hosted API application. The purpose of this application is to give us Solitans a CRUD APIenvironment that we can play with and that is easy to set up.**

The longer term intention for this project is to create a Docker container 
ecosystem that adds value to our internal testing needs as well as our client 
demos by connecting Docker containers that host relevant programs.

__Developer for this app: Stefan Günther__
-----------------------------------------------------------------
**1) HOW TO ACCESS AND RUN THE APPPLICATION**
a) Run the shell script with the "sh create_container.sh" to build the Docker container.
If you are a windows user, you may need to enable your computer to run shell scripts. Find more information here: https://linuxhint.com/run-sh-file-windows/.

**2) HOW TO ACCESS THE API'S DOCUMENTATION**
a) Once the Docker container is up and running, to "http://127.0.0.1:5001/openapidocs".
You can test the API endpoints straight from the OpenAPI documentation page.

**3) HOW TO CALL THE CRUD API**
You can call the API from the OpenAPI documentation by pressing the "Try out" and"execute" buttons. The OpenAPI
documentation also shows you what the various API responses are that you can get.

Alternatively, you can calso run one of the four "ex_" scripts which are accessible in app/tests.

**4) HOW TO QUERY THE SQLITE3 Database**
While you are testing / using the API, you may find it useful to query the data from the underlying SQLITE3 database directly. SQLITE3 supports the general SQL query syntaX as well as other SQL kywords. 
You can find the fulll list of supported SQLITE3 SQL keywords here: https://www.sqlite.org/lang_keywords.html.

**Below are some SQLITE3 commands that you may also find useful:**
Navigate to the 'var' folder in this directory which contains the SQLite3 database file and run one of the following commands in your terminal:

sqlite3 Database ".tables" ".exit" -- list the tables that exist in the database

sqlite3 Database "SELECT * FROM Customers;" ".exit" - query all of the data in the database

sqlite3 Database "SELECT * FROM Customers where row_id = 3;" ".exit" - query all of the data from row 3 in the database. You can change the query's row number.


