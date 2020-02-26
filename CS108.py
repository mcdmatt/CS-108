#!/usr/bin/python3
# Filename: project.py
# Author: Matt McDonnell (mcdmatt@bu.edu)
# Description: This program uses a database containing records from 3 tables. The
#               purpose of this program is to use this data to create a website
#               for the National Premier Soccer League. It will give tables of the
#               players, games, and teams along with ways to add to or update certain
#               aspects as the season goes on.

import MySQLdb as db    # the mysql database API 
import time
import cgi  
import cgitb; cgitb.enable()# web debugging package; always import it into your web apps

################################################################################
def connect_to_database():
    # connection to database
    '''Create a connection object to connect to MySQL database.
    Return the connection and cursor objects.
    '''
    
    ## NOTE: You will need to specify your connection to the database
    # Your username is your BU username and your password is the
    # first four numbers of your BUID.
    # For example, if your BUID is 'U123-45-6789',
    # your password is set to be '1234' (no quotes). 
    # change the db name to use your username, e.g. cs108_azs_mini_fb
    conn = db.connect(host="localhost",
                  user="mcdmatt", 
                  passwd="5106",
                  db="cs108_mcdmatt_project")
   
    cursor = conn.cursor()
    return conn, cursor


#####################################################################################
def print_form_data(form):
    '''Display the form data for debugging purposes.'''
    # print out the form data (for debugging purposes)
    print('Form data:<br>')

    print('<table>')
    keys = list(form.keys())
    keys.sort()
    # go through all keys:
    for k in keys:

        print('''<tr>
                    <td>%s</td>
                    <td>%s</td>
                </tr>''' % (k, form[k]))
        
    
    print('</table><hr>')
    
    
#####################################################################################
def print_headers():
    '''Print the HTTP headers.'''
    
    # print the content-type header
    print("Content-Type: text/html")
    print() # blank line to indicate end of headers
#####################################################################################
def intro():
    # this function shows an intro page as a home screen when nothing else is called
    """
    Function to display the introduction page where the NPSL logo and conference
    title is presented.
    """
    print("""
    <center>
    <title>NPSL Northeast Conference</title>
    <p><head>
    <p><br>
    <h2 align='center'<b><font size="+5" face="verdana" color="#191970">Northeast Conference</font></b></h2></head>
    <body align='center'><img src=http://www.npsl.com/wp-content/uploads/2017/11/NPSL_rev2018_4C-1.png width=250 height=300>
    <p>
    <i><font size="+1" face="verdana" color="#191970"><h3>We all work together to grow the game, build the NPSL, and develop our respective clubs.</h3><i></font>
    </body>
    """)
#####################################################################################
def print_HTML_page():
    # prints the style of the buttons at the top of each page using HTML

    '''Print the top of the HTML page to start the html code and set the coloring in
    the background for this website.'''
    
    print("""
    <html>
    <link rel="stylesheet" type="text/css" href="style.css">
    <form>
    <head>
    <style>
    body {
      background-color: #AED7E1;
    }

    h1 {
      color: black;
      margin-left: 20px;
    }
    </style>
    </head>
    <head>
    <style>
    .button {
        background-color:
    #DB3232;
        border: none;
        color: #FFFFFF;
        padding: 10px 40px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 3px 3px;
        cursor: pointer;
    }
    </style>
    </head>
    <body>
        
    <center>
    <img src=http://www.npsl.com/wp-content/uploads/2017/11/NPSL_rev2018_4C-1.png width=40 height=55>
    <input class="button" type="submit" name="homepage" value="Home">
    <input class="button" type="submit" name="teamlistpage" value="Teams">
    <input class="button" type="submit" name="standingspage" value="Standings">
    <input class="button" type="submit" name="playerlistpage" value="Players">
    <input class="button" type="submit" name="resultspage" value="Results">
    <img src=http://www.npsl.com/wp-content/uploads/2017/11/NPSL_rev2018_4C-1.png width=40 height=55>
    </center>
    </form>
    """
    # above are all the submit bottons you see at all times
    )
