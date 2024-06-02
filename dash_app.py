import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

from src.load_sql import load_database

# Load your dataset
df = load_database()

# Get the column index of 'Country' (assuming it's the first column)
country_column_index = 0  # Index 0 for the first column


def create_dash_app(flask_app):
    # Initialize the Dash app
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dash/")

    # Layout of the Dash app
    dash_app.layout = html.Div(
        [
            html.H1(children="Freedom Ratings Dash App", style={"textAlign": "center"}),
            dcc.Dropdown(
                options=[
                    {"label": country, "value": country}
                    for country in df.iloc[:, country_column_index].unique()
                ],
                value="Abkhazia",
                id="dropdown-country",
            ),
            dcc.Graph(id="graph-content"),
        ]
    )

    # Callback to update the graph based on selected country
    @dash_app.callback(
        Output("graph-content", "figure"), Input("dropdown-country", "value")
    )
    def update_graph(selected_country):
        dff = df[df.iloc[:, country_column_index] == selected_country]
        return px.line(
            dff,
            x="Edition",
            y="Total",
            title=f"Total Freedom Ratings for {selected_country}",
        )

    return dash_app
