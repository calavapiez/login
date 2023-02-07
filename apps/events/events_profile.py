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
                dcc.Store(id='eventsprofile_toload', storage_type='memory', data=0),
            ]
        ), 
        html.H2('Event Details'),
        html.Hr(),
        dbc.Alert(id='eventsprofile_alert', is_open=False),
        dbc.Form(
            [ 
                dbc.Row(
                    [ 
                        dbc.Label("Event Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='eventsprofile_eventname',
                                placeholder='Event Name'
                            ),
                            width=5
                        )
                    ], 
                ),
                dbc.Row(
                    [ 
                        dbc.Label("Date", width=1),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='eventsprofile_date',
                                placeholder='Event Date',
                                month_format='MMM Do, YY'
                            ),
                            width=5
                        )
                    ], 
                ),
                dbc.Row(
                    [ 
                        dbc.Label("Race Course", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='eventsprofile_racecourse',
                                placeholder='Race Course'
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
                            id='eventsprofile_removerecord',
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
            id='eventsprofile_removerecord_div'
        ),
        dbc.Button(
            'Submit',
            id='eventsprofile_submit',
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
            id='eventsprofile_successmodal',
            backdrop='static'
        )
    ]
)


@app.callback(
    [ 
        #Output('eventsprofile_genre', 'options'),
        Output('eventsprofile_toload', 'data'),
        Output('eventsprofile_removerecord_div', 'style'),
    ],
    [ 
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def eventsprofile_populatefields(pathname, search):
    if pathname == '/events/events_profile':
        # sql ="""
        # SELECT genre_name as label, genre_id as value
        # FROM genres
        # WHERE genre_delete_ind = False
        # """
        # values = []
        # cols = ['label','value']
        # df = db.querydatafromdatabase(sql, values, cols)
        # genre_options = df.to_dict('records')

        parsed = urlparse(search)             
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0
        
        removediv_style = {'display': 'none'} if not to_load else None
    else:
        raise PreventUpdate
    return [to_load, removediv_style]

@app.callback(
    [
        Output('eventsprofile_alert', 'color'),         
        Output('eventsprofile_alert', 'children'),         
        Output('eventsprofile_alert', 'is_open'),         
        Output('eventsprofile_successmodal', 'is_open')     
    ], 
    [
        Input('eventsprofile_submit', 'n_clicks')
    ],
    [ 
        State('eventsprofile_eventname', 'value'),         
        #State('movieprofile_genre', 'value'),         
        State('eventsprofile_date', 'date'),
        State('eventsprofile_racecourse', 'value'), 
        State('url', 'search'),
        State('eventsprofile_removerecord', 'value')
    ]
)
def eventsprofile_saveprofile(submitbtn, eventname, date, racecourse, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'eventsprofile_submit' and submitbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            inputs = [eventname, date, racecourse]

            if not all(inputs):
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply all inputs'
            elif not eventname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the event name'
            elif not date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the event date'
            elif not racecourse:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the race course'
            elif len(eventname)>256:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Title is too long. Must be less than 256 characters'
            else:
                parsed = urlparse(search)             
                mode = parse_qs(parsed.query)['mode'][0]
                if mode == 'add':
                    sql = """
                        INSERT INTO race (race_name, race_date, race_course, race_delete_ind)
                        VALUES (%s, %s, %s, %s)
                    """
                    values = [eventname, date, racecourse, False]

                    db.modifydatabase(sql, values)

                    modal_open = True

                elif mode == 'edit':
                    parsed = urlparse(search)             
                    raceid = parse_qs(parsed.query)['id'][0]

                    sql = """
                        update race
                        set
                            race_name = %s,
                            race_date = %s,
                            race_course = %s,
                            race_delete_ind = %s
                        where
                            race_id = %s
                        """
                    to_delete = bool(removerecord)
                    values = [eventname, date, racecourse, to_delete, raceid]

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
        Output('eventsprofile_eventname', 'value'),                  
        Output('eventsprofile_date', 'date'), 
        Output('eventsprofile_racecourse', 'value'),
    ],
    [
        Input('eventsprofile_toload', 'modified_timestamp')
    ],
    [
        State('eventsprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def eventsprofile_loadprofile(timestamp, to_load, search):
    if to_load == 1:

        parsed = urlparse(search)             
        raceid = parse_qs(parsed.query)['id'][0]

        sql = """
            select race_name, race_date, race_course
            from race
            where race_id = %s
        """
        values = [raceid]
        col = ['eventname', 'date','racecourse']

        df = db.querydatafromdatabase(sql, values, col)

        eventname = df['eventname'][0]
        date = df['date'][0]
        racecourse = df['racecourse'][0]

        return [eventname, date, racecourse]

    else:
        raise PreventUpdate