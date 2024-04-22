
from argparse import ArgumentParser

from flask import Flask, request, render_template, redirect, url_for

import pandas as pd
import json

app = Flask(__name__)
userAuthenticated = False

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    global userAuthenticated
    error = None
    if request.method == 'POST':
        usernames = [cred['username'] for cred in creds['creds']]
        passwords = [cred['password'] for cred in creds['creds']]
        if request.form['username'] not in usernames or request.form['password'] not in passwords:
            error = 'Invalid Credentials. Please try again.'
        elif usernames.index(request.form['username']) != passwords.index(request.form['password']):
            error = 'Invalid Credentials. Please try again.'
        else: #password match
            userAuthenticated = True
            return redirect(url_for('home'))
            
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global userAuthenticated
    userAuthenticated = False
    return redirect(url_for('login'))

# Route for handling the register page logic
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cred = {"username":username, "password":password}
        creds['creds'].append(cred) #add username to database
        with open("creds.json", "w") as file: #save added credentials to file
            json.dump(creds, file, indent=6)
        return redirect(url_for('login'))
    return render_template('register.html', msg = msg)


#redirect for query
@app.route("/query/<query>")
def queryFunc(query):
    if not userAuthenticated: #check for user authentication
        return redirect(url_for('logout'))
    result = DATA.query(query) #run query on dataframe
    return render_template('query.html',  tables=[result.to_html()], titles=[result.columns.values])

#redirect for query instantiation
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST']) 
def home():
    if not userAuthenticated:
        return redirect(url_for('logout'))
    if request.method == 'POST': 
        query = "" #initialize query string
        #drop down selector queries
        weather = request.form.get('weather')
        query += 'WEATHER == "' + weather + '"'
        stn = request.form.get('stn')
        query += ' and ' + 'STN_NAME == "' + stn + '"'

        #comparator query
        query = parseQuery(query, request.form, 'DATE')
        query = parseQuery(query, request.form, 'MONTH')
        query = parseQuery(query, request.form, 'TIME')
        query = parseQuery(query, request.form, 'WIND SPEED')
        query = parseQuery(query, request.form, 'VIS')
        query = parseQuery(query, request.form, 'DB')
        query = parseQuery(query, request.form, 'WIND DIR')

        # Print the query in terminal for verification 
        print(query) 

        #redirect to the url for resolution of query
        return redirect(url_for('queryFunc', query=query))
    
    parsedOutput = parseData()
    return render_template('home.html', weathers = parsedOutput['uniqueWeather'], stations = parsedOutput['stnUniqueName'], comparators = parsedOutput["comparators"]) 

def parseQuery(query, form, columnName):
    comparator = form.get('comparator' + columnName) #get the comparator sign
    val = form.get(columnName) #get the value for comparison
    if comparator != ' ': #if comparator is empty, ignore current column
        query += ' and ' + columnName + comparator + val
    return query

def parseData():
    parsedOutput = dict()
    parsedOutput['uniqueWeather'] = DATA.WEATHER.unique()
    parsedOutput['stnUniqueName'] = DATA.STN_NAME.unique()
    parsedOutput['comparators'] = ['>', '<', '==', ' ']

    return parsedOutput

if __name__ == '__main__':

    parser = ArgumentParser(prog='csvParser',
                    description='Web based querying of csv file')
    parser.add_argument('csv_file', nargs='*', help='The csv file that the app will query', 
                        default=['ADM.csv', 'AFA.csv', 'GWL.csv'])
    args = parser.parse_args()
    DATA = pd.concat((pd.read_csv(f) for f in args.csv_file), ignore_index=True) #concatenate all csv dataframes into one
    DATA = DATA.rename(columns={"DD": "DATE", "GGGG": "TIME", "FF":"WIND SPEED", "DDD":"WIND DIR"})#rename certain columns for web UI

    with open("creds.json", "r") as file:
        creds = json.load(file)
    app.run(debug = True)

