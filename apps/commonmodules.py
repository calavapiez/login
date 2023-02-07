import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app

navlink_style = {
    'color': '#fff',
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("The Annual Boulder Bolder Race", className="ml-2", 
                                            style={'margin-right': '2em'})),
                ],
                align="center",
                className="g-0"
            ),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("About Us", href="/about", style=navlink_style),
        dbc.NavLink("Contact Us", href="/contact", style=navlink_style),
        dbc.NavLink("Events", href="/events/events_home", style=navlink_style),
        dbc.NavLink("Profile", href="/profile", style=navlink_style),
        dbc.NavLink("Database", href="/database", style=navlink_style),
        dbc.NavLink("Management", href="/management", style=navlink_style),
        dbc.NavLink("Logout", href="/logout", style=navlink_style)

    ],
    dark=True,
    color='dark'
)