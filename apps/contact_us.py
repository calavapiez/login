import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table 
import dash 
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div(
    [
        html.H2('Contact Us'),
        html.Hr(),
        html.Div(
            [
                dbc.Col(
                    html.Div(
                        "Contact us for any inquery via email, phone or any of our social media pages. We would be glad to answer your questions and assist you in a any way.",
                        ),
                ),
                dbc.Col(
                    html.Div(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                html.H4("Mobile Phone"),
                                html.Hr,
                                html.H4("+xx xxx xxx xxxx"),
                                html.Hr,
                                html.H4("Landline"),
                                html.Hr,
                                html.H4("xx xxxx xxxx"),
                                html.Br,
                                html.H4("race.inqueries@gmail.com"),
                                html.Hr,
                                html.H4("race.organizers@gmail.com"),
                                html.Hr,
                            )
                        )
                    ]
                    ),
                ),
            ],
        ),
        
        ]
)
