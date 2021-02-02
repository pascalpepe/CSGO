import ast
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from navbar import Navbar


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('dybilal.csv')

for col in df.columns:
    if type(df[col][0]) is str:
        if '%' in df[col][0]:
            df[col] = df[col].apply(lambda x: int(x[:-1]))


players = df['Player_Name'].unique()
Map_names = ['All', 'Inferno', 'Dust2', 'Mirage', 'Overpass', 'Cache']
mname = ['.*', 'inferno', 'dust', 'mirage', 'overpass', 'cache']
Features= df.columns[3:-7]

def get_match_history(match):
    L = ast.literal_eval(match)

nav = Navbar()

page_3 = html.Div([
    html.H1(children='CSGO Stats : DYBILAL Edition.'),

    html.Div(children='''
        Les stats indivs au cours du temps.
    '''),


    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-map-ts',
                options=[{'label': i, 'value': j} for i,j in zip(Map_names, mname)],
                value='.*'
            )
        ], style={'width': '49%', 'display': 'inline-block'
        }),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-feat-ts',
                options=[{'label': i, 'value': i} for i in Features],
                value='Kills'
            )], 
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}
            ),
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-time-serie'
        )
    ], style={'width': '99%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2'),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')

])



output = html.Div(id = 'output',
                children = [],
                )

header = html.H3(
    'Select the stats you want!'
)

def App3():
    layout = html.Div([
        nav,
        header,
        page_3,
        output
    ])
    return layout

# if __name__ == '__main__':
    # app.run_server(debug=True)
