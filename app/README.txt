Welcome to the 'app' folder that contains all of the files that this app requires to run.

DETAILS ABOUT THIS FOLDER'S CONTENTS:
1) Data folder - contains the 'data.csv' file which has the dummy data. 
These 500 rows of data are loaded into the database once by the application. 

2) models folder - contain all the classes which themselves contain functions 
that define the logic for the GET/PUT/PATCH/DELETE requests.

3) tests folder - contain sample .py test scripts for the GET/PUT/PATCH/DELETE methods.

4) requirements.txt file - list the libraries and their versions that are
required in order for this app to function. These libraries are 
automatically installed by Docker when you build your Docker container.