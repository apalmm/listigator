import sys
from flask_sqlalchemy import SQLAlchemy
from contextlib import closing
from sqlite3 import Row, connect, DatabaseError

# create the extension
db = SQLAlchemy()

# DB_URL = "file:WAlawyers.sqlite?mode=ro"

def query_database(query, DB_URL, mapping=None, many=True, ):
    """Query the database with the given query and mapping
    Args:
        query (str): query string with named placeholders
        mapping (dict): dictionary holding placeholder values
    """
    try:
        with connect(DB_URL, uri=True) as conn:
            conn.row_factory = Row
            with closing(conn.cursor()) as cursor:
                cursor.execute(query, mapping)
                results = cursor.fetchall() if many else cursor.fetchone()
    except DatabaseError as err:
        print(err)
        sys.exit(1)

    return results

# PUBLIC INTERFACE

def get_lawyers(name, city, phone, field, state, probono=False):
    query = "SELECT * FROM Lawyer INNER JOIN Field ON Field.LicenseNumber = Lawyer.LicenseNumber"
    
    if(state == "Washington"):
        DB_URL = "file:WAlawyers.sqlite?mode=ro"
    if(state == "FL"):
        DB_URL = "file:FLlawyers.sqlite?mode=ro"

    parameters = {}
    conditions = []

    if field:
        conditions.append("Field LIKE :field")
        parameters['field'] = f'%{field}%'
    if name:
        conditions.append("Name LIKE :name")
        parameters['name'] = f'%{name}%'
    if city:
        conditions.append("City LIKE :city")
        parameters['city'] = f'%{city}%'
    if probono:
        conditions.append("Status = 'Pro Bono'")
        parameters['probono'] = probono
    if phone:
        conditions.append("Phone LIKE :phone")
        parameters['phone'] = f'%{phone}%'
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " LIMIT 250 "
        
    print(query, parameters, state)
        
    lawyers = query_database(query, DB_URL, parameters )
    
    return lawyers
