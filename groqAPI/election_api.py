import sqlite3
import json

raw_election_data_db = "election_data.db"
constituency_data_db = "constituency_data.db"
conn = sqlite3.connect(raw_election_data_db)

def query_election_data(year):
    # Connect to the SQLite3 database
    cursor = conn.cursor()
    
    # Define the query with the placeholder for the year
    query = """
select 
*
FROM all_election_data
where Year = ?
    """
    
    # Execute the query with the provided year parameter
    cursor.execute(query, (year,))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Optionally, get the column names
    column_names = [description[0] for description in cursor.description]
    
    # Convert the results to a list of dictionaries
    data = []
    for row in results:
        row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        data.append(row_dict)

    return data

def determine_winners(election_data):
    # Create a dictionary to hold the winners
    winners = {}

    # Iterate through the election data
    for row in election_data:
        constituency = row['Constituency_Name']
        votes = row['Votes']
        
        # Check if the constituency is already in the winners dictionary
        if constituency not in winners:
            winners[constituency] = row
        else:
            # If current row has more votes, update the winner
            if votes > winners[constituency]['Votes']:
                winners[constituency] = row
    
    # Extract the winner information
    winner_list = []
    for constituency, winner_info in winners.items():
        winner_list.append(winner_info.copy())
    
    return winner_list

def get_parties_in_year(year):
    cursor = conn.cursor()
    
    query = """
    select distinct Party from all_election_data where Year = ?
    """
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    parties = [row[0] for row in results]
    return parties

def get_parties_in_year_and_state(year, state):
    cursor = conn.cursor()
    
    query = """
    select distinct Party from all_election_data where Year = ? and State_Name = ?
    """
    cursor.execute(query, (year, state))
    results = cursor.fetchall()
    parties = [row[0] for row in results]
    return parties

def get_constituencies_in_state(state):
    conn = sqlite3.connect(constituency_data_db)
    cursor = conn.cursor()
    
    query = """
    select distinct Constituency_Name from all_constituencies where State_Name = ?
    """
    cursor.execute(query, (state,))
    results = cursor.fetchall()
    constituencies = [row[0] for row in results]
    return constituencies

def get_constituencies_in_state_and_year(state, year):
    cursor = conn.cursor()
    
    query = """
    select distinct Constituency_Name from all_election_data where Year = ? and State_Name = ?
    """
    cursor.execute(query, (year, state))
    results = cursor.fetchall()
    constituencies = [row[0] for row in results]
    return constituencies

def get_states_in_year(year):
    cursor = conn.cursor()
    
    query = """
    select distinct State_Name from all_election_data where Year = ?
    """
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    states = [row[0] for row in results]
    return states

def get_constituencies_in_year(year):
    cursor = conn.cursor()
    
    query = """
    select distinct Constituency_Name from all_election_data where Year = ?
    """
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    constituencies = [row[0] for row in results]
    return constituencies

def execute_query(query):
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = []
    for row in results:
        row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        data.append(row_dict)
    return data


# print(get_states_in_year(2019))
# print(get_constituencies_in_state_and_year("Uttar_Pradesh", 2019))
