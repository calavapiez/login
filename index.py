import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser

from app import app
from apps import commonmodules as cm
from apps import adminmodules as am
from apps import home
from apps import login
from apps import signup
from apps.events import events_home
from apps.events import events_profile
from apps.events import events_results
from apps.events import events_results_profile
from apps.profile import profile
from apps.profile import profile_settings 
from apps.profile import profile_records 
from apps.management import management

CONTENT_STYLE = {
    "margin-top": "2em",
    "margin-left": "1em",     
    "margin-right": "1em",     
    "padding": "1em 1em", 
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        #cm.navbar,

        dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        
        html.Div(
            # cm.navbar,
            id='navbar_div'
        ),

        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


@app.callback(
    [
        Output('page-content', 'children'),
        Output('navbar_div', 'style'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('currentrole', 'data')
    ]
)
def displaypage(pathname, sessionlogout, currentuserid, currentrole):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0] 
    else: 
        raise PreventUpdate

    if eventid == 'url':
        print(currentuserid, currentrole, pathname)
        if currentuserid < 0:
            if pathname in ['/']:
                returnlayout = login.layout
            elif pathname == '/signup':
                returnlayout = signup.layout
            else:
                returnlayout = '404: request not found'
       
        else:
            if pathname == '/logout':
                returnlayout = login.layout
                sessionlogout = True
            elif pathname == '/' or pathname == '/home':
                returnlayout = home.layout
            elif pathname == '/about':
                returnlayout = "insert about info here"
            elif pathname == '/contact':
                returnlayout = "insert contact details here"

            elif pathname == '/events/events_home':
                returnlayout = events_home.layout
            elif pathname == '/events/events_profile':
                returnlayout = events_profile.layout
            elif pathname == '/events/events_results':
                returnlayout = events_results.layout
            elif pathname == '/events/events_results_profile':
                returnlayout = events_results_profile.layout

            elif pathname == '/profile':
                returnlayout = profile.layout
            elif pathname == '/profile/profile_settings':
                returnlayout = profile_settings.layout
            elif pathname == '/profile/profile_records':
                returnlayout = profile_records.layout
            
            elif pathname == '/database':
                returnlayout = "insert database here"

            elif pathname == '/management':
                returnlayout = management.layout

            else:
                returnlayout = 'error404'
                
        if currentrole > 0:
            navbar_div = am.navbar
        elif currentrole < 0: 
            navbar_div = cm.navbar
    else:
        raise PreventUpdate
    
    # if currentrole > 0:
    #     navbar_div = am.navbar
    # elif currentrole < 0: 
    #         navbar_div = cm.navbar
    # else:
    #     raise PreventUpdate

    navbar_div = {'display': 'none' if sessionlogout else 'unset'}
    return [returnlayout, navbar_div, sessionlogout]


# @app.callback(
#     [
#         Output('navbar_div', 'style'),
#     ],
#     [
#         Input('currentrole', 'data'),
#     ],
#     # [
#     #     State('currentrole', 'data'),
#     # ]
# )
# def displaynavbar(currentrole):
#     if currentrole < 0:
#         navbar_div = cm.navbar
#     elif currentrole > 0:
#         navbar_div = am.navbar
#     else:
#         raise PreventUpdate
    
#     return [navbar_div]


if __name__ == '__main__':     
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)     
    app.run_server(debug=False)