#####################################################################################
def print_bottom_of_page():
    '''Print the bottom of the HTML page with the time you entered a page and a return to main page button.'''

    print('''
<hr>
<center>
<u>This page was generated at %s.</u><br>
Return to the <a href="./project.py">main page</a>.
</body>
</html>
''' % time.ctime())
################################################################################
def get_all_teams():
    """Middleware function to get all teams from the Teams table.
    Returns a list containing one tuples from all fields in the Teams table"""

    # connect to database
    conn, cursor = connect_to_database()

    # build SQL
    sql = """
    SELECT * 
    FROM Teams
    ORDER BY team_id
    """

    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return data
################################################################################
def get_one_team(team_id):
    """Middleware function to retrieve one team's info from the database.
    Returns a list containing one tuple (team_id)."""
    
    # connect to database
    conn, cursor = connect_to_database()

    # build SQL
    sql = """
    SELECT *
    FROM Teams
    WHERE team_id=%s
    """

    # execute the query
    parameters = (team_id, )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data
#################################################################################
def show_all_teams(data):
    """
    Presentation layer function to display a table containing all teams' id and name.
    """
    ## create an HTML table for output:
    print("""
    <table align='center' border=10>
    <h2 align='center'><font size="+2" face="verdana" color="#191970">Teams</font></h2>
      <tr>
        <td align='center'><b><font face="verdana" color="#191970">Team ID</b></font></td>
        <td align='center'><b><font face="verdana" color="#191970">Name</b></font></td>
      </tr>
    """)
    
    for record in data:

        # each iteration of this loop creates one record of output:
        (team_name, city, state, national_championships, image, team_id, wins, losses) = record

        print("""
        <tr>
            <td align='center'><font face="verdana" color="#191970"><a href="?team_id=%s">%s</a></td>
            <td align='center'><font face="verdana" color="#191970"><a href="?team_id=%s">%s</a></td>
        </tr>
        """ % (team_id, team_id, team_id, team_name))
        

    print("""
    </table>
    """)

    print("""
    <body align='center'><i><font face="verdana" color="#191970">There are currently %d
    teams in the NPSL Northeast Conference.</font><br></i></body>""" % len(data))
###############################################################################################
def show_team_page(data):
    """Presentation layer function to display the profile page for one team.
    It combines sql select query and python lists. This loop give the city, state,
    and championships along with the logo. Additionally wins/losses are displayed."""

    ## show profile information
    record = data[0] # we expect only one record in this data set
    (team_name, city, state, national_championships, image, team_id, wins, losses) = record

    print("""
    <br><body align='center'><img align='center' src=%s width=133 height=133></body><br>
    <table align='center' border=10><br>
        <tr>
            <td><font face="verdana" color="#191970">City</font></td>
            <td align='center'><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">State</font></td>
            <td align='center'><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">National Championships</font></td>
            <td align='center'><font face="verdana" color="#191970">%s</font></td>
    </table>
    
    <h2><font face="verdana" size="+2" color="#191970">2018 Record</font></h2>
    <table align='center' border=10>
        <tr>
            <th><font face="verdana" color="#191970">Wins</font></th>
            <th><font face="verdana" color="#191970">Losses</font></th>
        </tr>
        <tr>
            <td align='center'><font face="verdana" color="#191970">%s</font></td>
            <td align='center'><font face="verdana" color="#191970">%s</font></td>
        </tr>
    </table>
    <i><font size="+1" face="verdana"><font face="verdana" color="#191970">As of %s</font></i><p>
    """ % (image, city, state, national_championships, wins, losses, time.ctime()))
#####################################################################################################
def show_update_team_results_form(data):
    """Display an HTML form to update the a team's wins/losses using a tuple."""
    
    record = data[0] # we expect only one record in this data set
    (team_name, city, state, national_championships, image, team_id, wins, losses) = record

    print('''
    <br>
    <b><font size="+2" face="verdana" color="#191970">Fill out and submit this record form after each
    game is played to update results.</font></b>

    <form>
    <input type='hidden' name='team_id' value='%s'>
    <table align='center'>
         <tr>
            <th><font face="verdana" color="#191970">Wins:</font></th>
            <td><input type='text' name='wins' value='%s'></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">Losses:</font></th>
            <td><input type='text' name='losses' value='%s'></td>
        </tr>

    <head>
    <style>
    .button {
        background-color:
    #DB3232;
        border: none;
        color: #FFFFFF;
        padding: 10px 40px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 3px 3px;
        cursor: pointer;
    }
    </style>
    </head>
    </table>

        <center><input class="button" type='submit' name='update_team_results' value='Update Record!'>

        </form>
        ''' % (team_id, wins, losses) )
