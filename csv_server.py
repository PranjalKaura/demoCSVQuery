
from argparse import ArgumentParser

from flask import Flask, request, render_template, redirect, url_for

import pandas as pd

app = Flask(__name__)

#redirect for query
@app.route("/query/<query>")
def queryFunc(query):
    result = DATA.query(query) #run query on dataframe
    return render_template('query.html',  tables=[result.to_html()], titles=[result.columns.values])

@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if request.method == 'POST': 
        query = "" #initialize query string

        #drop down selector queries
        weather = request.form.get('weather')
        query += 'WEATHER == "' + weather + '"'
        stn = request.form.get('stn')
        query += ' and ' + 'STN_NAME == "' + stn + '"'

        #comparator query
        query = parseQuery(query, request.form, 'DD')
        query = parseQuery(query, request.form, 'MONTH')
        query = parseQuery(query, request.form, 'GGGG')
        query = parseQuery(query, request.form, 'FF')
        query = parseQuery(query, request.form, 'VIS')
        query = parseQuery(query, request.form, 'DB')

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
    # parsedOutput.monthUnique = DATA.MONTH.unique()
    # parsedOutput.ddUnique = DATA.DD.unique()
    # parsedOutput.ggggUnique = DATA.GGGG.unique()
    # parsedOutput.dddUnique = DATA.DDD.unique()
    # parsedOutput.ffUnique = DATA.FF.unique()
    # parsedOutput.visUnique = DATA.VIS.unique()
    # parsedOutput.dbUnique = DATA.DB.unique()

    return parsedOutput

if __name__ == '__main__':

    parser = ArgumentParser(prog='csvParser',
                    description='Web based querying of csv file')
    parser.add_argument('csv_file', nargs='*', help='The csv file that the app will query', 
                        default=['ADM.csv', 'AFA.csv', 'GWL.csv'])
    args = parser.parse_args()
    DATA = pd.concat((pd.read_csv(f) for f in args.csv_file), ignore_index=True) #concatenate all csv dataframes into one
    app.run()

