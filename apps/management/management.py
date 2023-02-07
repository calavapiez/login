import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        html.H2("Data Reports"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                html.H4("List of Winners"),
                                ),
                                dbc.Col(
                                    dcc.Dropdown(['Male Open', 'Female Open', 'Male Master Open', 'Female Master Open'],
                                    value = 'Male Open',
                                    clearable = False, id='management_categoryfilter'
                                    )
                                ),
                            ],
                            className="mb-3"
                        ),
                        html.Div(
                            "This will contain the table for the list of winners per category during the past 5 races",
                            id='management_winners'
                        )
                    ],
                    style={"margin-right": "2em"}
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            html.H4("Number of Participants"),
                            className="mb-3"
                        ),
                        html.Div(
                            "This will contain the table for the number of participants during the past 10 years",
                            id='management_count'
                        ),
                        
                    ]
                ),
            ],
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            html.H4("List of Elite Runners"),
                            className="mb-3"
                        ),
                        html.Div(
                            "This will contain the table for the current list of elite runners",
                            id='management_elite'
                        ),
                        
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            html.H4("List of Runners in the Current Race"),
                            className="mb-3"
                        ),
                        html.Div(
                            "This will contain the table for the list of runners in the current race",
                            id='management_currentrunners'
                        ),
                        
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                html.H4("Running Time of Winners"),
                                ),
                                dbc.Col(
                                    dcc.Dropdown(['Overall', 'Male Open', 'Female Open', 'Male Master Open', 'Female Master Open'],
                                    value = 'Overall',
                                    clearable = False, id='management_graphfilter'
                                    )
                                ),
                            ],
                            className="mb-3"
                        ),
                        dcc.Graph(id='management_winnersgraph'),
                        # html.Div(
                        #     "This will contain the graphs for the running time of winners per category during the last 10 races",
                        #     id='management_winnersgraph'
                        # )
                    ],
                    style={"margin-right": "2em"}
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            html.H4("Age of Youngest Players"),
                            className="mb-3"
                        ),
                        dcc.Graph(id='management_agegraph'),
                        # html.Div(
                        #     "This will contain the graph of the youngest players each race during the past 10 years",
                        #     id='management_youngestgraph'
                        # ),
                        
                    ]
                ),
            ]
        ),        
    ]
)