#################################################################################################
def update_team_results(team_id, wins, losses):
    '''Update the record for one team. team_id acts as an identifier and the wins/
        losses are able to be updated to the Teams table according to the team_id'''

    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()

    # 2. Write SQL query as a Python string
    sql = '''
    UPDATE Teams
    SET wins=%s, losses=%s
    WHERE team_id = %s
    '''
    parameters = (wins, losses, team_id)

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql, parameters)

    # 4. Fetch/process the result set
    # cannot fetch results from INSERT query
    rowcount = cursor.rowcount # this is not a method -- no ()

    # 5. Clean up the database connection/cursor.
    cursor.close()
    conn.commit()
    conn.close()

    return rowcount
########################################################################################
def show_add_team_form():
    """Presentation layer function to display a table containing input boxes to add
    a team to the league by entering their info into the boxes.
    """

    print("""
    <p>
    <form>
    <h2><font size="+2" face="verdana" color="#191970">Add New Expansion Team</font></h2>
    <table align='center' border=10>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Team Name</font></font></b></label></td>
            <td align='center'><input type='text' name='team_name'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">City</font></b></label></td>
            <td align='center'><input type='text' name='city'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">State</font></b></label></td>
            <td><select name="state">
            <option value="AL">AL</option>
            <option value="AK">AK</option>
            <option value="AZ">AZ</option>
            <option value="AR">AR</option>
            <option value="CA">CA</option>
            <option value="CO">CO</option>
            <option value="CT">CT</option>
            <option value="DE">DE</option>
            <option value="DC">DC</option>
            <option value="FL">FL</option>
            <option value="GA">GA</option>
            <option value="HI">HI</option>
            <option value="ID">ID</option>
            <option value="IL">IL</option>
            <option value="IN">IN</option>
            <option value="IA">IA</option>
            <option value="KS">KS</option>
            <option value="KY">KY</option>
            <option value="LA">LA</option>
            <option value="ME">ME</option>
            <option value="MD">MD</option>
            <option value="MA">MA</option>
            <option value="MI">MI</option>
            <option value="MN">MN</option>
            <option value="MS">MS</option>
            <option value="MO">MO</option>
            <option value="MT">MT</option>
            <option value="NE">NE</option>
            <option value="NV">NV</option>
            <option value="NH">NH</option>
            <option value="NJ">NJ</option>
            <option value="NM">NM</option>
            <option value="NY">NY</option>
            <option value="NC">NC</option>
            <option value="ND">ND</option>
            <option value="OH">OH</option>
            <option value="OK">OK</option>
            <option value="OR">OR</option>
            <option value="PA">PA</option>
            <option value="RI">RI</option>	
            <option value="SC">SC</option>
            <option value="SD">SD</option>
            <option value="TN">TN</option>
            <option value="TX">TX</option>
            <option value="UT">UT</option>
            <option value="VT">VT</option>
            <option value="VA">VA</option>
            <option value="WA">WA</option>
            <option value="WV">WV</option>
            <option value="WI">WI</option>
            <option value="WY">WY</option>
	</select>	
    </td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">National Championships</font></b></label></td>
            <td align='center'><input type='text' name='national_championships'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Team ID</font></b></label></td>
            <td align='center'><input type='text' name='team_id'><br></td>
        </tr>
    </table>
    <table>
    <head>
    <style>
    .button {
        background-color:
    #DB3232;
        border: none;
        color: #FFFFFF;
        padding: 10px 40px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 3px 3px;
        cursor: pointer;
    }
    </style>
    </head>
    <tr><input class="button" type='submit' name='add_team' value='Add Team'></tr>
    </table>
    </form>
    <p>
    """ )
