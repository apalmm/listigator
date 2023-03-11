from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def results():
    field = request.form['field']
    name = request.form['name']
    city = request.form['city']
    probono = request.form.get('probono')
    phone = request.form['phone']

    query = "SELECT * FROM Lawyer INNER JOIN Field ON Field.LicenseNumber=Lawyer.LicenseNumber"
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
    if probono is not None:
        conditions.append("Status = 'Pro Bono'")
        parameters['probono'] = probono
    if phone:
        conditions.append("Phone LIKE :phone")
        parameters['phone'] = f'%{phone}%'
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with sqlite3.connect('WALawyers.sqlite') as conn:
        cursor = conn.cursor()
        results = cursor.execute(query, parameters).fetchall()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
