import pandas as pd
import os
import json
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input, State
import plotly.express as px

# Load Data and Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/processed/df_gen.csv")
config_path = os.path.join(BASE_DIR, "../config/vessel_config.json")

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data file not found at {data_path}")
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file not found at {config_path}")

df = pd.read_csv(data_path)

with open(config_path, "r") as f:
    config = json.load(f)

# Create Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Freight Rate Dashboard"
app.config.suppress_callback_exceptions = True

# Layout
app.layout = dbc.Container([
    html.H1("Freight Rate Dashboard", className="mb-4"),
    dcc.Tabs([
        dcc.Tab(label="Freight Rate Prediction", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Label("Vessel Type:"),
                    dcc.Dropdown(
                        id="vessel_type",
                        options=[{"label": t, "value": t} for t in df["Vessel Type"].unique()],
                        placeholder="Select vessel type"
                    ),
                    dbc.Label("Route ID:"),
                    dcc.Dropdown(
                        id="route_id",
                        options=[{"label": route, "value": route} for route in df["Route ID"].unique()],
                        placeholder="Select route ID"
                    ),
                    dbc.Label("Fuel Cost ($/liter):"),
                    dcc.Input(id="fuel_cost", type="number", placeholder="Enter fuel cost"),
                    dbc.Button("Predict", id="predict-btn", color="primary", className="mt-3"),
                ], width=4),
                dbc.Col([
                    html.Div([
                        dbc.Label("Vessel Size (tons):"),
                        html.Div(id="vessel_size_display", className="mb-2"),
                        dbc.Label("Distance (nm):"),
                        html.Div(id="distance_display", className="mb-2"),
                    ]),
                    html.Div(id="prediction-output", className="mt-3"),
                ]),
            ]),
        ]),
        dcc.Tab(label="Trend Analysis", children=[
            dcc.Dropdown(
                id="trend-vessel-type",
                options=[{"label": t, "value": t} for t in df["Vessel Type"].unique()],
                placeholder="Select a vessel type",
            ),
            dcc.Graph(id="trend-graph"),
        ]),
        dcc.Tab(label="Historical Data", children=[
            html.H3("Explore Historical Freight Data"),
            dcc.Dropdown(
                id="table-vessel-type",
                options=[{"label": t, "value": t} for t in df["Vessel Type"].unique()],
                placeholder="Filter by vessel type",
            ),
            dcc.Dropdown(
                id="table-route-id",
                options=[{"label": route, "value": route} for route in df["Route ID"].unique()],
                placeholder="Filter by route ID",
            ),
            html.Div(id="historical-table"),
        ]),
    ]),
], fluid=True)

# Callbacks
@app.callback(
    [Output("vessel_size_display", "children"), Output("distance_display", "children")],
    [Input("vessel_type", "value"), Input("route_id", "value")],
)
def update_dynamic_fields(vessel_type, route_id):
    try:
        vessel_size = "N/A"
        distance = "N/A"

        if vessel_type in config["vessel_types"]:
            vessel_config = config["vessel_types"][vessel_type]
            vessel_size = f"{vessel_config.get('cargo_capacity_dwt', 'N/A')} tons"

        if route_id in config["routes"]:
            route_config = config["routes"][route_id]
            distance = f"{route_config.get('distance_nm', 'N/A')} nautical miles"

        return vessel_size, distance
    except Exception as e:
        return f"Error: {e}", f"Error: {e}"


@app.callback(
    Output("prediction-output", "children"),
    Input("predict-btn", "n_clicks"),
    [
        State("vessel_type", "value"),
        State("route_id", "value"),
        State("fuel_cost", "value"),
        State("vessel_size_display", "children"),
        State("distance_display", "children"),
    ],
)
def predict_freight_rate(n_clicks, vessel_type, route_id, fuel_cost, vessel_size_display, distance_display):
    if n_clicks is None:
        return "Enter parameters and click 'Predict'."

    try:
        # Validate inputs
        if not all([vessel_type, route_id, fuel_cost, vessel_size_display, distance_display]):
            return "All fields are required."

        if "N/A" in (vessel_size_display, distance_display):
            return "Error: Missing vessel size or route distance."

        # Parse data
        vessel_config = config["vessel_types"][vessel_type]
        route_config = config["routes"][route_id]

        average_speed_knots = vessel_config["average_speed_knots"]
        daily_consumption = vessel_config["daily_consumption"]
        operational_costs_daily = vessel_config["operational_costs_daily"]

        distance_nm = float(distance_display.split()[0])
        duration_days = distance_nm / (average_speed_knots * 24)

        total_fuel = daily_consumption * duration_days
        total_fuel_cost = total_fuel * fuel_cost

        port_fees = route_config["port_fees"]
        canal_fees = route_config["canal_fees"]
        total_operating_cost = operational_costs_daily * duration_days

        freight_rate = total_fuel_cost + port_fees + canal_fees + total_operating_cost
        margin = freight_rate * 0.2

        return html.Div([
            html.H4(f"Predicted Freight Rate: ${freight_rate:.2f}"),
            html.H4(f"Estimated Margin: ${margin:.2f}"),
        ])
    except Exception as e:
        return html.Div(f"Error: {e}", style={"color": "red"})


@app.callback(
    Output("trend-graph", "figure"),
    [Input("trend-vessel-type", "value")],
)
def update_trend_graph(vessel_type):
    filtered_df = df[df["Vessel Type"] == vessel_type] if vessel_type else df

    fig = px.line(
        filtered_df,
        x="Charter Date",
        y="Charter Price ($/day)",
        title=f"Freight Rate Trends for {vessel_type or 'All Vessels'}",
        labels={"Charter Date": "Date", "Charter Price ($/day)": "Freight Rate ($)"},
    )
    return fig


@app.callback(
    Output("historical-table", "children"),
    [Input("table-vessel-type", "value"), Input("table-route-id", "value")],
)
def update_historical_table(vessel_type, route_id):
    filtered_df = df
    if vessel_type:
        filtered_df = filtered_df[filtered_df["Vessel Type"] == vessel_type]
    if route_id:
        filtered_df = filtered_df[filtered_df["Route ID"] == route_id]

    return dbc.Table.from_dataframe(
        filtered_df[["Charter Date", "Vessel Type", "Route ID", "Charter Price ($/day)", "Distance (nm)", "Port Fees ($)"]],
        striped=True,
        bordered=True,
        hover=True,
    )

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