################################################################################
def add_team(team_id, team_name, city, state, national_championships):
    '''Inserts a new team into the database.'''

    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()
    sql = '''
    INSERT INTO Teams (team_id, team_name, city, state, national_championships)
    VALUES (%s, %s, %s, %s, %s)
    '''

    #2 For MySQL, use %s for substitutions into sql query (str, int, float, date)
    parameters = (team_id, team_name, city, state, national_championships) # make a tuple with one value

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql, parameters)

    # 4. Fetch/process the result set
    rowcount = cursor.rowcount

    # 5. Clean up the database connection/cursor.
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount   
################################################################################
def get_all_players():
    """Middleware function to get all rostered players from the players table.
    Returns a list of tuples of (player_ID, name, number, position)."""

    # connect to database
    conn, cursor = connect_to_database()

    # build SQL
    sql = """
    SELECT player_id, name, number, position
    FROM Players
    """

    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return data
################################################################################
def get_one_player(player_id):
    """Middleware function to retrieve one player's records from the database.
    Returns a list containing of tuples."""
    
    # connect to database
    conn, cursor = connect_to_database()

    # build SQL
    sql = """
    SELECT *
    FROM Players
    WHERE player_id=%s
    """

    # execute the query
    parameters = (player_id, )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data
####################################################################################
def show_all_players(data):
    """
    Presentation layer function to display a table containing all players' player_id,
    name, number, and position."""

    ## create an HTML table for output:

    print("""
    <h2 align='center'><font size="+2" face="verdana" color="#191970">Rostered Players</h2>

    <table align='center' border=10>
      <tr>
        <td align='center'><font size="+1" face="verdana" color="#191970"><b>Player ID</b></font></td>
        <td align='center'><font size="+1" face="verdana" color="#191970"><b>Name</b></font></td>
        <td align='center'><font size="+1" face="verdana" color="#191970"><b>Number</b></font></td>
        <td align='center'><font size="+1" face="verdana" color="#191970"><b>Position</b></font></td>
      </tr>
    """)
    
    for record in data:

        # each iteration of this loop creates on record of output:
        (player_id, name, number, position) = record

        print("""
      <tr>
        <td align='center'><font face="verdana" color="#191970"><a href="?player_id=%s">%s</a></td>
        <td align='center'><font face="verdana" color="#191970"><a href="?player_id=%s">%s</a></td>
        <td align='center'><font face="verdana" color="#191970"><a href="?player_id=%s">%s</a></td>
        <td align='center'><font face="verdana" color="#191970"><a href="?player_id=%s">%s</a></td>
      </tr>
        """ % (player_id, player_id, player_id, name, player_id, number, player_id, position))
        

    print("""
    </table>
    """)
    print("""</font><body align='center'><i><font face="verdana" color="#191970">Found %d players
    rostered in the Northeast Conference.</font></i><p></body>""" % len(data))
#################################################################################
def show_profile_page(data):
    """Presentation layer function to display the profile page for one player."""

    ## show profile information
    record = data[0] # we expect only one record in this data set
    (player_id, name, number, position, birth_year, college, goals, assists, saves, minutes_played, team_id) = record

    print("""
    <h2 align='center'><font face="verdana" color="#191970">%s</font></h2>
    <p>
    <table align='center' border=10>
        <tr>
            <td><font face="verdana" color="#191970">Number</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Position</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Birth Year</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">College</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Goals</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Assists</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Saves</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Minutes Played</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
        <tr>
            <td><font face="verdana" color="#191970">Current Team ID</font></td>
            <td><font face="verdana" color="#191970">%s</font></td>
        </tr>
    </table>
    """ % (name, number, position, birth_year, college, goals, assists, saves, minutes_played, team_id))

    # used to submit for a specific player_id and format the submit button
    print('''
    <p>
    <form>
    <head>
    <style>
    .button {
        background-color:
    #DB3232;
        border: none;
        color: #FFFFFF;
        padding: 10px 40px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 3px 3px;
        cursor: pointer;
    }
    </style>
    </head>
    <table align='center'>
        <tr>
            <td><input type='hidden' name='player_id' value='%s'></td></td>
            <td><input class="button" type='submit' name='show_update_player_form' value='Update Statistics Here'>
        </tr>
    </table>
    </form>
    ''' % (player_id)) 
