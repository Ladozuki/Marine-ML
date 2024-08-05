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


categories = list(eda_table_options.keys())
subcategory_options = list(eda_table_options.values())


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
app.config.suppress_callback_exceptions = True  # Enable this setting


app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(label='Exploratory Data Analysis', children=[
            html.Div([
                html.H3("Exploratory Data Analysis"),
                dcc.Dropdown(
                    id='eda-category-dropdown',
                    options= [
            {'label': 'Data Time Series Plot', 'value': 'data_time_series_plot'},
            {'label': 'Vessel Type Category Cargo', 'value': 'vessel_type_category_cargo'},
            {'label': 'Charter Analysis', 'value': 'charter_analysis'},
            {'label': 'Size', 'value': 'size'},
            {'label': 'Capacity Dimensions Analysis', 'value': 'capacity_dimensions_analysis'},
            {'label': 'LNG LP Capacity', 'value': 'lng_lp_capacity'}
            ],
            placeholder="Select a category"
                ),
                html.Div(id = 'eda-subcategory-container'),
                dcc.Graph(id = 'eda-graph'),
                # dag.AgGrid(
                #     id='vessel-grid',
                #     columnDefs=columns,
                #     rowData=rowData,
                #     defaultColDef={"sortable": True, "filter": True, "resizable": True}
                # ),
            ])
        ]),
        dcc.Tab(label='Charter Price Prediction', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        generate_form_group("Vessel Size ", "vessel_size", placeholder="Enter vessel size"),
                        generate_form_group("Vessel Age ", "vessel_age", placeholder="Enter vessel age"),
                        generate_form_group("Distance (miles) ", "distance", placeholder="Enter distance"),
                        generate_form_group("Fuel Cost ($/day) ", "fuel_cost", placeholder="Enter fuel cost"),
                        html.Div([
                            dbc.Label("Vessel Type"),
                            dcc.Dropdown(
                                id='vessel_type',
                                options=vessel_type,
                                placeholder='Select a vessel type'
                            )
                        ])
                    ], width=6),
                    dbc.Button("Predict", id = "predict-button", color = 'primary')
                ])
            ])
        ])
    ])
])

@app.callback(
    Output('eda-subcategory-container', 'children'),
    Input('eda-category-dropdown', 'value')
)
def update_radioitems(selected_feature):
    if selected_feature is None:
        return html.Div("Select a feature or display options.")
    
    options = eda_table_options.get(selected_feature, [])
    return html.Div([
        dcc.RadioItems(
            id='eda-feature-radioitems',
            options=options,
            labelStyle={'display': 'block'}
        )
    ])

# Callback to update the graph based on the selected radio item
@app.callback(
    Output('eda-graph', 'figure'),
    [Input('eda-category-dropdown', 'value'),
    Input('eda-feature-radioitems', 'value')]
)
def update_graph(selected_feature, selected_option):
    if selected_feature is None or selected_option is None:
        return {}
    
    if selected_feature == 'data_time_series_plot':
        if selected_option == 'data_series':
            fig = px.line(df, x='charter_date', y='charter_price_($/day)', title='Charter Price Over Time')
        elif selected_option == 'time_series_plot':
            fig = px.line(df, x='charter_date', y='charter_price_($/day)', title='Time Series Plot')
    
    elif selected_feature == 'vessel_type_category_cargo':
        if selected_option == 'vessel_type':
            fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='Frequency of Each Vessel Type')
        elif selected_option == 'category':
            fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='Frequency of Each Category')
        elif selected_option == 'cargo_type':
            fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='Frequency of Each Cargo Type')
    
    elif selected_feature == 'charter_analysis':
        if selected_option == 'charter_price_analysis':
            fig = px.histogram(df, x='charter_price_($/day)', nbins=20, title='Histogram of Charter Prices')
        elif selected_option == 'duration_analysis':
            fig = px.histogram(df, x='charter_price_($/day)', nbins=20, title='Duration Analysis')
        elif selected_option == 'fuel_cost_analysis':
            fig = px.histogram(df, x='charter_price_($/day)', nbins=20, title='Fuel Cost Analysis')
    
    elif selected_feature == 'size':
        fig = px.bar(df['size_category'].value_counts().reset_index(), x='index', y='size_category', title='Frequency of Each Size Category')
    
    elif selected_feature == 'capacity_dimensions_analysis':
        if selected_option == 'capacity_analysis':
            fig = px.scatter(df, x='cargo_capacity_(dwt)', y='charter_price_($/day)', title='Capacity Analysis')
        elif selected_option == 'dimensions_analysis':
            fig = px.scatter(df, x='cargo_capacity_(dwt)', y='charter_price_($/day)', title='Dimensions Analysis')
    
    elif selected_feature == 'lng_lp_capacity':
        if selected_option == 'lng_capacity':
            fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='LNG Capacity')
        elif selected_option == 'lp_capacity':
            fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='LP Capacity')
    
    else:
        fig = {}

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

