# coding: utf-8

"""
    Example of using dash_record_navigator with a database.
    Example data come from https://www.ssa.gov/oact/babynames/limits.html
"""

import os
import sqlite3
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL

from dash_record_navigator import RecordNavigator

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

# make database
if not os.path.exists('yob2018.db'):
    df = pd.read_csv('yob2018.txt', names=['name', 'gender', 'births'])
    df = df.sort_values(['births', 'name'], ascending=[False, True])
    db = sqlite3.connect('yob2018.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE names (name TEXT, gender TEXT, births INTEGER);''')
    for row in df.itertuples(index=False):
        sql = '''INSERT INTO names VALUES ('{}','{}','{}');'''.format(*row)
        cursor.execute(sql)
    db.commit()
    db.close()
    
# load data
db = sqlite3.connect('file:yob2018.db?mode=ro', uri=True, check_same_thread=False)
cursor = db.cursor()

def execute(sql):
    cursor.execute(sql)
    rows = []
    row = cursor.fetchone()
    while row:
        rows.append(row)
        row = cursor.fetchone()
        
    return rows

record_nav = RecordNavigator('names')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
            [
                dcc.Input(id='search-name',
                          placeholder='Enter a string',
                          value='',
                          type='search',
                          autoFocus=True,
                          autoComplete='off',
                          size='40',
                          style={'margin-top': '20px'}),
                dcc.Checklist(options=[
                                       {'label': 'Female', 'value': 'F'},
                                       {'label': 'Male', 'value': 'M'},
                                      ],
                              value=['F', 'M'],
                              labelStyle={'display': 'inline-block'},
                              id='check-gender',
                              style={'margin-top': '20px'}
                        ),
                html.Div(id='table-names'),
                record_nav.html(),
            ],
            style={'margin-left': '10px'})

@app.callback(
    Output('table-names', 'children'),
    [Input('search-name', 'value'),
     Input('check-gender', 'value'),
     Input({'index': ALL, 'role': ALL, 'name': 'names'}, 'n_clicks_timestamp')])
def display_records_from_df(search_name, check_gender, all_ts):
    btn = record_nav.which_button(*all_ts)
    rows = select_in_db(search_name, check_gender, btn)

    trs = [
        html.Tr(
            [
                html.Td(row[0]),
                html.Td(row[1]),
                html.Td(row[2])
            ]) for row in rows]

    if len(trs) == 0:
        result = html.P('No name available.')
    else:
        result = html.Table([
                            html.Th('name'),
                            html.Th('gender'),
                            html.Th('births'),
                            *trs
                            ],
                            style={'font-size': 'small'})
    return result

def select_in_db(search_name, check_gender, btn):
    sql = '''SELECT name, gender, births FROM names WHERE (name like '%{}%') AND (gender IN ('{}'))'''.format(search_name, "','".join(check_gender))
    sql_count = '''SELECT COUNT(*) FROM ({});'''.format(sql)
    

    limit, offset = record_nav.get_bounds(btn,
                                          (search_name, check_gender),
                                          lambda: execute(sql_count)[0][0])

    sql = '{} LIMIT {} OFFSET {};'.format(sql, limit, offset)
    rows = execute(sql)
    
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)
