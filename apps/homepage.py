import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table 
import dash 
from dash.exceptions import PreventUpdate 

from app import app

layout = html.Div(
    [   dbc.Card(
    [
        dbc.CardImg(
            #input img src
            src="/assets/images/BB10K1.webp",
            top=True,
            style={"opacity": 0.5, "width":"auto"},
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4("Bolder Boulder Race 2023", className="card-title"),
                    html.P(
                        "Register for this year's race, "
                        "happening on May 29, 2023!",
                        className="card-text",
                    ),
                    dbc.Button("Register", color="primary"),
                    #INSERT LINK TO REG PAGE
                ],
            ),
        ),
    ],
    style={"width": "18rem"},
), 
        html.Br(),
        html.Div(
            [
                html.Span(
                     "The BB10K is for everybody: part race, run, walk, tribute and holiday celebration.",
                     style={'font-style': 'bold'}
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "!!!",
                    style={'font-style':'italic'}
                ),
            ]
        )
    ]
)