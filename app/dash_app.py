import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag

#Create column definitions


df = pd.read_csv('/Users/ladipo/Desktop/Charter/charter_pricepred/data/processed/data_generation.csv')

columns = [{"headerName": col, "field": col} for col in df.columns]
rowData = df.to_dict('records')

#Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    dag.AgGrid(
        id = 'vessel-grid',
        columnDefs = columns, 
        rowData = rowData)
])

#Run the app
if __name__ == '__main__':
    app.run_server(debug=True)