#########################################################################################
def show_update_player_form(data):
    """Display an HTML form to update the profile for a user using a tuple."""

    record = data[0] # we expect only one record in this data set
    (player_id, name, number, position, birth_year, college, goals, assists, saves, minutes_played, team_id) = record

    print('''
    <p>
    <h3 align='center'><font face="verdana" color="#191970">Fill out and submit this form to update a player's stats to the database.</font></h3>
    <p>
    <form>
    <input type='hidden' name='player_id' value='%s'>
    <table border=10 align='center'>
         <tr>
            <th><font face="verdana" color="#191970">Position:</font></th>
            <td><select name="position">
                <option value="%s" selected>%s</option>
                <option value='F'>F</option>
                <option value='M'>M</option>
                <option value='D'>D</option>
                <option value='GK'>GK</option>
                </select></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">College:</font></th>
            <td><input type='text' name='college' value='%s'></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">Goals:</font></th>
            <td><input type='text' name='goals' value='%s'></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">Assist:</font></th>
            <td><input type='text' name='assists' value='%s'></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">Saves:</font></th>
            <td><input type='text' name='saves' value='%s'></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">Minutes Played:</font></th>
            <td><input type='text' name='minutes_played' value='%s'></td>
        </tr>
        <tr>
            <th><font face="verdana" color="#191970">Team ID:</font></th>
            <td><input type='text' name='team_id' value='%s'></td>
        </tr>
        </table>
        
        <center><input class="button" type='submit' name='update_stats' value='Update!'></td>
        
        </form>
        ''' % (player_id, position, position, college, goals, assists, saves, minutes_played, team_id) )
##############################################################################################
def update_stats(player_id, position, college, goals, assists, saves, minutes_played, team_id):
    '''Update the statistics for one player through an SQL query of the database.'''

    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()

    # 2. Write SQL query as a Python string
    sql = '''
    UPDATE Players
    SET position=%s, college=%s, goals=%s, assists=%s, saves=%s, minutes_played=%s, team_id=%s
    WHERE player_id = %s
    '''
    parameters = (position, college, goals, assists, saves, minutes_played, team_id, player_id)

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql, parameters)

    # 4. Fetch/process the result set
    # cannot fetch results from INSERT query
    rowcount = cursor.rowcount # this is not a method -- no ()

    # 5. Clean up the database connection/cursor.
    cursor.close()
    conn.commit()
    conn.close()

    return rowcount
##############################################################################################
def show_all_games(data):
    """
    Presentation layer function to display a table containing all games' ID, location,
    scores, and home/away team IDs.
    """
    
    print("""
    <h2 align='center'><font face="verdana" color="#191970">Results</font></h2>
    <p>
    <table align='center' border=10>
      <tr>
        <td align='center'><font face="verdana" color="#191970"><b>Game ID</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Location</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Home Score</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Away Score</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Home Team ID</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Away Team ID</b></font></td>
      </tr>
    """)
    
    for record in data:
        # each iteration of this loop creates on record of output:
        (game_id, home_team_id, away_team_id, location, home_score, away_score) = record

        print("""
        <tr>
            <td align='center'><font face="verdana" color="#191970">%s</td>
            <td><font face="verdana" color="#191970">%s</td>
            <td align='center'><font face="verdana" color="#191970">%s</td>
            <td align='center'><font face="verdana" color="#191970">%s</td>
            <td align='center'><font face="verdana" color="#191970">%s</td>
            <td align='center'><font face="verdana" color="#191970">%s</font></td>
        </tr>
        """ % (game_id, location, home_score, away_score, home_team_id, away_team_id))
        

    print("""
    </table>
    """)
    
    print("""<body align='center'><i><font face="verdana" color="#191970">There have
    been %d games played in the NPSL Northeast Conference so far this season.</font><br></i></body>""" % len(data))
################################################################################
def get_all_games():
    """Middleware function to get all games from the Games table.
    Returns a list of tuples."""

    # connect to database
    conn, cursor = connect_to_database()

    # build SQL
    sql = """
    SELECT * 
    FROM Games
    """

    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.commit()
    conn.close()
    cursor.close()
    
    return data
