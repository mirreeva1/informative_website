from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sqlalchemy

# Connect to your SQL database
engine = sqlalchemy.create_engine('your_database_connection_string')

# Load your dataset from SQL
query = "SELECT * FROM your_table"
df = pd.read_sql(query, engine)

# Create Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1(children='Freedom Ratings by Country', style={'textAlign': 'center'}),
    dcc.Dropdown(options=[{'label': country, 'value': country} for country in df['country'].unique()],
                 value='Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

# Define callback to update graph based on dropdown selection
@app.callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value')]
)
def update_graph(selected_country):
    filtered_df = df[df['country'] == selected_country]
    fig = px.line(filtered_df, x='year', y='total_freedom_score', title=f'Freedom Ratings for {selected_country}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
