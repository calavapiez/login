import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Please Login'),
        html.Hr(),
        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert',
                  is_open=False),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="login_username", placeholder="Enter username"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="login_password", placeholder="Enter password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button('Login', color="secondary", id='login_loginbtn'),
        html.Hr(),
        html.A('Signup Now!', href='/signup'),
    ]
)


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
        Output('currentrole', 'data')
    ],
    [
        Input('login_loginbtn', 'n_clicks')
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
        State('currentrole', 'data')
    ]
)
def loginprocess(loginbtn, username, password,
                 sessionlogout, currentuserid, currentrole):
    openalert = False
    
    if loginbtn and username and password:
        sql = """SELECT user_id, org_id
        FROM users
        WHERE 
            user_name = %s AND
            user_password = %s AND
            NOT user_delete_ind"""
        
        # we match the encrypted input to the encrypted password in the db
        encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
         
        values = [username, encrypt_string(password)]
        cols = ['userid','org_id']
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape[0]: # if query returns rows
            currentuserid = df['userid'][0]
            currentrole = df['org_id'][0]
        else:
            currentuserid = -1
            currentrole = -1
            openalert = True
        
    else:
        raise PreventUpdate
    
    return [openalert, currentuserid, currentrole]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'),
        State('currentrole', 'data') 
    ]
)
def routelogin(logintime, userid, currentrole):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0 or currentrole > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]