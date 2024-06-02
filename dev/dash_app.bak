from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load your dataset
dataset_path = 'data/raw/your_dataset.csv'
df = pd.read_csv(dataset_path, sep=';')

# Get the column index of 'Country' (assuming it's the first column)
country_column_index = 0  # Index 0 for the first column

# Initialize the Dash app
app = Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1(children='Freedom Ratings Dash App', style={'textAlign': 'center'}),
    dcc.Dropdown(options=[{'label': country, 'value': country} for country in df.iloc[:, country_column_index].unique()], value='Abkhazia', id='dropdown-country'),
    dcc.Graph(id='graph-content')
])

# Callback to update the graph based on selected country
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-country', 'value')
)
def update_graph(selected_country):
    dff = df[df.iloc[:, country_column_index] == selected_country]
    return px.line(dff, x='Edition', y='Total', title=f'Total Freedom Ratings for {selected_country}')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
