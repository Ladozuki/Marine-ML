import pandas as pd
import plotly.express as px
# import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import joblib
import numpy as np

#Create column definitions

df = pd.read_csv('/Users/ladipo/Desktop/Charter/charter_pricepred/data/data/data_generation.csv')

columns = [{"headerName": col, "field": col} for col in df.columns]
dropdown = [{"label": col, "value": col} for col in df.columns]
rowData = df.to_dict('records')

eda_table_options = {
    'vessel_type_category_cargo': [
        {'label': 'Vessel Type', 'value': 'vessel_type'},
        {'label': 'Category', 'value': 'category'},
        {'label': 'Cargo Type', 'value': 'cargo_type'}
    ],
    'data_time_series_plot': [
        {'label': 'Data Series', 'value': 'data_series'},
        {'label': 'Time Series Plot', 'value': 'time_series_plot'}
    ],
    'capacity_dimensions_analysis': [
        {'label': 'Capacity Analysis', 'value': 'capacity_analysis'},
        {'label': 'Dimensions Analysis', 'value': 'dimensions_analysis'}
    ],
    'charter_analysis': [
        {'label': 'Charter Price Analysis', 'value': 'charter_price_analysis'},
        {'label': 'Duration Analysis', 'value': 'duration_analysis'},
        {'label': 'Fuel Cost Analysis', 'value': 'fuel_cost_analysis'}
    ],
    'lng_lp_capacity': [
        {'label': 'LNG Capacity', 'value': 'lng_capacity'},
        {'label': 'LP Capacity', 'value': 'lp_capacity'}
    ]
}


vessel_type = [
    {'label': 'LNG Carrier', 'value': 'lng_carrier'},
    {'label': 'LPG Carrier', 'value': 'lpg_carrier'},
    {'label': 'Tanker', 'value': 'tanker'},
    {'label': 'Bulk Carrier', 'value': 'bulk_carrier'},
    {'label': 'Container Ship', 'value': 'container_ship'}
]

#Function tp generate dbc.FormGroup
def generate_form_group(label, input_id, input_type = 'number', placeholder = ''):
    form_group = html.Div([
        dbc.Label(label),
        dcc.Input(id = input_id, type = input_type, placeholder = placeholder)
    ])
    return form_group

#Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(label='Charter Price Prediction', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        generate_form_group("Vessel Size", "vessel_size", placeholder="Enter vessel size"),
                        generate_form_group("Vessel Age", "vessel_age", placeholder="Enter vessel age"),
                        generate_form_group("Distance", "distance", placeholder="Enter distance"),
                        generate_form_group("Fuel Cost", "fuel_cost", placeholder="Enter fuel cost"),
                        html.Div([
                            dbc.Label("Vessel Type"),
                            dcc.Dropdown(
                                id='vessel_type',
                                options= vessel_type,
                                placeholder='Select a vessel type'
                            )
                        ])
                    ], width=6)
                ])
            ])
        ])
    ])
]),

dcc.Tab(label = 'Exploratory Data Analysis', children = [
    html.Div([
        html.H3("Exploratory Data Analysis"),
        dcc.Dropdown(
            id = 'eda-feature-dropdown',
            options = eda_table_options)
            ]),
            dag.AgGrid(
                id = 'vessel-grid',
                columnDefs = columns, 
                rowData = rowData,
                defaultColDef={"sortable": True, "filter":
                               True, "resizable": True}),
                               dbc.Container([
                                   dbc.Row([
                                       dbc.Col(html.H1("Hello, Dash with Bootstrap!"))
                                       ])
                                       ]),
])

# @app.callback(
#     Output('vessel-grid', 'rowData'),
#     [Input('vessel_type', 'value')]
# )
# def update_vessel_grid(selected_vessel_type):
#     # Logic to filter rowData based on selected_vessel_type
#     filtered_data = [{''}]
#     return filtered_data


#Run the app
if __name__ == '__main__':
    app.run_server(debug=True)