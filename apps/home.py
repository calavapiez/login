import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table 
import dash 
from dash.exceptions import PreventUpdate 
import pandas as pd

from app import app

layout = html.Div(
    [
        html.H2('Welcome to our app!'),
        html.Hr(),
        html.Div(
            "This is the homepage"
        )
    ]
)