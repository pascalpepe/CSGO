import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from app1 import App1
from app2 import App2
from app3 import App3
from homepage import Homepage


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return App1()
    if pathname == '/apps/app2':
        return App2()
    if pathname == '/apps/app3':
        return App3()
    else:
        return Homepage()

## CALLBACKS DEUXIEME PAGE
df = pd.read_csv('dybilal.csv')
df.date = pd.to_datetime(pd.to_datetime(df.date).dt.date)
df['date_int'] = df.date.astype(np.int64)//1e9
all_date = sorted(df.date)
dt_all = pd.date_range(start=all_date[0],end=all_date[-1])
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df['date'])]
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]


matches= df.groupby('Match_id').first()
finished = matches.loc[matches.Match_Result != 'Unfinished']
df = df.loc[df.Match_id.isin(finished.index)]

for col in df.columns:
    if type(df[col][0]) is str:
        if '%' in df[col][0]:
            df[col] = df[col].apply(lambda x: int(x[:-1]))

players = df['Player_Name'].unique()
colors = ['#006494','#FFC500','#800580','#008500','#FF0500','#FFA500','#00F0D0']
colors = {p:c for p,c in zip(players, colors)}

maps = df.map.unique().tolist()
map_colors = ['#DE9B35', '#B31B21', '#CCBA7C', '#808080', '#415D2A']
map_colors = {m:c for m,c in zip(maps, map_colors)}
Map_names = ['All Maps', 'Inferno', 'Dust2', 'Mirage', 'Overpass', 'Cache', 'Vertigo']
mname = ['.*', 'inferno', 'dust', 'mirage', 'overpass', 'cache', 'vertigo']
Features= df.columns[3:-7]


## CALLBACKS DEUXIEME PAGE
# VIOLINPLOT
@app.callback(
    dash.dependencies.Output('crossfilter-player-scatterplot', 'figure'),
    [dash.dependencies.Input('crossfilter-map-scat', 'value'),
     dash.dependencies.Input('crossfilter-feat-scat', 'value')])
def update_graph(ma, feature):
    dg = df.loc[df.map.str.contains(ma)]

    fig = px.violin(dg, y=feature, color=df.Player_Name, box=True, points="all",
            color_discrete_map=colors,
          hover_data=['Kills', 'Deaths', 'Assists', 'Percentage of kills with a headshot',
          'Percentage of rounds with a Kill, Assist, Survived or Death Traded'])
    return fig

# WINDROSE PLOTS
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-radial1', 'figure'),
    [dash.dependencies.Input('crossfilter-column1-rad', 'value'),
     dash.dependencies.Input('crossfilter-feature-rad', 'value')])
def update_graph(ma, feature):
    dg = df.loc[df.map.str.contains(ma)].groupby('Player_Name')[feature].mean()
    dg = pd.DataFrame(dg).reset_index()

    fig = px.bar_polar(dg, r=feature, theta='Player_Name',
                   color=feature, template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-radial2', 'figure'),
    [dash.dependencies.Input('crossfilter-column2-rad', 'value'),
     dash.dependencies.Input('crossfilter-feature-rad', 'value')])
def update_graph(ma, feature):
    dg = df.loc[df.map.str.contains(ma)].groupby('Player_Name')[feature].mean()
    dg = pd.DataFrame(dg).reset_index()

    fig = px.bar_polar(dg, r=feature, theta='Player_Name',
                   color=feature, template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
    return fig

# SCATTERPLOT + BARPLOTS
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-date-slider', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-feat', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-feat', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 date_value, xfeature, yfeature):

    dff = df[df['date_int']<date_value]
    dffm = dff[dff['map'].str.contains(yaxis_column_name)]
    dffmp = dffm[dffm['Player_Name']==xaxis_column_name]

    fig = px.scatter(dffmp, x=xfeature,y=yfeature, color='map',color_discrete_map=map_colors)

    fig.update_traces(customdata=dffmp['Match_id'])
    fig.update_xaxes(title=xfeature, type='linear')
    fig.update_yaxes(title=yfeature, type='linear')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', title='{} vs {}'.format(yfeature, xfeature))

    return fig


def create_time_series(dff, title, param):
    fig = px.bar(dff, x='Player_Name', y=param)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-feat', 'value')])
def update_y_timeseries(hoverData, feature):
    mid = hoverData['points'][0]['customdata']
    dff = df[df['Match_id'] == mid]
    param = feature
    title = '<b>{}</b><br>{}'.format(param, mid)
    return create_time_series(dff, title, param)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-feat', 'value')])
def update_x_timeseries(hoverData, feature):
    mid = hoverData['points'][0]['customdata']
    dff = df[df['Match_id'] == mid]
    param = feature
    title = '<b>{}</b><br>{}'.format(param, mid)
    return create_time_series(dff, title, param)

## CALLBACKS APP 3
@app.callback(
    dash.dependencies.Output('crossfilter-time-serie', 'figure'),
    [dash.dependencies.Input('crossfilter-map-ts', 'value'),
     dash.dependencies.Input('crossfilter-feat-ts', 'value')])
def update_graph(mp, feature):
    dg = df.loc[df.map.str.contains(mp)]
    dg = dg[['Player_Name', 'date', feature]].sort_values(by='date')
    dk = dg.groupby(['Player_Name','date']).mean().reset_index(level='Player_Name')
    dh = pd.DataFrame(dk.groupby('Player_Name')[feature].rolling('30d').mean()).reset_index()
    fig1 = px.line(dh,x='date',y=feature, color='Player_Name',color_discrete_map=colors, hover_name=None)
    fig2 = px.scatter(dg,x="date", y=feature, color="Player_Name",
              title='{} vs time'.format(feature),color_discrete_map=colors
              )

    fig = go.Figure(data=fig1.data+fig2.data)
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    # fig.update_xaxes(dtick="M1",tickformat="%b\n%Y")

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
