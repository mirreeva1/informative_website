import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

from src.load_sql import load_database

# Load your dataset
df = load_database()

# Get the column index of 'Country' (assuming it's the first column)
country_column_index = 0  # Index 0 for the first column


def create_dash_app(flask_app):
    # Initialize the Dash app
    dash_app = Dash(__name__, server=flask_app, url_base_pathname="/dash/")

    # Relevant CSS for the navigation bar
    css_styles = """
    .navbar {
        position: fixed;
        top: 0;
        width: 100%;
        background-color: #333;
        padding: 50px 0;
        color: #fff;
        text-align: center;
        z-index: 1000;
        padding-bottom: 30px;
    }

    .navbar-logo {
        float: left;
        margin-left: 20px;
    }

    .navbar-links {
        float: right;
        margin-right: 20px;
    }

    .navbar-links a {
        color: #fff;
        text-decoration: none;
        margin: 0 15px;
    }
    """

    # Layout of the Dash app including the navbar and CSS stylesheet
    dash_app.layout = html.Div(
        [
            # Navbar
            html.Div(
                className="navbar",
                children=[
                    html.Div(
                        className="navbar-logo",
                        children=[
                            html.Img(
                                src="/static/bird.png",
                                alt="Logo",
                                height="50",
                            )
                        ],
                    ),
                    html.Div(
                        className="navbar-links",
                        children=[
                            html.A("Home", href="/welcome"),
                            html.A("FAQs", href="/FAQ"),
                            html.A("Data Page", href="/data"),
                            html.A("Freedom Trends", href="/dash"),
                            html.A("Data Visualisation", href="/charts")
                        ],
                    ),
                ],
            ),
            # Content
            html.Div(
                className="content",
                children=[
                    html.H1(
                        children="Freedom Ratings Around the World",
                        style={"textAlign": "center"},
                    ),
                     html.P(
                        children=[
                            "Explore the freedom rating trend of your chosen country over the past 11 years by selecting a country from the dropdown menu",
                        ]
                    ),
                    dcc.Dropdown(
                        options=[
                            {"label": country, "value": country}
                            for country in df.iloc[:, country_column_index].unique()
                        ],
                        value="Abkhazia",
                        id="dropdown-country",
                    ),
                    dcc.Graph(id="graph-content"),
                ],
            ),
        ],
        # Include CSS stylesheet
        style={"content": css_styles},
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
