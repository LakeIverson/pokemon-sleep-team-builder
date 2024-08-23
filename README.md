### Pokemon Sleep Team Builder
The goal of this app was to aid in the creation of teams for the mobile game *Pokemon Sleep*. The app in it's current state would store Pokemon you discover in game and their stats, and will find the best team for each given week given the random conditions.

This is a sqlite3 based database project built in python3 using the click library for command handling.

Below are each of the files and what they are for.
#### add-data.py
This file will update `data.txt`which is just a hardcoded txt file with all the data needed for the team builder. Whenever the game updates the player will need to use this python script to add in the files in the proper format to allow the database to accept the new data.

#### create-database.py
This deletes the current database and recreates it according to `database.schema`.

#### helper.py
Adds user pokemon to the database as "helpers". These helpers are what the database uses to construct a team.

#### populate-database.py
Used in conjunction with `create-database.py`. When the user creates the database, this will read `data.txt`and feed the information into the database.

#### team-builder.py
This will ask the user for information regarding the current area they are in the for the week and will find the best 5 pokemon from the user's helper list to create an optimal team for the week.
