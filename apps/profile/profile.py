import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from urllib.parse import urlparse, parse_qs
import pandas as pd

from app import app
from apps import dbconnect as db



layout = html.Div(
    [   
        html.Div(
            [
            dcc.Store(id='profile_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2("My Profile"),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(src='assets/images/profile-picture.png', alt='profile picture', 
                                        width='375px', height='300px', className='center'),
                                html.H6("Change picture", style={'text-align': 'center', 'font-style': 'italic'}),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H4("insert name here", id='profile_name'),
                                                html.H6("insert email here",id='profile_email'),
                                                html.H6("insert username here", style={'font-style':'italic'}, id='profile_user'),
                                                html.Br(),
                                                
                                                html.H5("Personal Details"),
                                                html.H6(
                                                    [
                                                        html.Span("insert age here", id='profile_age'),
                                                        html.Span(" "),
                                                        html.Span("insert birthday here", id='profile_bday'),
                                                    ]
                                                ),
                                                html.H6("insert gender here", id='profile_sex'),
                                                html.Br(),

                                                html.H5("Contact Information"),
                                                html.H6("insert mobile number here", id='profile_mobile'),
                                                html.H6("Insert address here", id='profile_address'),
                                                html.Br(),

                                                html.H5("SSN"),
                                                html.H6("insert ssn here", id='profile_ssn'),
                                            ],
                                        ),
                                        className="mb-3",
                                    ),
                                ),
                                dbc.Button(
                                    'Settings',
                                    href='/profile/profile_settings',
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H6("PR", style={'font-style':'italic'}),
                                                                html.H4("Insert PR here", id='profile_pr')
                                                            ]                                                    
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H6("Avrg. Time", style={'font-style':'italic'}),
                                                                html.H4("Insert average time here", id='profile_avrg')
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.Br(),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H6("Joined", style={'font-style':'italic'}),
                                                                html.H4("Insert num. of races joined here", id='profile_joined')
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H6("Completed", style={'font-style':'italic'}),
                                                                html.H4("Insert num. of completed races here", id='profile_completed')
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ],
                                            style={'text-align': 'center'}
                                        ),
                                        className="mb-3",
                                    ),
                                ),
                                dbc.Button(
                                    'See more',
                                    href='/profile/profile_records',
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)


@app.callback(
    [
        Output('profile_name', 'children'),
        Output('profile_email', 'children'),
        Output('profile_user', 'children'),
        Output('profile_age', 'children'),
        Output('profile_bday', 'children'),
        Output('profile_sex', 'children'),
        Output('profile_mobile', 'children'),
        Output('profile_address', 'children'),
        Output('profile_ssn', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def profile_loadpersonalinfo(pathname, search):
      
    if pathname == '/profile':
        parsed = urlparse(search)
        ptcptid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT ptcpt_name, email, username, 
                CONCAT(CAST(DATE_PART('year',AGE(brt_dt)) AS varchar(10)), ' years old'), 
                CONCAT('(', TO_CHAR(brt_dt, 'Mon dd, yyyy'), ')'), 
                gender, mobile_num, address, ssn 
            FROM participant
            WHERE ptcpt_id = %s
        """
        values = [ptcptid]
        cols = ['name', 'email', 'username', 'age', 'birthday', 'sex', 'mobile', 'address', 'ssn']
        
        df = db.querydatafromdatabase(sql, values, cols)

        name = df['name'][0]
        email = df['email'][0]
        username = df['username'][0]
        age = df['age'][0]
        birthday = df['birthday'][0]
        sex = df['sex'][0]
        mobile = df['mobile'][0]
        address = df['address'][0]
        ssn = df['ssn'][0]
        
    else:
        raise PreventUpdate
    
    return [name, email, username, age, birthday, sex, mobile, address, ssn]


@app.callback(
    [
        Output('profile_pr', 'children'),
        Output('profile_avrg', 'children'),
        Output('profile_joined', 'children'),
        Output('profile_completed', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def profile_loadraceinfo(pathname, search):
    if pathname == '/profile':
        parsed = urlparse(search)
        ptcptid = parse_qs(parsed.query)['id'][0]

        sql = """
            SELECT MIN(run_tm), TO_CHAR(AVG(run_tm), 'HH24:MI:SS'), count(run_tm), count(run_tm) filter(where cmplt=B'1')
            from individual_race_record
            where ptcpt_id=%s;
        """
        values = [ptcptid]
        cols = ['pr', 'avrg', 'joined', 'completed']
        
        df = db.querydatafromdatabase(sql, values, cols)

        pr = df['pr'][0]
        avrg = df['avrg'][0]
        joined = df['joined'][0]
        completed = df['completed'][0]
        
    else:
        raise PreventUpdate
    
    return [pr, avrg, joined, completed]
