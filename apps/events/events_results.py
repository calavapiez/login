from operator import truediv
import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table 
import dash 
from dash.exceptions import PreventUpdate 
import pandas as pd
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs

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
                        html.H3(
                            'Event Name',
                            id='eventsresults_eventname'
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div(
                            [ 
                                dbc.Button(
                                    "Add Participant Record",
                                    href='/events/events_results_profile?mode=add'
                                )
                            ]
                        ),
                        html.Hr(), 
                        html.Div(
                            [ 
                                html.H4('Find Participant'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [ 
                                                dbc.Label("Search Participant Name", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='eventsresults_namefilter',
                                                        placeholder='Event Participant Name'
                                                    ),
                                                    width=5
                                                )
                                            ], 
                                        ),
                                        className="mb-3",
                                    )
                                ),
                                html.Div(
                                    "Table with results will go here.",
                                    id='eventsresults_participantlist'
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
        Output('eventsresults_eventname', 'children'),     
    ],     
    [         
        Input('url', 'pathname'),  
    ],
    [
        State('url', 'search')
    ]
)

def eventsresults_loadeventname(pathname, search):
    if pathname == '/events/events_results':

        parsed = urlparse(search)             
        raceid = parse_qs(parsed.query)['id'][0]         
        # 1. Obtain records from the DB via SQL
        sql = """select race_name from race where race_id = %s
            """    
        values = [raceid]

        cols = ['eventname']

        df = db.querydatafromdatabase(sql, values, cols)

        eventname = df['eventname'][0]

        return [eventname]

    else:
        raise PreventUpdate

@app.callback(     
    [         
        Output('eventsresults_participantlist', 'children'),     
    ],     
    [         
        Input('url', 'pathname'),
        Input('eventsresults_namefilter', 'value')     
    ],
    [
        State('url', 'search')
    ]
) 
def eventsresults_loadeventresults(pathname, searchterm, search):     
    if pathname == '/events/events_results':

        parsed = urlparse(search)             
        raceid = parse_qs(parsed.query)['id'][0]         
        # 1. Obtain records from the DB via SQL
        sql = """select ptcpt_name, case 
                when cmplt = '0' then 'No' else 'Yes'  
            end completed, rnkg, run_tm, irr_id
            from individual_race_record i
            inner join participant p on i.ptcpt_id = p.ptcpt_id
            where not irr_delete_ind and race_id = %s
            """    
        values = [raceid]

        cols = ['Participant Name', 'Completed', 'Ranking', 'Race Time', 'ID']


        if searchterm:
            sql += """ and ptcpt_name ILIKE %s"""

            values += [f"%{searchterm}%"]

        results = db.querydatafromdatabase(sql, values, cols)
        
        if results.shape[0]:   
            edit = []
            for irr_id in results['ID']:
                edit += [
                    html.Div(
                        dbc.Button("Edit", href=f'events_results_profile?mode=edit&id={irr_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ] 

            results['Action'] = edit

            results.drop('ID', axis=1, inplace=True)

            table = dbc.Table.from_dataframe(results, striped=True, bordered=True, hover=True, size='sm')
            
            return [table]
        else:
            return ["No records to display"]
    else:         
        raise PreventUpdate 