#Tab 1
#Callback to update radio based on selected category
# @app.callback(
#         Output('eda-subcategory-container', 'children'),
#         Input('eda-category-dropdown', 'value')
# )

# def update_radioitems(selected_feature):
#     if selected_feature is None:
#         return html.Div("Select a feature or display options.")
    
#     options = eda_table_options.get(selected_feature, [])

#     return html.Div([
#         dcc.RadioItems(
#             id = 'eda-feature-options',
#             options = options,
#             labelStyle = {'display': 'block'}
#         )
#     ])


# # Callback to update the graph based on the selected radio item
# @app.callback(
#     Output('eda-graph', 'figure'),
#     [Input('eda-category-dropdown', 'value'),
#      Input('eda-feature-options', 'value')]
# )
# def update_graph(selected_feature, selected_option):
#     if selected_feature is None or selected_option is None:
#         return {}
    
#     if selected_feature == 'data_time_series_plot':
#         if selected_option == 'data_series':
#             fig = px.line(df, x='charter_date', y='charter_price_($/day)', title='Charter Price Over Time')
#         elif selected_option == 'time_series_plot':
#             fig = px.line(df, x='charter_date', y='charter_price_($/day)', title='Time Series Plot')
    
#     elif selected_feature == 'vessel_type_category_cargo':
#         if selected_option == 'vessel_type':
#             fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='Frequency of Each Vessel Type')
#         elif selected_option == 'category':
#             fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='Frequency of Each Category')
#         elif selected_option == 'cargo_type':
#             fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='Frequency of Each Cargo Type')
    
#     elif selected_feature == 'charter_analysis':
#         if selected_option == 'charter_price_analysis':
#             fig = px.histogram(df, x='charter_price_($/day)', nbins=20, title='Histogram of Charter Prices')
#         elif selected_option == 'duration_analysis':
#             fig = px.histogram(df, x='charter_price_($/day)', nbins=20, title='Duration Analysis')
#         elif selected_option == 'fuel_cost_analysis':
#             fig = px.histogram(df, x='charter_price_($/day)', nbins=20, title='Fuel Cost Analysis')
    
#     elif selected_feature == 'size':
#         fig = px.bar(df['size_category'].value_counts().reset_index(), x='index', y='size_category', title='Frequency of Each Size Category')
    
#     elif selected_feature == 'capacity_dimensions_analysis':
#         if selected_option == 'capacity_analysis':
#             fig = px.scatter(df, x='cargo_capacity_(dwt)', y='charter_price_($/day)', title='Capacity Analysis')
#         elif selected_option == 'dimensions_analysis':
#             fig = px.scatter(df, x='cargo_capacity_(dwt)', y='charter_price_($/day)', title='Dimensions Analysis')
    
#     elif selected_feature == 'lng_lp_capacity':
#         if selected_option == 'lng_capacity':
#             fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='LNG Capacity')
#         elif selected_option == 'lp_capacity':
#             fig = px.bar(df['vessel_type'].value_counts().reset_index(), x='index', y='vessel_type', title='LP Capacity')
    
#     else:
#         fig = {}

#     return fig

# # @app.callback(
# #     Output('vessel-grid', 'rowData'),
# #     [Input('vessel_type', 'value')]
# # )
# # def update_vessel_grid(selected_vessel_type):
# #     # Logic to filter rowData based on selected_vessel_type
# #     filtered_data = [{''}]
# #     return filtered_data

# #Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

