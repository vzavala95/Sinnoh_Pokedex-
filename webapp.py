from flask import Flask, render_template, request, redirect
import os
import MySQLdb as mariadb
from db_credentials import host, user, passwd, db



def connect_to_database(host = host, user = user, passwd = passwd, db = db):
    '''
    connects to a database and returns a database objects
    '''
    db_connection = mariadb.connect(host,user,passwd,db)
    return db_connection

def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object
    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query
    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.
    '''

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params))
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor()

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    #TODO: Sanitize the query before executing it!!!
    cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit()
    return cursor

#create the web application
webapp = Flask(__name__)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    webapp.run(port=port, debug=True)


# app routes for Landing page
	

@webapp.route('/main.html')
def home():
    return render_template('main.html')

# SEARCH FOR POKEMON -------------------------------------------------------------------

@webapp.route('/search.html', methods=['GET', 'POST'])
def search(): 
    return render_template('search.html')
    #     db_connection=connect_to_database()
    #     query = query = 'SELECT * FROM Pokemon WHERE Pokemon.pokeName = %s;'
    #     results = execute_query(db_connection, query).fetchall()
    #     print(results,)
    #     return render_template('search.html')
    
    # elif request.form == 'POST':
    #     db_connection = connect_to_database()
    #     search_term = request.form['search_term']
    #     query = 'SELECT * FROM Pokemon WHERE Pokemon.pokeName = %s;'
    #     data = (search_term,)
    #     search_results = execute_query(db_connection, query, data).fetchall()
    #     print(search_results)
    #     return redirect('search.html', search_results=search_results)


# app routes for POKEMON ---------------------------------------------------------------

# POKEMON READ ---------------------------------------------------------------------------------

@webapp.route('/view_pokemon.html', methods=['GET', 'POST'])
def view_pokemon():
    if request.method == 'GET':
        db_connection = connect_to_database()
        query = 'SELECT * FROM Pokemon; '
        results = execute_query(db_connection, query).fetchall()
        print(results)
        return render_template('view_pokemon.html', pokemon=results)


# POKEMON CREATE -------------------------------------------------------------------------------

@webapp.route('/add_pokemon.html', methods=['POST', 'GET'])
def add_pokemon():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_pokemon.html')

    elif request.method == 'POST':
        pokeName = request.form['pokeName']
        pokeBio = request.form['pokeBio']
        query = 'INSERT INTO Pokemon (pokeName, pokeBio) VALUES (%s, %s);'
        data = (pokeName, pokeBio)
        execute_query(db_connection, query, data)
        return redirect('/view_pokemon.html')

# POKEMON UPDATE --------------------------------------------------------------------------------

@webapp.route('/update_pokemon.html/<int:pokeID>', methods=['POST', 'GET'])
def update_pokemon(pokeID):
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Pokemon WHERE pokeID = %s;"
        data = (pokeID,)
        execute_query(db_connection, query, data).fetchall()
        return render_template('add_pokemon.html')

    elif request.method == 'POST':
        pokeName = request.form['pokeName']
        pokeBio = request.form['pokeBio']
        query = 'UPDATE Pokemon SET PokeName = %s, pokeBio = %s WHERE pokeID = %s;'
        data = (pokeName, pokeBio, pokeID)
        execute_query(db_connection, query, data)
        return redirect('/view_pokemon.html')

# POKEMON DELETE ------------------------------------------------------------------------------------

@webapp.route('/delete_pokemon.html/<int:pokeID>')
def delete_pokemon(pokeID):
    db_connection = connect_to_database()
    query = 'DELETE FROM Pokemon WHERE pokeID = %s;'
    data = (pokeID,)
    execute_query(db_connection, query, data)
    return redirect('/view_pokemon.html')

# app routes for TYPES ----------------------------------------------------------------------

# TYPES READ --------------------------------------------------------------------------------------

@webapp.route('/view_types.html')
def view_types():
    db_connection = connect_to_database()
    query = 'SELECT * FROM Types; '
    results = execute_query(db_connection, query).fetchall()
    print(results)
    return render_template('view_types.html', types=results)

# TYPES CREATE ------------------------------------------------------------------------------------

@webapp.route('/add_type.html', methods=['POST', 'GET'])
def add_type():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_type.html')

    elif request.method == 'POST':
        db_connection = connect_to_database()
        typeName = request.form['typeName']
        weakness = request.form['weakness']
        strength = request.form['strength']
        query = 'INSERT INTO Types (typeName, weakness, strength) VALUES (%s, %s, %s);'
        data = (typeName, weakness, strength)
        execute_query(db_connection, query, data)
        return redirect('/view_types.html')


# @webapp.route('/add_type.html', methods=['POST', 'GET'])
# def add_types():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         return render_template('add_type.html')

#     elif request.method == 'POST':
#         typeName = request.form['typeName']
#         weakness = request.form['weakness']
#         strength = request.form['strength']
#         query = 'INSERT INTO Types(typeName, weakness, strength) VALUES (%s, %s, %s);'
#         data = (typeName, weakness, strength)
#         execute_query(db_connection, query, data)
#         return redirect('/view_types.html')


# TYPES UPDATE -------------------------------------------------------------------------------------

@webapp.route('/update_type.html/<int:typeID>', methods=['POST', 'GET'])
def update_type(typeID):
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Types WHERE typeID = %s;"
        data = (typeID,)
        execute_query(db_connection, query, data).fetchall()
        return render_template('add_type.html')

    elif request.method == 'POST':
        typeName = request.form['typeName']
        weakness = request.form['weakness']
        strength = request.form['strength']
        query = 'UPDATE Types SET typeName = %s, weakness = %s, strength = %s WHERE typeID = %s;'
        data = (typeName, weakness, strength, typeID)
        execute_query(db_connection, query, data)
        return redirect('/view_types.html')

# TYPES DELETE ------------------------------------------------------------------------------------

@webapp.route('/delete_type.html/<int:typeID>')
def delete_types(typeID):
    db_connection = connect_to_database()
    query = 'DELETE FROM Types WHERE typeID = %s;'
    data = (typeID,)
    execute_query(db_connection, query, data)
    return redirect('/view_types.html')


# app routes for MOVES --------------------------------------------------------------------------

@webapp.route('/view_moves.html')
def view_moves():
    db_connection = connect_to_database()
    query = 'SELECT Moves.moveID, Moves.moveName, Moves.category, Types.typeName FROM Moves LEFT JOIN Types ON Moves.type = Types.typeID;'
    results = execute_query(db_connection, query).fetchall()
    print(results)
    return render_template('view_moves.html', moves=results)

# MOVES CREATE -----------------------------------------------------------------------------------------

@webapp.route('/add_move.html', methods=['POST', 'GET'])
def add_move():
    db_connection = connect_to_database()
    if request.method == 'GET':
        types_query = 'SELECT Types.typeName FROM Moves RIGHT JOIN Types ON Moves.type = Types.typeID;'
        types_dropdown = execute_query(db_connection, query=types_query).fetchall()
        print(types_dropdown,)
        return render_template('add_move.html', types=types_dropdown)

    if "addMove" in request.form:
        moveName = request.form['moveName']
        category = request.form['category']
        type = request.form['type']
        query = 'INSERT INTO Moves (moveName, category, type) VALUES (%s, %s, (SELECT typeID FROM Types WHERE typeName = %s));'
        data = (moveName, category, type,)
        execute_query(db_connection, query, data)
        return redirect('/view_moves.html')

# MOVES UPDATE -------------------------------------------------------------------------------------------


# MOVES DELETE -------------------------------------------------------------------------------------------

@webapp.route('/delete_move.html/<int:moveID>')
def delete_move(moveID):
    db_connection = connect_to_database()
    query = 'DELETE FROM Moves WHERE moveID = %s;'
    data = (moveID,)
    execute_query(db_connection, query, data)
    return redirect('/view_moves.html')

# app route for LOCATIONS ----------------------------------------------------------------------------

# LOCATIONS READ ------------------------------------------------------------------------------------------------

@webapp.route('/view_locations.html')
def view_locations():
    db_connection = connect_to_database()
    query = 'SELECT Locations.locationID, Locations.locationName, Locations.locationBio, Gym_Leaders.leadName FROM Locations LEFT JOIN Gym_Leaders ON Locations.leader = Gym_Leaders.leadID;'
    results = execute_query(db_connection, query).fetchall()
    print(results)
    return render_template('view_locations.html', locations=results)

# LOCATIONS CREATE -----------------------------------------------------------------------------------------------

# 'SELECT Locations.locationID, Locations.locationName, Locations.locationBio, Gym_Leaders.leadName FROM Locations LEFT JOIN Gym_Leaders ON Locations.Leader = Gym_Leaders.leadID;'

@webapp.route('/add_location.html', methods=['POST', 'GET'])
def add_location():
    db_connection = connect_to_database()
    if request.method == 'GET':
        gym_leaders_query = 'SELECT Gym_Leaders.leadName FROM Locations RIGHT JOIN Gym_Leaders ON Locations.leader = Gym_Leaders.leadID;'
        gym_leaders_dropdown = execute_query(db_connection, query=gym_leaders_query).fetchall()
        print(gym_leaders_dropdown,)
        return render_template('add_location.html', gym_leaders=gym_leaders_dropdown)
    
    if request.method == 'POST':
        locationName = request.form['locationName']
        locationBio = request.form['locationBio']
        leader = request.form['leader']
        query = 'INSERT INTO Locations (locationName, locationBio, leader) VALUES (%s, %s, (SELECT leadID FROM Gym_Leaders WHERE leadName = %s));'
        data = (locationName, locationBio, leader,)
        execute_query(db_connection, query, data)
        return redirect('/view_locations.html')


# LOCATIONS DELETE -----------------------------------------------------------------------------------------------

@webapp.route('/delete_location.html/<int:locationID>')
def delete_location(locationID):
    db_connection = connect_to_database()
    query = 'DELETE FROM Locations WHERE locationID = %s;'
    data = (locationID,)
    execute_query(db_connection, query, data)
    return redirect('/view_locations.html')

# app routes for GYM LEADERS -----------------------------------------------------------------------------

# GYM LEADERS READ ----------------------------------------------------------------------------------------------------

@webapp.route('/view_gym_leaders.html')
def view_gym_leaders():
    db_connection = connect_to_database()
    query = 'SELECT * FROM Gym_Leaders;'
    results = execute_query(db_connection, query).fetchall()
    print(results)
    return render_template('view_gym_leaders.html', gym_leaders=results)

# GYM LEADERS CREATE --------------------------------------------------------------------------------------------------

@webapp.route('/add_gym_leader.html', methods=['POST', 'GET'])
def add_gym_leader():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_gym_leader.html')

    elif request.method == 'POST':
        leadName = request.form['leadName']
        query = 'INSERT INTO Gym_Leaders (leadName) VALUES (%s);'
        data = (leadName,)
        execute_query(db_connection, query, data)
        return redirect('/view_gym_leaders.html')

# GYM LEADERS UPDATE -----------------------------------------------------------------------------------------------------

@webapp.route('/update_gym_leader.html/<int:leadID>', methods=['POST', 'GET'])
def update_gym_leader(leadID):
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT * FROM Gym_Leaders WHERE leadID = %s;"
        data = (leadID,)
        results = execute_query(db_connection, query, data).fetchall()
        return render_template('add_gym_leader.html', gym_leader_data=results, form_action='/update_gym_leader.html/' + str(leadID))

    elif request.method == 'POST':
        leadName = request.form['leadName']
        query = 'UPDATE Gym_Leaders SET leadName = %s WHERE leadID = %s;'
        data = (leadName, leadID)
        execute_query(db_connection, query, data)
        return redirect('/view_gym_leaders.html')

# GYM LEADERS DELETE ------------------------------------------------------------------------------------------------------

@webapp.route('/delete_gym_leader.html/<int:leadID>')
def delete_gym_leader(leadID):
    db_connection = connect_to_database()
    query = 'DELETE FROM Gym_Leaders WHERE leadID = %s;'
    data = (leadID,)
    execute_query(db_connection, query, data)
    return redirect('/view_gym_leaders.html')


# app routes for POKEMON_MOVES -----------------------------------------------------------------------------

# POKEMON_MOVES READ ----------------------------------------------------------------------------------------------------------

@webapp.route('/view_pokemon_moves.html', methods=['GET', 'POST'])
def view_pokemon_moves():
    if request.method == 'POST': 
        db_connection = connect_to_database()
        sinnoh_pokemon = request.form['sinnoh_pokemon']
        move = request.form['move']
        data = (sinnoh_pokemon, move)
        query = 'DELETE FROM Pokemon_Moves WHERE sinnoh_pokemon = %s AND move = %s;'
        results = execute_query(db_connection, query, data).fetchall()
        return redirect('view_pokemon_moves.html')
    else:
        query = 'SELECT Pokemon.pokeID, Pokemon.pokeName, Moves.moveID, Moves.moveName FROM Pokemon_Moves LEFT JOIN Pokemon ON Pokemon_Moves.sinnoh_pokemon = Pokemon.pokeID LEFT JOIN Moves ON Pokemon_Moves.move = Moves.moveID;'
        db_connection = connect_to_database()
        results = execute_query(db_connection, query).fetchall()
        print(results)
        return render_template('view_pokemon_moves.html', pokemon_moves=results)

# POKEMON_MOVES CREATE --------------------------------------------------------------------------------------------------------

@webapp.route('/add_pm.html', methods=['POST', 'GET'])
def add_pokemon_move():
    db_connection = connect_to_database()
    if request.method == 'GET':
        p_query = 'SELECT Pokemon.pokeID FROM Pokemon_Moves RIGHT JOIN Pokemon ON Pokemon_Moves.sinnoh_pokemon = Pokemon.pokeID;'
        m_query = 'SELECT Moves.moveID FROM Pokemon_Moves RIGHT JOIN Moves ON Pokemon_Moves.move = Moves.moveID;'
        p_dropdown = execute_query(db_connection, query=p_query).fetchall()
        m_dropdown = execute_query(db_connection, query=m_query).fetchall()
        print(p_dropdown, m_dropdown)
        return render_template('add_pm.html', pokemon=p_dropdown, moves=m_dropdown)

    elif request.method == 'POST':
        sinnoh_pokemon = request.form['sinnoh_pokemon']
        move = request.form['move']
        query = 'INSERT INTO Pokemon_Moves(sinnoh_pokemon, move) VALUES (%s, %s);'
        data = (sinnoh_pokemon, move,)
        execute_query(db_connection, query, data)
        return redirect('/view_pokemon_moves.html')

# POKEMON_MOVES DELETE ---------------------------------------------------------------------------------------------------------

# @webapp.route('/delete_pm.html/<int:sinnoh_pokemon><int:move>', methods=['GET', 'POST'])
# def delete_pm(pokeID, moveID):
#     db_connection = connect_to_database()
#     if request.method == 'POST':
#         pokeID = request.form['pokeID']
#         moveID = request.form['moveID']
#         query = 'DELETE FROM Pokemon_Moves WHERE Pokemon_Moves.sinnoh_pokemon = %{s} AND Pokemon_Moves.move = %{s};'
#         data = (pokeID, moveID,)
#         execute_query(db_connection, query, data)
#         return redirect('/view_pokemon_moves.html')

# app routes for POKEMON_LOCATIONS -----------------------------------------------------------------------------

# POKEMON_LOCATIONS READ ----------------------------------------------------------------------------------------------------------

@webapp.route('/view_pokemon_locations.html')
def view_pokemon_locations():
    db_connection = connect_to_database()
    query = 'SELECT Pokemon.pokeID, Pokemon.pokeName, Locations.locationID, Locations.locationName FROM Pokemon_Locations LEFT JOIN Pokemon ON Pokemon_Locations.sinnoh_pokemon = Pokemon.pokeID LEFT JOIN Locations ON Pokemon_Locations.location = Locations.locationID;'
    results = execute_query(db_connection, query).fetchall()
    print(results)
    return render_template('view_pokemon_locations.html', pokemon_locations=results)

# POKEMON_LOCATIONS CREATE --------------------------------------------------------------------------------------------------------

@webapp.route('/add_pokemon_location.html', methods=['POST', 'GET'])
def add_pokemon_location():
    db_connection = connect_to_database()
    if request.method == 'GET':
        po_query = 'SELECT Pokemon.pokeID FROM Pokemon_Locations RIGHT JOIN Pokemon ON Pokemon_Locations.sinnoh_pokemon=Pokemon.pokeID;'
        lo_query = 'SELECT Locations.locationID FROM Pokemon_Locations RIGHT JOIN Locations ON Pokemon_Locations.location = Locations.locationID;'
        po_dropdown = execute_query(db_connection, query=po_query).fetchall()
        lo_dropdown = execute_query(db_connection, query=lo_query).fetchall()
        print(po_dropdown, lo_dropdown)
        return render_template('add_pokemon_location.html', pokemon=po_dropdown, locations=lo_dropdown)

    elif request.method == 'POST':
        sinnoh_pokemon = request.form['sinnoh_pokemon']
        location = request.form['location']
        query = 'INSERT INTO Pokemon_Locations(sinnoh_pokemon, location) VALUES (%s, %s);'
        data = (sinnoh_pokemon, location,)
        execute_query(db_connection, query, data)
        return redirect('/view_pokemon_locations.html')

def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object
    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query
    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.
    '''

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params))
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor()

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    #TODO: Sanitize the query before executing it!!!
    cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit()
    return cursor
