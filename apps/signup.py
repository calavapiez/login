import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Enter the details'),
        html.Hr(),
        dbc.Alert('Please supply details.', color="danger", id='signup_alert',
                  is_open=False),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_username", placeholder="Enter a username"
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
                        type="password", id="signup_password", placeholder="Enter a password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(" Confirm Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_passwordconf", placeholder="Re-type the password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label("Full Name", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_participantname", placeholder="Enter your full name"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label("Social Security Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_ssn", placeholder="Enter your Social Security Number, if you don't have one, please leave this blank"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label("Address", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_address", placeholder="Enter your address"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label("Gender", width=2),
                dbc.Col(
                    dcc.Dropdown(['Male', 'Female'],
                         id="signup_gender", placeholder="Select your biological gender"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label("Birthdate", width=2),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='signup_birthdate',
                        placeholder='Select your birthdate',
                        month_format='MMM Do, YY'
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [ 
                dbc.Label("Personal Record", width=2),
                dbc.Col(
                    dbc.Input(
                        type='text',
                        id='signup_pr',
                        placeholder='Input personal record run time as HH:MM:SS'
                    ),
                    width=6
                )
            ], 
            className="mb-3",
        ),

        dbc.Button('Sign up', color="secondary", id='signup_signupbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                dbc.ModalBody("User has been saved", id='signup_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/'
                    )
                ),
            ],
            id="signup_modal",
            is_open=False,
        ),
    ]
)


# disable the signup button if passwords do not match
@app.callback(
    [
        Output('signup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('signup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_username', 'value'),
        State('signup_password', 'value'),
        State('signup_ssn', 'value'),
        State('signup_birthdate', 'date'),
        State('signup_participantname', 'value'),
        State('signup_pr', 'value'),
        State('signup_address', 'value'),
        State('signup_gender', 'value'),
    ]
)
def saveuser(loginbtn, username, password, ssn, birthdate, participantname, pr, address, gender):
    openalert = openmodal = False
    inputs = [username, password, birthdate, participantname, pr, address, gender]
    if loginbtn:
        if all(inputs):
            sql = """INSERT INTO users (user_name, user_password)
            VALUES (%s, %s);
            
            INSERT INTO participant (ssn, brt_dt, ptcpt_name, pr, address, gender, ptcpt_delete_ind)
            VALUES (%s, %s, %s, %s, %s, %s, False)"""  
            
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins should see
            # user passwords 
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [username, encrypt_string(password), ssn, birthdate, participantname, pr, address, gender]
            db.modifydatabase(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]

# @app.callback(
#     [
#         Output('signup_alert', 'is_open'),
#         Output('signup_modal', 'is_open')   
#     ],
#     [
#         Input('singup_signupbtn', 'n_clicks')
#     ],
#     [
#         State('signup_ssn', 'value'),
#         State('signup_birthdate', 'value'),
#         State('signup_participantname', 'value'),
#         State('signup_pr', 'value'),
#         State('signup_address', 'value'),
#         State('signup_gender', 'value'),
#     ]
# )
# def saveuserinfo(loginbtn, ssn, birthdate, participantname, pr, address, gender):
#     openalert = openmodal = False
#     if loginbtn:
#         if ssn and birthdate and participantname and pr and address and gender:
#             sql = """INSERT INTO participant (ssn, brt_dt, ptcpt_name, pr, address, gender, ptcpt_delete_ind)
#             VALUES (%s, %s, %s, %s, %s, False)"""  
            
#             # This lambda fcn encrypts the password before saving it
#             # for security purposes, not even database admins should see
#             # user passwords 
            
            
#             values = [ssn, birthdate, participantname, pr, address, gender]
#             db.modifydatabase(sql, values)
            
#             openmodal = True
#         else:
#             openalert = True
#     else:
#         raise PreventUpdate

#     return [openalert, openmodal]