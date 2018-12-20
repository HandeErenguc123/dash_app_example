
# coding: utf-8

# In[7]:


#The first one will be a scatterplot with 
#two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


data = pd.read_csv("nama_10_gdp_1_Data.csv", sep="," )
data = data[(data.GEO != 'European Union (current composition)') & (data.GEO != 'European Union (without United Kingdom)') & 
        (data.GEO != 'European Union (15 countries)') & 
        (data.GEO != 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)') &
        (data.GEO != 'Euro area (19 countries)') & (data.GEO != 'Euro area (12 countries)')]
data.replace(':', np.nan)
data.dropna()

available_indicators = data['NA_ITEM'].unique()
available_indicatorsx=data["GEO"].unique()
data=data[data['UNIT']=="Current prices, million euro"]

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(id='xaxis-type')
        ],
        style={'width': '48%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
              ),
            dcc.RadioItems(id='yaxis-type',)
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),


    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=data['TIME'].min(),
        max=data['TIME'].max(),
        value=data['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in data['TIME'].unique()}
    ),

    
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_indicatorsx],
                value='Czechia'
            )],
        style={'width': '48%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='yaxis-column-2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
              )],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),


    dcc.Graph(id='indicator-graphic-2'),

])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    datax = data[data['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=datax[datax['NA_ITEM'] == xaxis_column_name]['Value'],
            y=datax[datax['NA_ITEM'] == yaxis_column_name]['Value'],
            text=datax[datax['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'},
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic-2', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column-2', 'value')])
def update_graph(country_name, yaxis_column_name):
    datax = data[data['GEO'] == country_name]
    
    return {
        'data': [go.Scatter(
            x=datax[datax['NA_ITEM'] == yaxis_column_name]['TIME'],
            y=datax[datax['NA_ITEM'] == yaxis_column_name]['Value'],
            text=datax[datax['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='lines'
        )],
        'layout': go.Layout(
            xaxis={
                'title': "YEAR",
                'type': 'linear'},
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=False)

