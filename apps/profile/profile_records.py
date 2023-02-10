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
        # html.Div(
        #     [
        #     dcc.Store(id='profilerecords_toload', storage_type='memory', data=0),
        #     ]
        # ),
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
    ],
    [
        State('currentptcptid', 'data'),
    ]
)
def addracelist(pathname, currentptcptid):
    if pathname == '/profile/profile_records':

        sql = """
            SELECT race_name, date, cmplt, rnkg, run_tm
            FROM(
                SELECT 
                    ptcpt_id,
                    race_name, 
                    TO_CHAR(race_date, 'Mon dd, yyyy') AS date, 
                    UPPER(cmplt::text) AS cmplt, 
                    DENSE_RANK () OVER(
                            PARTITION BY r.race_id
                            ORDER BY irr.run_tm
                        ) AS rnkg, 
                    run_tm
                FROM race r
                    INNER JOIN individual_race_record irr 
                        ON r.race_id = irr.race_id
                WHERE NOT irr_delete_ind 
            ) add_rank
            WHERE ptcpt_id = %s;
        """
        val = [currentptcptid]
        colnames = ['Event Name', 'Date', 'Completed?', 'Ranking', 'Run Time']

        races = db.querydatafromdatabase(sql, val, colnames)
        print(races)

        if races.shape[0]:            
            table = dbc.Table.from_dataframe(races, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No records to display."]
    else:
        raise PreventUpdate