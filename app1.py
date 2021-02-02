# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from navbar import Navbar

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


DF = pd.read_csv('dybilal.csv')
maps = DF.map.unique().tolist()
map_colors = ['#DE9B35', '#B31B21', '#CCBA7C', '#808080', '#415D2A']
map_colors = {m:c for m,c in zip(maps, map_colors)}


# KILLS BARPLOT
DF['Total Kills'] = DF['Kills'].groupby([DF['Player_Name'],DF['map']]).transform('sum')
players = DF['Player_Name'].unique()
kills = px.bar(DF, x="Player_Name", y="Kills", color="map", barmode="group",
            hover_data=['Player_Name', 'map', 'Total Kills','Kills', 'Deaths'], 
            color_discrete_map=map_colors)
kills.update_layout(title_text="Nombres de kills par Map")

# MAPS PLAYED GRAPH
map_count = DF.groupby('Player_Name').map.value_counts()
map_count = map_count.unstack().reset_index()
map_count = pd.melt(map_count, id_vars= 'Player_Name', value_name='Occurences')
val = map_count.groupby(['Player_Name']).sum()['Occurences']

for play in players:
    map_count.loc[map_count['Player_Name']==play,'Total'] = val[play]

maps_count = px.bar(map_count, x="Player_Name", y="Occurences", color="map", barmode="stack",
                hover_data= ['Player_Name', 'map', 'Total',"Occurences"], 
            color_discrete_map=map_colors)
maps_count.update_layout(title_text="Nombres de fois où a été jouée la Map")

## WIN RATE PLOT
matches= DF.groupby('Match_id').first()
labels = matches['Match_Result'].value_counts().index
values = matches['Match_Result'].value_counts().values

win_rate = make_subplots(rows=2, cols=3, specs=[[{'type':'domain'}]*3, [{'type':'domain'}]*3], subplot_titles=['Global']+maps)
win_rate.add_trace(go.Pie(labels=labels, values=values, name="Global WR"), 1, 1)
for i,m in enumerate(maps):
    values = matches.loc[matches.map==m]['Match_Result'].value_counts().values
    if i<2:
        win_rate.add_trace(go.Pie(labels=labels, values=values, name="{} WR".format(m)), 1, i+2)
    else :
        win_rate.add_trace(go.Pie(labels=labels, values=values, name="{} WR".format(m)), 2, i-1)
win_rate.update_traces(hole=.4)#, hoverinfo="label+percent+name")
win_rate.update_layout(width=1800, height=600, title_text="Win_rate by Map")

# T/CT sides win

finished = matches.loc[matches.Match_Result != 'Unfinished']
# group_labels = maps
# hist_data = [finished.loc[finished.map==m]['CT_round_diff'] for m in maps]

# Create distplot with custom bin_size
T_RD_per_maps = px.histogram(finished, x='T_round_diff', color='map', marginal='box', 
            color_discrete_map=map_colors)
T_RD_per_maps.update_layout(width=1800, height=800, title_text='T side Round Difference Distribution by Map')
CT_RD_per_maps = px.histogram(finished, x='CT_round_diff', color='map', marginal='box', 
            color_discrete_map=map_colors)
CT_RD_per_maps.update_layout(width=1800, height=800, title_text='CT side Round Difference Distribution by Map')


## PAGE LAYOUT
nav = Navbar()

page_1 = html.Div(children=[
    html.H1(children='CSGO Stats : DYBILAL Edition.'),

    html.Div(children='''
        Les bonnes stats de la team DYBILAL. By Florian et Hélène.
    '''),

    html.Div(children='''
        Layout de l'application: 
            1e page dédiée au stats générales de l'équipe,
            2e page pour les stats indivs,
            3e page pour les stats en fonction du temps
    '''),

    dcc.Graph(
        id='Kills',
        figure=kills
    ),

    dcc.Graph(
        id='Les maps',
        figure=maps_count
    ),
    dcc.Graph(
        id='Le win rate',
        figure=win_rate
    ),
    dcc.Graph(
        id='T round diff',
        figure=T_RD_per_maps
    ),
    dcc.Graph(
        id='CT round diff',
        figure=CT_RD_per_maps
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2'),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 3', href='/apps/app3')
])

output = html.Div(id = 'output',
                children = [],
                )

header = html.H3(
    'Select the stats you want!'
)

def App1():
    layout = html.Div([
        nav,
        header,
        page_1,
        output
    ])
    return layout

# if __name__ == '__main__':
    # app.run_server(debug=True)
