import ast
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from navbar import Navbar

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('dybilal.csv')
df.date = pd.to_datetime(df.date).dt.date
df['date_int'] = pd.to_datetime(df.date).astype(np.int64)//1e9

for col in df.columns:
    if type(df[col][0]) is str:
        if '%' in df[col][0]:
            df[col] = df[col].apply(lambda x: int(x[:-1]))

players = df['Player_Name'].unique()
Map_names = ['All Maps', 'Inferno', 'Dust2', 'Mirage', 'Overpass', 'Cache', 'Vertigo']
mname = ['.*', 'inferno', 'dust', 'mirage', 'overpass', 'cache', 'vertigo']
Features= df.columns[3:-7]


nav = Navbar()

page_2 = html.Div([
    html.H1(children='CSGO Stats : DYBILAL Edition.'),

    html.Div(children='''
        Les stats indivduelles : le règne de la kékette.
    '''),


## PREMIER GRAPH : RADPLOT SUR STATS INDIVS PAR MAP

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-feature-rad',
                options=[{'label': i, 'value': i} for i in Features],
                value='Kills'
            )
    ], style={'width': '75%', 'display': 'inline-block'}
    ),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-column1-rad',
                options=[{'label': i, 'value': j} for i,j in zip(Map_names, mname)],
                value='.*'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-column2-rad',
                options=[{'label': i, 'value': j} for i,j in zip(Map_names, mname)],
                value='.*'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
        )], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'}
    ),

        html.Div([
        dcc.Graph(
            id='crossfilter-indicator-radial1',
            hoverData={}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
    ),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-radial2',
            hoverData={}
        )
    ], style={'display': 'inline-block', 'width': '49%', 'float':'right','borderBottom': 'thin lightgrey solid'}
    ),

    # DEUXIÈME GRAPH DISTPLOT

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-map-scat',
                options=[{'label': i, 'value': j} for i,j in zip(Map_names, mname)],
                value='.*'
            )
        ], style={'width': '49%', 'display': 'inline-block'
        }),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-feat-scat',
                options=[{'label': i, 'value': i} for i in Features],
                value='Kills'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'}
    ),

    html.Div([
        dcc.Graph(
            id='crossfilter-player-scatterplot',
        )
    ], style={'width': '99%', 'display': 'inline-block'}),


    # TROISEME GRAPH SCATTER + CALLBACK MAP

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in df.Player_Name.unique()],
                value='Blhoux'
            )
            ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': j} for i,j in zip(Map_names, mname)],
                value='.*'
            )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-feat',
                options=[{'label': i, 'value': i} for i in Features],
                value='Kills'
            )
            ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-feat',
                options=[{'label': i, 'value': i} for i in Features],
                value='Deaths'
            )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': '8379122'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block',"margin-top": "25px"}),

    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%', "margin-top": "25px"}),

    html.Div(dcc.Slider(
        id='crossfilter-date-slider',
        min=df.date_int.min(),
        max=df.date_int.max(),
        value=df.date_int.max(),
        marks={str(epoch): str(date) for epoch,date in df[['date_int', 'date']].drop_duplicates().sort_values(by='date').iloc[::10].to_numpy()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

    html.Div(id='app-1-display-value'),
    dcc.Link('Team Stats', href='/apps/app1'),
    html.Div(id='app-1-display-value'),
    dcc.Link('Time Stats', href='/apps/app3')
])


output = html.Div(id = 'output',
                children = [],
                )

header = html.H3(
    'Select the stats you want!'
)

def App2():
    layout = html.Div([
        nav,
        header,
        page_2,
        output
    ])
    return layout



# if __name__ == '__main__':
#     app.run_server(debug=True)