@app.callback(
    [
        Output('management_winners', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('management_categoryfilter', 'value'),
    ]
)
def updatewinnerslist(pathname, filtervalue):
    if pathname == '/management':
        sql = """
            SELECT rank_filter.* FROM(
                SELECT
                    race_name, 
                    TO_CHAR(race_date, 'Mon dd, yyyy'), 
                    run_tm, 
                    ptcpt_name,
                    RANK () OVER(
                        PARTITION BY r.race_id
                        ORDER BY irr.run_tm
                    )
                FROM 
                    race r
                    INNER JOIN individual_race_record irr 
                        ON r.race_id = irr.race_id
                    INNER JOIN participant p 
                        ON p.ptcpt_id = irr.ptcpt_id
                WHERE r.race_date > current_date - interval '5 years'
        """
        
        val = []
        colnames = ['Event Name', 'Date', 'Run Time', 'Name', 'Rank']

        if filtervalue == 'Male Open':
            sql += """ AND p.gender = 'Male'"""
        elif filtervalue == 'Female Open':
            sql += """ AND p.gender = 'Female'"""
        if filtervalue == 'Male Master Open':
            sql += """ AND p.gender = 'Male' AND AGE(NOW(), p.brt_dt) > interval '40 years'"""
        elif filtervalue == 'Female Master Open':
            sql += """ AND p.gender = 'Female' AND AGE(p.brt_dt) > interval '40 years'"""
        

        sql += """) rank_filter WHERE RANK = 1"""

        races = db.querydatafromdatabase(sql, val, colnames)
        
        if races.shape[0]:
            races.drop('Rank', axis=1, inplace=True),
            
            table = dbc.Table.from_dataframe(races, striped=True, bordered=True, hover=True, size='sm')
            return [table]

        else:
            return ["No records to display."] 
    else:
        raise PreventUpdate
    

@app.callback(
    [
        Output('management_count', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ]
)
def updatecountlist(pathname):
    if pathname == '/management':
        sql = """
            SELECT 
                r.race_name, 
                EXTRACT(YEAR FROM r.race_date), 
                COALESCE(sub.num, 0)
            FROM (
                SELECT race_id, COUNT(ptcpt_id) AS num
                FROM 
                    individual_race_record 
                GROUP BY
                    race_id
            ) sub
            RIGHT JOIN race r
                    ON r.race_id = sub.race_id
            WHERE r.race_date > current_date - interval '10 years'
            ORDER BY
                r.race_date DESC        
        """
        
        val = []
        colnames = ['Event Name', 'Year', 'Participants']

        races = db.querydatafromdatabase(sql, val, colnames)
        
        if races.shape[0]:
            table = dbc.Table.from_dataframe(races, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return ["No records to display."] 
    else:
        raise PreventUpdate
    

@app.callback(
    [
        Output('management_elite', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ]
)
def updateelitelist(pathname):
    if pathname == '/management':
        sql = """
            SELECT 
                p.ssn,
                p.ptcpt_name,
                p.address,
                p.brt_dt,
                p.gender,
                COALESCE(CAST(comb.prev AS varchar), 'N/A'),
                comb.pr
            FROM (
                SELECT 
                    pr_time.ptcpt_id,
                    pr_time.pr,
                    prev_time.prev
                FROM (
                    SELECT 
                        ptcpt_id,
                        MIN(time) AS pr
                    FROM (
                        SELECT ptcpt_id, pr AS time FROM participant 
                        UNION ALL
                        SELECT ptcpt_id, run_tm AS time FROM individual_race_record		
                    ) recorded_times
                    GROUP BY ptcpt_id
                ) pr_time
                LEFT JOIN (
                    SELECT ptcpt_id, run_tm AS prev FROM individual_race_record 
                    WHERE race_id=(SELECT max(race_id) FROM race)
                ) prev_time
                    ON pr_time.ptcpt_id = prev_time.ptcpt_id
            ) comb
            INNER JOIN participant p 
                ON p.ptcpt_id = comb.ptcpt_id
            WHERE ((comb.pr < interval '41 mins' AND p.gender='Female') 
            OR (comb.pr < interval '38 mins' AND p.gender='Male')) 
        """

        val = []
        colnames = ['SSN', 'Name', 'Address', 'Birthday', 'Gender', 'Run Time During Last Race', 'Personal Record']

        elites = db.querydatafromdatabase(sql, val, colnames)
        
        if elites.shape[0]:
            table = dbc.Table.from_dataframe(elites, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return ["No records to display."] 
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('management_currentrunners', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ]
)
def updatecurrentlist(pathname):
    if pathname == '/management':
        sql = """
            SELECT 
                p.ptcpt_name,
                DATE_PART('year', AGE(p.brt_dt)) AS age,
                p.gender,
                irr.run_tm
            FROM participant p
            INNER JOIN individual_race_record irr
                ON irr.ptcpt_id = p.ptcpt_id
            WHERE irr.race_id=(SELECT max(race_id) FROM race)
            ORDER BY age, p.gender, irr.run_tm
        """

        val = []
        colnames = ['Name', 'Age', 'Gender', 'Run Time']

        runners = db.querydatafromdatabase(sql, val, colnames)
        
        if runners.shape[0]:
            table = dbc.Table.from_dataframe(runners, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        
        else:
            return ["No records to display."] 
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('management_winnersgraph', 'figure'),
    ],
    [
        Input('url', 'pathname'),
        Input('management_graphfilter', 'value'),
    ]
)
def updatewinnersgraph(pathname, filtervalue):
    if pathname == '/management':
        sql = """
            SELECT rank_filter.* FROM(
                SELECT
                    EXTRACT(YEAR FROM race_date),
                    run_tm, 
                    ptcpt_name,
                    RANK () OVER(
                        PARTITION BY r.race_id
                        ORDER BY irr.run_tm
                    )
                FROM 
                    race r
                    INNER JOIN individual_race_record irr 
                        ON r.race_id = irr.race_id
                    INNER JOIN participant p 
                        ON p.ptcpt_id = irr.ptcpt_id
                WHERE r.race_date > current_date - interval '10 years'
        """

        if filtervalue == 'Male Open':
            sql += """ AND p.gender = 'Male'"""
        elif filtervalue == 'Female Open':
            sql += """ AND p.gender = 'Female'"""
        if filtervalue == 'Male Master Open':
            sql += """ AND p.gender = 'Male' AND AGE(NOW(), p.brt_dt) > interval '40 years'"""
        elif filtervalue == 'Female Master Open':
            sql += """ AND p.gender = 'Female' AND AGE(p.brt_dt) > interval '40 years'"""
        
        sql += """) rank_filter WHERE RANK = 1"""

        val = []
        colnames = ['Year', 'Run Time', 'Name', 'Rank']

        runtime = db.querydatafromdatabase(sql, val, colnames)  
        runtime['Run Time'] = pd.to_datetime(runtime['Run Time'].astype(str))

        if runtime.shape[0]:    
            fig = px.line(runtime, x="Year", y="Run Time", hover_name="Name", markers=True)
            fig.update_layout(yaxis_tickformat='%H:%M:%S')
            
            return [fig]
        else:
            fig = px.line()
            fig.update_layout(
                xaxis =  { "visible": False },
                yaxis = { "visible": False },
                paper_bgcolor="white",
                plot_bgcolor="white", 
                annotations = 
                [
                    {   
                        "text": "No records to display",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 15
                        }
                    }
                ]
            )
            return [fig] 
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('management_agegraph', 'figure'),
    ],
    [
        Input('url', 'pathname'),
    ]
)
def updatewinnersgraph(pathname):
    if pathname == '/management':
        sql = """
            SELECT * FROM (
                SELECT r.race_name,
                       EXTRACT(YEAR FROM r.race_date) AS "year",
                       DATE_PART('year', r.race_date) - DATE_PART('year', p.brt_dt) AS age,
                       p.ptcpt_name
                FROM       participant            p
                INNER JOIN individual_race_record irr ON p.ptcpt_id = irr.ptcpt_id
                INNER JOIN race                   r   ON r.race_id = irr.race_id
                WHERE r.race_date > current_date - interval '10 years'
                ORDER BY DENSE_RANK() OVER(
                            PARTITION BY race_name 
                            ORDER     BY r.race_date - p.brt_dt)
                FETCH FIRST 1 ROWS WITH TIES
            ) subquery
            ORDER BY year DESC
        """
        
        val = []
        colnames = ['Event Name', 'Year', 'Age', 'Participant']

        age = db.querydatafromdatabase(sql, val, colnames)
        
        if age.shape[0]:

            fig = px.line(age, x="Year", y="Age", hover_name="Participant", markers=True)
            return [fig]

        else:
            return ["No records to display."] 
    else:
        raise PreventUpdate





"""
with mat_age as (
    select DEPARTMENT, date_part('year', age(CREATEDATE)) as mage
    from Materials
)
select
    DEPARTMENT,
    count(*) filter (where mage<10) as "age<10",
    count(*) filter (where mage>=10 and mage<20) as "10<age<20",
    count(*) filter (where mage>=20) as "20<age"
from
    mat_age
group by
    DEPARTMENT;


SELECT COUNT(id) FILTER (WHERE (age < 18)) AS "Under 18",
       COUNT(id) FILTER (WHERE (age >= 18 AND age <= 24)) AS "18-24",
       COUNT(id) FILTER (WHERE (age >= 25 AND age <= 34)) AS "25-34"
FROM contacts

 
COALESCE(CAST(min.age AS varchar), 'N/A') FROM(

"""