################################################################################
def insert_game(game_id, home_score, away_score, home_team_id, away_team_id):
    '''Insert a new game into the database using an SQL query of the database.'''

    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()
    sql = '''
    INSERT INTO Games (game_id, location, home_score, away_score, home_team_id, away_team_id)
    VALUES (NULL, %s, %s, %s, %s, %s)
    '''
    
    # For MySQL, use %s for substitutions into sql query (str, int, float, date)
    parameters = (location, home_score, away_score, home_team_id, away_team_id) # make a tuple with one value

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql, parameters)

    # 4. Fetch/process the result set
    rowcount = cursor.rowcount

    # 5. Clean up the database connection/cursor.
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
########################################################################################
def show_add_game_form():
    """Presentation layer function to display a form to add a new game to the league results."""

    print("""
    <p>
    <form>
    <h3><font face="verdana" color="#191970">Use this form to insert a new result.</font></h3>
    <table align='center' border=10>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Game ID</b></label></td>
            <td align='center'><input type='text' name='game_id'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Location</b></label></td>
            <td align='center'><input type='text' name='location'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Home Score</b></label></td>
            <td align='center'><input type='text' name='home_score'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Away Score</b></label></td>
            <td align='center'><input type='text' name='away_score'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Home ID</b></label></td>
            <td align='center'><input type='text' name='home_team_id'><br></td>
        </tr>
        <tr>
            <td align='center'><label><b><font face="verdana" color="#191970">Away ID</font></b></label></td>
            <td align='center'><input type='text' name='away_team_id'><br></td>
        </tr>
    </table>
    <table>
    <head>
    <style>
    .button {
        background-color:
    #DB3232;
        border: none;
        color: #FFFFFF;
        padding: 10px 40px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 3px 3px;
        cursor: pointer;
    }
    </style>
    </head>
    <tr><input class='button' type='submit' name='insert_game' value='Insert New Result'></tr>
    </table>
    </form>
    <p>
    """ )
##############################################################################################
def get_wins_at_home():
    '''Execute a query to the database to get the wins at home.'''
    
    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()

    sql = '''
    SELECT Teams.team_name, count(Games.home_team_id) as "home_wins"
    FROM `Games`
    INNER JOIN `Teams`
    ON Games.home_team_id = Teams.team_id
    WHERE Games.home_score > Games.away_score
    GROUP by Games.home_team_id
    ORDER by home_wins DESC
    '''
    # For MySQL, use %s for substitutions into sql query (str, int, float, date)
    # parameters = (team_id, ) # make a tuple with one value

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql)

    # 4. Fetch/process the result set
    data = cursor.fetchall()

    # 5. Clean up the database connection/cursor.
    cursor.close()
    conn.close()

    return data
##############################################################################################
def show_home_wins(data):
    """
    Presentation layer function to display a table containing the current home wins standing.
    """

    ## create an HTML table for output:
    print("""
    <h2 align='center'><font face="verdana" color="#191970">Home Wins</h2>
    
    <table align='center' border=10>
      <tr>
        <td align='center'><font face="verdana" color="#191970"><b>Team Name</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Wins</b></font></td>
      </tr>
    """)
    
    for record in data:

        # each iteration of this loop creates on record of output:
        (team_name, wins) = record

        print("""
      <tr>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
      </tr>
        """ % (team_name, wins))
    print("""
    </table>
    """)
##############################################################################################
def get_losses_at_home():
    '''Execute a query to the database to get the losses at home standing.'''
    
    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()

    sql = '''
    SELECT Teams.team_name, count(Games.home_team_id) as "home_losses"
    FROM `Games`
    INNER JOIN `Teams`
    ON Games.home_team_id = Teams.team_id
    WHERE Games.home_score < Games.away_score
    GROUP by Games.home_team_id
    ORDER by home_losses DESC
    '''
    
    # For MySQL, use %s for substitutions into sql query (str, int, float, date)
    # parameters = (team_id, ) # make a tuple with one value

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql)

    # 4. Fetch/process the result set
    data = cursor.fetchall()

    # 5. Clean up the database connection/cursor.
    cursor.close()
    conn.close()

    return data
