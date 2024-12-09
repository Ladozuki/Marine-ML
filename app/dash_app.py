import pandas as pd
import os
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input

# Load Data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
data_path = os.path.join(BASE_DIR, "..", "data", "processed", "df_gen.csv")

# Verify the path and load the data
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data file not found at {data_path}")
    
df = pd.read_csv(data_path)
# Update column definitions
columns = [{"headerName": col, "field": col} for col in df.columns]
dropdown = [{"label": col, "value": col} for col in df.columns]

# Exploratory Data Analysis options
eda_table_options = {
    'vessel_type_category_cargo': [
        {'label': 'Vessel Type', 'value': 'Vessel Type'},
        {'label': 'Cargo Type', 'value': 'Cargo Type/Use Case'}
    ],
    'charter_analysis': [
        {'label': 'Charter Price Analysis', 'value': 'Charter Price ($/day)'},
        {'label': 'Duration Analysis', 'value': 'Duration (days)'},
        {'label': 'Capacity Analysis', 'value': 'Capacity/Bollard Pull'}
    ]
}

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Freight Rate Dashboard"

app.config.suppress_callback_exceptions = True

# Layout
app.layout = dbc.Container([
    html.H1("Freight Rate Dashboard", className="mb-4"),
    
    # Navigation Tabs
    dcc.Tabs([
        dcc.Tab(label="Freight Rate Prediction", children=[
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Vessel Size (tons):"),
                        dcc.Input(id="vessel_size", type="number", placeholder="Enter vessel size"),
                        dbc.Label("Distance (miles):"),
                        dcc.Input(id="distance", type="number", placeholder="Enter distance"),
                        dbc.Label("Fuel Cost ($/liter):"),
                        dcc.Input(id="fuel_cost", type="number", placeholder="Enter fuel cost"),
                        dbc.Label("Vessel Type:"),
                        dcc.Dropdown(
                            id="vessel_type",
                            options=[
                                {"label": "Tanker", "value": "Tanker"},
                                {"label": "Container Ship", "value": "Container Ship"},
                                {"label": "LNG Carrier", "value": "LNG Carrier"}
                            ],
                            placeholder="Select vessel type"
                        ),
                        dbc.Button("Predict", id="predict-btn", color="primary", className="mt-3")
                    ], width=4),
                    
                    dbc.Col([
                        html.Div(id="prediction-output", className="mt-3"),
                    ])
                ])
            ])
        ]),
        dcc.Tab(label="Trend Analysis", children=[
            html.Div([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Select Vessel Type:"),
                        dcc.Dropdown(
                            id="trend-vessel-type",
                            options=[
                                {"label": t, "value": t} for t in df["Vessel Type"].unique()
                            ],
                            placeholder="Select a vessel type"
                        )
                    ], width=4)
                ]),
                dcc.Graph(id="trend-graph", className="mt-3")
            ])
        ]),
        dcc.Tab(label="Historical Data", children=[
            html.Div([
                html.H3("Explore Historical Freight Data"),
                dcc.Dropdown(
                    id="table-vessel-type",
                    options=[
                        {"label": t, "value": t} for t in df["Vessel Type"].unique()
                    ],
                    placeholder="Filter by vessel type",
                    className="mb-3"
                ),
                html.Div(id="historical-table")
            ])
        ])
    ])
], fluid=True)


@app.callback(
    Output("prediction-output", "children"),
    Input("predict-btn", "n_clicks"),
    [
        Input("vessel_size", "value"),
        Input("distance", "value"),
        Input("fuel_cost", "value"),
        Input("vessel_type", "value")
    ]
)
def predict_freight_rate(n_clicks, size, distance, fuel_cost, vessel_type):
    if n_clicks is None:
        return "Enter parameters and click 'Predict'."
    
    # Placeholder logic for prediction
    try:
        if not (size and distance and fuel_cost and vessel_type):
            raise ValueError("All fields are required.")
        
        predicted_rate = size * 0.05 + distance * 0.1 + fuel_cost * 2  # Simplified formula
        margin = predicted_rate * 0.2  # Example margin calculation
        
        return html.Div([
            html.H4(f"Predicted Freight Rate: ${predicted_rate:.2f}"),
            html.H4(f"Estimated Margin: ${margin:.2f}")
        ])
    except Exception as e:
        return html.Div(str(e), style={"color": "red"})

@app.callback(
    Output("trend-graph", "figure"),
    Input("trend-vessel-type", "value")
)
def update_trend_graph(vessel_type):
    if not vessel_type:
        return {}
    
    filtered_df = df[df["Vessel Type"] == vessel_type]
    fig = px.line(
        filtered_df, x="Charter Date", y="Charter Price ($/day)",
        title=f"Freight Rate Trends for {vessel_type}",
        labels={"Charter Date": "Date", "Charter Price ($/day)": "Freight Rate ($)"}
    )
    return fig


@app.callback(
    Output("historical-table", "children"),
    Input("table-vessel-type", "value")
)
def update_historical_table(vessel_type):
    filtered_df = df[df["Vessel Type"] == vessel_type] if vessel_type else df
    return dbc.Table.from_dataframe(
        filtered_df[["Charter Date", "Vessel Type", "Charter Price ($/day)", "Distance (miles)"]],
        striped=True, bordered=True, hover=True
    )


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
