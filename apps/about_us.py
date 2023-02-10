import dash_core_components as dcc 
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table 
import dash 
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div(
    #FOR DIV WITH MULTIPLE CHILDREN USE []
    dbc.Accordion(
        [
            dbc.AccordionItem(
                html.Div(
                [
                    
                    html.H3("OUR COMMITMENT"),
                    html.Hr,
                    html.P(
                        "Organizing, presenting and managing the BOLDERBoulder is part art and part science. It takes 364 days of dreaming, brainstorming, planning, and sweat to stage the best road race on the planet.",
                        "Our passion and commitment is to deliver an amazing experience for all 50,000+ participants, 100,000+ spectators and 3000+ volunteers.",
                        "And we aspire to make the experience better, year after year.",
                        " ",
                        "We are proud to be recognized as “America's All-time Best 10K” by Runners World Magazine, and we strive to deliver on that honor every day.",
                    ),
                ]
                ), title="Commitment",
            ),
            dbc.AccordionItem(
                html.Div(
                [
                    dbc.Carousel(
                        items=[
                            #FILL THIS WITH ACTUAL PHOTOS
                            #{"key": "1", "src": "/static/images/slide1.svg"},
                            #{"key": "2", "src": "/static/images/slide2.svg"},
                            #{"key": "3", "src": "/static/images/slide3.svg"},
                        ],
                        controls=True,
                        indicators=False,
                    ),
                ],
                ), title="Gallery"
            ),
            dbc.AccordionItem(
                
                html.Div(
                [    html.H4("Are there finisher medals?"),
                    html.Hr,
                    html.P(
                        "There are award medals for the top 15 male and female runners after official race results have been posted.",
                        " ",
                        "BOLDERBoulder does not have general finisher medals. However, once you cross the finish line you will receive an awesome goody bag, and a front row seat to the BOLDERBoulder Memorial Day tribute!",
                        " ",
                        "Also, a printable finisher's certificate with all of your race stats will be emailed to you a few weeks after the race. ",
                    ),
                    html.Hr,
                    html.H4("Is there a refund or cancellation policy?"),
                    html.Hr,
                    html.P(
                        "All entry fees are non-refundable. During the registration process acknowledgment of this policy is made. Once a runner registers, race items will be immediately ordered and printed for a participants’ registration.",
                        " ",
                        "There are NO exceptions. In case the event can't be done in person, participants will be transferred to our virtual option.",
                    ),
                    html.Hr,
                    html.H4("I signed-up to run virtually. Can I change to run in-person?"),
                    html.Hr,
                    html.P(
                        "Yes. For $10 we will issue you a new bib number with a timing tag. If you have already received your packet and your virtual bib number, contact us at race@bolderboulder.com with your request.",
                    )
                ]
                ), title="Frequently Asked Questions"
            ),
        ],
        start_collapsed=True,
        always_open=True
    ),
)