from operator import truediv
import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table 
import dash 
from dash.exceptions import PreventUpdate 
import pandas as pd
from dash.dependencies import Input, Output, State

from app import app
from apps import dbconnect as db




layout = html.Div(
    [
        html.H2('Events'),  
        html.Hr(), 
        dbc.Card(
            [
                dbc.CardHeader(
                    [ 
                        html.H3('Manage Events')
                    ]
                ),
                dbc.CardBody(
                    [ 
                        html.Div(
                            [ 
                                dbc.Button(
                                    "Add Event",
                                    href='/events/events_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [ 
                                html.H4('Find Events'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [ 
                                                dbc.Label("Search Event Name", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='eventshome_namefilter',
                                                        placeholder='Event Name'
                                                    ),
                                                    width=5
                                                )
                                            ], 
                                        ),
                                        className="mb-3",
                                    )
                                ),
                                html.Div(
                                    "Table with movies will go here.",
                                    id='eventshome_eventslist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(     
    [         
        Output('eventshome_eventslist', 'children')     
    ],     
    [         
        Input('url', 'pathname'),
        Input('eventshome_namefilter', 'value')     
    ] 
) 
def eventhome_loadeventlist(pathname, searchterm):     
    if pathname == '/events/events_home':         
        # 1. Obtain records from the DB via SQL
        sql = """select race_name, race_date, race_course, race_id from race
            where not race_delete_ind
            """    
        values = []

        cols = ['Event Name', 'Date', 'Race Course', "ID"]


        if searchterm:
            sql += """ and race_name ILIKE %s"""

            values += [f"%{searchterm}%"]

        events = db.querydatafromdatabase(sql, values, cols)
        
        if events.shape[0]:   
        # 2. Create the html element to return to the Div 
            edit = []
            for race_id in events['ID']:
                edit += [
                    html.Div(
                        dbc.Button("Edit", href=f'events_profile?mode=edit&id={race_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ] 

            events['Action'] = edit

            results = []
            for race_id in events['ID']:
                results += [
                    html.Div(
                        dbc.Button("View", href=f'events_results?id={race_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ] 

            events['Race Results'] = results

            events.drop('ID', axis=1, inplace=True)

            table = dbc.Table.from_dataframe(events, striped=True, bordered=True, hover=True, size='sm')
            
            return [table]
        else:
            return ["No records to display"]
    else:         
        raise PreventUpdate 