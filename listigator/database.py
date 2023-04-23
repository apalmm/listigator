from flask_sqlalchemy import SQLAlchemy
import sys
from contextlib import closing
from sqlite3 import Row, connect, DatabaseError

# create the extension
db = SQLAlchemy()

DB_URL = "file:WALawyers.sqlite?mode=ro"

def query_database(query, mapping=None, many=True):
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

def get_lawyers(name, city, phone, field, probono):
    query = "SELECT * FROM Lawyer INNER JOIN Field ON Field.LicenseNumber = Lawyer.LicenseNumber"
    
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
        
    print(query, parameters)
        
    lawyers = query_database(query, parameters)
    
    return lawyers
