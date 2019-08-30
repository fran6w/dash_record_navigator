# coding: utf-8

"""
    Example of using dash_record_navigator with a dataframe.
    Example data come from https://www.ssa.gov/oact/babynames/limits.html
"""

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_record_navigator import RecordNavigator

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

# load data
df = pd.read_csv('yob2018.txt', names=['name', 'gender', 'births'])
df = df.sort_values(['births', 'name'], ascending=[False, True])

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
                record_nav.html()
            ],
            style={'margin-left': '10px'})

@app.callback(
    Output('table-names', 'children'),
    [Input('search-name', 'value'),
     Input('check-gender', 'value'),
     *record_nav.inputs()])
def display_records_from_df(search_name, check_gender, fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts):
    btn = record_nav.which_button(fast_backward_ts, step_backward_ts, step_forward_ts, fast_forward_ts)
    rows = select_in_df(search_name, check_gender, btn)

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

def select_in_df(search_name, check_gender, btn):    
    df2 = df.loc[df['name'].str.contains(search_name, case=False) & df['gender'].isin(check_gender)]

    limit, offset = record_nav.get_bounds(btn,
                                          (search_name, check_gender),
                                          len(df2))

    df2 = df2.iloc[offset:offset+limit]
    
    return list(df2.itertuples(index=False))

if __name__ == '__main__':
    app.run_server(debug=True)