##############################################################################################
def show_home_losses(data):
    """
    Presentation layer function to display a table containing home losses standing.
    """

    ## create an HTML table for output:
    print("""
    <h2 align='center'>Home Losses</h2>
    <p>
    
    <table align='center' border=10>
      <tr>
        <td align='center'><font face="verdana" color="#191970"><b>Team Name</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Losses</b></font></td>
      </tr>
    """)
    
    for record in data:

        # each iteration of this loop creates on record of output:
        (team_name, losses) = record

        print("""
      <tr>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
      </tr>
        """ % (team_name, losses))
    print("""
    </table>
    """)
###################################################################################
def get_wins_away():
    '''Execute a query to the database to get the conference standing for away wins.'''
    
    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()

    sql = '''
    SELECT Teams.team_name, count(Games.away_team_id) as "away_wins"
    FROM `Games`
    INNER JOIN `Teams`
    ON Games.away_team_id = Teams.team_id
    WHERE Games.away_score > Games.home_score
    GROUP by Games.away_team_id
    ORDER by away_wins DESC
    '''
    
    # For MySQL, use %s for substitutions into sql query (str, int, float, date)
    # parameters = (team_id, ) # make a tuple with one value

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql)

    # 4. Fetch/process the result set
    data = cursor.fetchall()

    # 5. Clean up the database connection/cursor.
    cursor.close()
    conn.close()

    return data
##############################################################################################
def show_away_wins(data):
    """
    Presentation layer function to display a table containing the current away wins standing.
    """

    ## create an HTML table for output:
    print("""
    <h2 align='center'>Away Wins</h2>
    <p>
    
    <table align='center' border=10>
      <tr>
        <td align='center'><font face="verdana" color="#191970"><b>Team Name</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Wins</b></font></td>
      </tr>
    """)
    
    for record in data:

        # each iteration of this loop creates on record of output:
        (team_name, wins) = record

        print("""
      <tr>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
      </tr>
        """ % (team_name, wins))

    print("""
    </table>
    """)
##############################################################################################
def get_losses_away():
    '''Execute a query to the database to get the conference standing for away losses.'''
    
    # 1. Connect to database, obtain cursor object
    conn, cursor = connect_to_database()

    sql = '''
    SELECT Teams.team_name, count(Games.away_team_id) as "away_losses"
    FROM `Games`
    INNER JOIN `Teams`
    ON Games.away_team_id = Teams.team_id
    WHERE Games.away_score < Games.home_score
    GROUP by Games.away_team_id
    ORDER by away_losses DESC
    '''
    # For MySQL, use %s for substitutions into sql query (str, int, float, date)
    # parameters = (team_id, ) # make a tuple with one value

    # 3. Execute the SQL query against the database cursor
    cursor.execute(sql)

    # 4. Fetch/process the result set
    data = cursor.fetchall()

    # 5. Clean up the database connection/cursor.
    cursor.close()
    conn.close()

    return data
##############################################################################################
def show_away_losses(data):
    """
    Presentation layer function to display a table containing the current away losses standing.
    """

    ## create an HTML table for output:
    print("""
    <h2 align='center'>Away Losses</h2>
    <p>
    
    <table align='center' border=10>
      <tr>
        <td align='center'><font face="verdana" color="#191970"><b>Team Name</b></font></td>
        <td align='center'><font face="verdana" color="#191970"><b>Losses</b></font></td>
      </tr>
    """)
    
    for record in data:

        # each iteration of this loop creates on record of output:
        (team_name, losses) = record

        print("""
      <tr>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
        <td align='center'><font face="verdana" color="#191970">%s</font></a></td>
      </tr>
        """ % (team_name, losses))

    print("""
    </table>
    """)
