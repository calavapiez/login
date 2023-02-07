from logging.handlers import DatagramHandler
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
        html.Div(
            [
                dcc.Store(id='resultsprofile_toload', storage_type='memory', data=0),
            ]
        ), 
        html.H2('Participant Record Details'),
        html.Hr(),
        dbc.Alert(id='resultsprofile_alert', is_open=False),
        dbc.Form(
            [ 
                dbc.Row(
                    [ 
                        dbc.Label("Event Name", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='resultsprofile_eventname',
                                placeholder='Event Name',
                                searchable=True,
                                clearable=True
                            ),
                            width=5
                        )
                    ], 
                ),
                dbc.Row(
                    [ 
                        dbc.Label("Participant Name", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='resultsprofile_participantname',
                                placeholder='Participant Name',
                                searchable=True,
                                clearable=True
                            ),
                            width=5
                        )
                    ], 
                ),
                dbc.Row(
                    [ 
                        dbc.Label("Completed?", width=1),
                        dbc.Col(
                            dbc.Checklist(
                            id='resultsprofile_completed',
                            options=[
                                {
                                    'label': "Mark if completed",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'},
                            ),
                            width = 5
                        )
                    ], 
                ),
                dbc.Row(
                    [ 
                        dbc.Label("Ranking", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='number',
                                id='resultsprofile_ranking',
                                placeholder='Ranking'
                            ),
                            width=5
                        )
                    ], 
                ),
                dbc.Row(
                    [ 
                        dbc.Label("Run Time", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='resultsprofile_runtime',
                                placeholder='Input run time as HH:MM:SS'
                            ),
                            width=5
                        )
                    ], 
                ),
            ],
            className="mb-3",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='resultsprofile_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'},
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='resultsprofile_removerecord_div'
        ),
        dbc.Button(
            'Submit',
            id='resultsprofile_submit',
            n_clicks=0
        ),
        dbc.Modal(
            [ 
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    'Message here! Edit me please!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/events/events_home'
                    )
                )
            ],
            centered=True,
            id='resultsprofile_successmodal',
            backdrop='static'
        )
    ]
)


@app.callback(
    [ 
        Output('resultsprofile_eventname', 'options'),
        Output('resultsprofile_toload', 'data'),
        Output('resultsprofile_removerecord_div', 'style'),
    ],
    [ 
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def resultsprofile_populateeventnamefield(pathname, search):
    if pathname == '/events/events_results_profile':
        sql ="""
        SELECT race_name as label, race_id as value
        FROM race
        WHERE race_delete_ind = False
        """
        values = []
        cols = ['label','value']
        df = db.querydatafromdatabase(sql, values, cols)
        eventname_options = df.to_dict('records')

        parsed = urlparse(search)             
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0
        
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [eventname_options, to_load, removediv_style]


@app.callback(
    [ 
        Output('resultsprofile_participantname', 'options')
    ],
    [ 
        Input('url', 'pathname')
    ]
)

def resultsprofile_populateparticipantnamefield(pathname):
    if pathname == '/events/events_results_profile':
        sql ="""
        SELECT ptcpt_name as label, ptcpt_id as value
        FROM participant
        WHERE ptcpt_delete_ind = False
        """
        values = []
        cols = ['label','value']
        df = db.querydatafromdatabase(sql, values, cols)
        participantname_options = df.to_dict('records')
    else:
        raise PreventUpdate
    return [participantname_options]


@app.callback(
    [
        Output('resultsprofile_alert', 'color'),         
        Output('resultsprofile_alert', 'children'),         
        Output('resultsprofile_alert', 'is_open'),         
        Output('resultsprofile_successmodal', 'is_open')     
    ], 
    [
        Input('resultsprofile_submit', 'n_clicks')
    ],
    [ 
        State('resultsprofile_eventname', 'value'),                 
        State('resultsprofile_participantname', 'value'),
        State('resultsprofile_completed', 'value'), 
        State('resultsprofile_ranking', 'value'),
        State('resultsprofile_runtime', 'value'), 
        State('url', 'search'),
        State('resultsprofile_removerecord', 'value')
    ]
)
def resultsprofile_saveprofile(submitbtn, eventname, participantname, completed, ranking, runtime, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'resultsprofile_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            inputs = [eventname, participantname, ranking, runtime]

            if not all(inputs):
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply all inputs'
            elif not eventname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the event name'
            elif not participantname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the participant name'
            elif not ranking:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the ranking'
            elif not runtime:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the run time'
            else:
                parsed = urlparse(search)             
                mode = parse_qs(parsed.query)['mode'][0]
                if mode == 'add':
                    sql = """
                        INSERT INTO individual_race_record (race_id, ptcpt_id, cmplt, rnkg, run_tm, irr_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    is_completed = bool(completed)
                    values = [eventname, participantname, is_completed, ranking, runtime, False]

                    db.modifydatabase(sql, values)

                    modal_open = True

                elif mode == 'edit':
                    parsed = urlparse(search)             
                    irr_id = parse_qs(parsed.query)['id'][0]

                    sql = """
                        update individual_race_record
                        set
                            race_id = %s,
                            ptcpt_id = %s,
                            cmplt = %s,
                            rnkg = %s,
                            run_tm = %s,
                            irr_delete_ind = %s
                        where
                            irr_id = %s
                        """
                    to_delete = bool(removerecord)
                    is_completed = bool(completed)
                    values = [eventname, participantname, is_completed, ranking, runtime, to_delete, irr_id]

                    db.modifydatabase(sql, values)

                    modal_open = True

                else:
                    raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('resultsprofile_eventname', 'value'),                  
        Output('resultsprofile_participantname', 'value'), 
        Output('resultsprofile_completed', 'value'),
        Output('resultsprofile_ranking', 'value'),
        Output('resultsprofile_runtime', 'value')
    ],
    [
        Input('resultsprofile_toload', 'modified_timestamp')
    ],
    [
        State('resultsprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def eventsprofile_loadprofile(timestamp, to_load, search):
    if to_load == 1:

        parsed = urlparse(search)             
        irr_id = parse_qs(parsed.query)['id'][0]

        sql = """
            select race_id, ptcpt_id, cmplt, rnkg, run_tm
            from individual_race_record
            where irr_id = %s
        """
        values = [irr_id]
        col = ['raceid', 'ptcptid', 'completed', 'ranking', 'runtime']

        df = db.querydatafromdatabase(sql, values, col)

        eventname = int(df['raceid'][0])
        participantname = int(df['ptcptid'][0])
        completed = bool(df['completed'][0])
        ranking = df['ranking'][0]
        runtime = df['runtime'][0]

        return [eventname, participantname, completed, ranking, runtime]

    else:
        raise PreventUpdate