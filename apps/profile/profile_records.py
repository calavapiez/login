import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from apps import dbconnect as db


layout=html.Div(
    [
        html.H3("Personal Race Records"),
        html.Hr(),
        html.Div(
            "This will contain the table for the user's race records",
            id='profilerecords_racelist'
        )
    ]
)


@app.callback(
    [
        Output('profilerecords_racelist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        # Input('moviehome_titlefilter', 'value'),
    ]
)
def updatemovielist(pathname):
    if pathname == '/profile/profile_records':
        # 1. query the relevant records
        sql = """SELECT race_name, race_date, cmplt, rnkg, run_tm
                FROM race r
                    INNER JOIN individual_race_record irr ON r.race_id = irr.race_id
                WHERE NOT irr_delete_ind AND ptcpt_id = 1"""
        val = []
        colnames = ['Event Name', 'Date', 'Completed?', 'Ranking', 'Run Time']

        # if searchterm:
        #     sql += """ AND movie_name ILIKE %s"""
        #     val += [f"%{searchterm}%"]


        races = db.querydatafromdatabase(sql, val, colnames)
        
        # # 2. create the table and add it to the db
        # if movies.shape[0]:
        #     # add the buttons with the respective href
        #     buttons = []
        #     for movie_id in movies['ID']:
        #         buttons += [
        #             html.Div(
        #             dbc.Button('Edit', href=f"/movies/movies_profile?mode=edit&id={movie_id}",
        #                         size='sm', color='primary'),
        #             style={'text-align': 'center'}
        #             )
        #         ]
            
        #     # add the buttons to the movies table
        #     movies['Action'] = buttons

        #     #remove the ID column
        #     movies.drop('ID', axis=1, inplace=True),
            
        table = dbc.Table.from_dataframe(races, striped=True, bordered=True, hover=True, size='sm')
        return [table]
        # else:
        #     return ["No records to display."]
    else:
        raise PreventUpdate