##############################################################################################
if __name__ == "__main__":
    # gets form field data
    print_headers()

    form = cgi.FieldStorage() # obtain the HTTP form data into a python variable

    # shows any errors in the form data for coder reference
    ##print_form_data(form)

    # this provides the buttons at the top of each page to enter an isolated view of the different fields displayed  
    print_HTML_page()

    # this scans for player id in the form to lead up to the update 
    if 'player_id' in form:
        player_id = form['player_id'].value

        # this starts the player statistics update 
        if 'show_update_player_form' in form:

            # calls the show update form for one player
            data = get_one_player(player_id)
            show_update_player_form(data)

        # this is the needed code for starting the second step in the update
        if 'update_stats' in form:

            # this is the second half (response) of the second step to the update
            if ('position' in form and 'college' in form
                and 'goals' in form and 'assists' in form
                and 'saves' in form and 'minutes_played'
                in form and 'team_id' in form):

                # calls the update function when user updates player stats
                position = form['position'].value
                college = form['college'].value
                goals = form['goals'].value
                assists = form['assists'].value
                saves = form['saves'].value
                minutes_played = form['minutes_played'].value
                team_id = form['team_id'].value

                # calls for the stats to be updated to the database
                rc = update_stats(player_id, position, college, goals, assists, saves, minutes_played, team_id)
                print('Player profile has been updated!')

            # Ensures that all stats have some valid value inputted or it won't update the stats
            else:
                print("<b>Cannot update stats, missing some required form data.<b>")

        # this allows the user to click on a rostered player and view their profile page
        data = get_one_player(player_id)
        show_profile_page(data)
        
        
    elif 'team_id' in form:
        team_id = form['team_id'].value

        if 'show_update_team_results_form' in form:
            data = get_one_team(team_id)
            show_update_team_results_form(data)
            
        # this calls the show the update form
        elif 'update_team_results' in form:

            if ('wins' in form and 'losses' in form):

                # calls the update function when user updates teams' results
                wins = form['wins'].value
                losses = form['losses'].value
                rc = update_team_results(team_id, wins, losses)

        # this will start the add
        if 'add_team' in form:

            if ('team_id' in form and 'team_name' in form and 'city' in form and
                'state' in form and 'national_championships' in form): 

                # calls the add function when user adds teams
                team_id = form['team_id'].value
                team_name = form['team_name'].value
                city = form['city'].value
                state = form['state'].value
                national_championships = form['national_championships'].value

                rc = add_team(team_id, team_name, city, state, national_championships)
                print('%d team was added to the conference.' % rc)

        # this fetches one team based on their id and then shows the corresponding
        # team profile page with an ability to update their win/loss record.
        data = get_one_team(team_id)
        show_team_page(data)
        show_update_team_results_form(data)
        
    # calls forms that include the game id to be able to insert a new game/result
    elif 'game_id' in form:

        game_id = form['game_id'].value

        #calls the form to insert a new game in after results are final
        if 'insert_game' in form:

            if ('location' in form and 'home_score' in form and 'away_score' in form
                and 'home_team_id' in form and 'away_team_id' in form):

                # calls the insert function when user adds a result
                
                location = form['location'].value
                home_score = form['home_score'].value
                away_score = form['away_score'].value
                home_team_id = form['home_team_id'].value
                away_team_id = form['away_team_id'].value

                rc = insert_game(game_id, home_score, away_score, home_team_id, away_team_id)
                # counts the rows inserted
                print('%d games were inserted.' % rc)
          
    elif 'teamlistpage' in form:
        # calls the function which shows a table of all the teams in the database

        data = get_all_teams()
        show_all_teams(data)
        show_add_team_form()

    elif 'playerlistpage' in form:
        # calls the function which shows a table of all the players in the database

        data = get_all_players()
        show_all_players(data)


    # calls the function which shows the standings tables
    elif 'standingspage' in form:

        # shows the home wins table
        data = get_wins_at_home()
        show_home_wins(data)

        # shows the away wins table
        data = get_wins_away()
        show_away_wins(data)

        # shows the home losses table
        data = get_losses_at_home()
        show_home_losses(data)

        # shows the away losses table
        data = get_losses_away()
        show_away_losses(data)
        
    elif 'resultspage' in form:
        # calls the function which shows the home/away game results
        data = get_all_games()
        show_all_games(data)
        show_add_game_form()

    # this else sends it to the introduction page with the logo and league name
    else:
        
        #homepage displaying the title, logo, and league moto each time no other functions are called
        intro()
    # prints out the bottom of the page set for all pages
    print_bottom_of_page() 
