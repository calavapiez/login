import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs


from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        html.Div(
            [
            dcc.Store(id='profilesettings_toload', storage_type='memory', data=0),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("Edit your profile")
                            ),
                            dbc.CardBody(
                                [
                                    dbc.Alert(id='profilesettings_alert', is_open=False),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Name:"),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='text',
                                                                        id='profilesettings_name', 
                                                                        placeholder='Name',
                                                                    ),
                                                                ),
                                                            ],
                                                            className="mb-3",
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Birthday:"),
                                                                dbc.Col(
                                                                    dcc.DatePickerSingle(
                                                                        id='profilesettings_bday', 
                                                                    ),
                                                                ),
                                                            ],
                                                            className="mb-3",
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("Sex:"),
                                                                dbc.Col(
                                                                    dcc.Dropdown(
                                                                        options=['Male', 'Female'],
                                                                        id="profilesettings_sex",
                                                                        clearable=True,
                                                                        searchable=True,
                                                                    ),
                                                                    className="dash-bootstrap",
                                                                ),
                                                            ],
                                                            className="mb-3",
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Label("SSN:"),
                                                                dbc.Col(
                                                                    dbc.Input(
                                                                        type='number',
                                                                        id='profilesettings_ssn', 
                                                                        placeholder='SSN',
                                                                    ),
                                                                    className="dash-bootstrap",
                                                                ),
                                                            ],
                                                            className="mb-3",
                                                        ),
                                                    ]
                                                ),
                                                className="m-4",
                                            ),
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                        dbc.Row(
                                                                [
                                                                    dbc.Label("Contact Number:"),
                                                                    dbc.Col(
                                                                        dbc.Input(
                                                                            type='text',
                                                                            id='profilesettings_mobile', 
                                                                            placeholder='Contact Number',
                                                                        ),
                                                                    ),
                                                                ],
                                                                className="mb-3",
                                                            ),
                                                        dbc.Row(
                                                                [
                                                                    dbc.Label("Address:"),
                                                                    dbc.Col(
                                                                        dbc.Textarea(
                                                                            id='profilesettings_address', 
                                                                            placeholder='Address',
                                                                        ),
                                                                    ),
                                                                ],
                                                                className="mb-3",
                                                            ),
                                                    ]
                                                ),
                                                className="m-4",
                                            ),
                                        ]                        
                                    ),
                                ]
                            ),
                        ],
                    ),
                    width=8
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("Account Settings")
                            ),
                            dbc.CardBody(
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Label("Email:"),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='email',
                                                        id='profilesettings_email', 
                                                        placeholder='Email',
                                                    ),
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Username:"),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='profilesettings_user', 
                                                        placeholder='Username',
                                                    ),
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("Password:"),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='password',
                                                        id='profilesettings_pw', 
                                                        placeholder='Password',
                                                    ),
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label("New password:"),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='password',
                                                        id='profilesettings_newpw', 
                                                        placeholder='New password',
                                                    ),
                                                ),
                                            ],
                                            className="mb-3",
                                        ),
                                    ]
                                ),
                                className="m-4",
                            ),
                        ]
                    ),
                    width=4
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Button(
                "Save",
                id='profilesettings_savebtn',
                className="ml-3",
                n_clicks=0
            )
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Great!")
                ),
                dbc.ModalBody("Your profile changes has been saved succesfully!", id='profilesettings_feedback'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", 
                        id='profilesettings_closebtn', 
                        className="ms-auto",
                        href='/profile', 
                        n_clicks=0
                    )
                ),
            ],
            centered=True,
            backdrop='static',
            id='profilesettings_modal',
        ),
    ]
)


@app.callback(
    [
        Output('profilesettings_name', 'value'),
        Output('profilesettings_email', 'value'),
        Output('profilesettings_user', 'value'),
        Output('profilesettings_bday', 'date'),
        Output('profilesettings_sex', 'value'),
        Output('profilesettings_mobile', 'value'),
        Output('profilesettings_address', 'value'),
        Output('profilesettings_ssn', 'value'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def profile_loadpersonalinfo(pathname, search):
    if pathname == '/profile/profile_settings':
        parsed = urlparse(search)
        ptcptid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT ptcpt_name, email, username, brt_dt, gender, mobile_num, address, ssn 
            FROM participant
            WHERE ptcpt_id = %s
        """
        values = [ptcptid]
        cols = ['name', 'email', 'username', 'birthday', 'sex', 'mobile', 'address', 'ssn']
        
        df = db.querydatafromdatabase(sql, values, cols)

        name = df['name'][0]
        email = df['email'][0]
        username = df['username'][0]
        birthday = df['birthday'][0]
        sex = df['sex'][0]
        mobile = df['mobile'][0]
        address = df['address'][0]
        ssn = df['ssn'][0]
        
    else:
        raise PreventUpdate
    
    return [name, email, username, birthday, sex, mobile, address, ssn]


@app.callback(
    [
        Output('profilesettings_alert', 'color'),         
        Output('profilesettings_alert', 'children'),         
        Output('profilesettings_alert', 'is_open'),  
        Output('profilesettings_modal', 'is_open'),
        # Output('profilesettings_closebtn', 'href'),       
    ],
    [
        Input('profilesettings_savebtn', 'n_clicks'),
        # Input('profilesettings_closebtn', 'n_clicks'),
    ],
    [
        State('profilesettings_name', 'value'),
        State('profilesettings_email', 'value'),
        State('profilesettings_user', 'value'),
        State('profilesettings_bday', 'date'),
        State('profilesettings_sex', 'value'),
        State('profilesettings_mobile', 'value'),
        State('profilesettings_address', 'value'),
        State('profilesettings_ssn', 'value'),
        State('url', 'search'),
        # State('movieprof_removerecord', 'value'),
    ]
)
def movieprofile_saveprofile(savetbtn, name, email, user, bday, sex, mobile, address, ssn, search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'profilesettings_savebtn' and savetbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            inputs = [
                name, 
                email, 
                user, 
                bday, 
                sex, 
                mobile, 
                address, 
                ssn
            ]

            if not all(inputs):
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please supply all inputs'
            elif len(ssn)>9:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'SSN is too long. Must be 9 digits'
            elif len(ssn)<9:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'SSN is too short. Must be 9 digits'
            else:
                parsed = urlparse(search)             
                ptcptid = parse_qs(parsed.query)['id'][0]

                sql = """
                    UPDATE participant 
                    SET 
                        ptcpt_name = %s,
                        email = %s,
                        username = %s,
                        brt_dt = %s,
                        gender = %s,
                        mobile_num = %s,
                        address = %s,
                        ssn = %s
                    WHERE ptcpt_id = %s;
                """

                values = [name, email, user, bday, sex, mobile, address, ssn, ptcptid]

                db.modifydatabase(sql, values)
                modal_open = True
        
            return[alert_color, alert_text, alert_open, modal_open] 
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate