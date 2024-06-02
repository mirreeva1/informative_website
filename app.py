from flask import Flask, render_template, jsonify, redirect, url_for
from pathlib import Path
import pandas as pd
from loguru import logger
from dash_app import serve_dash_app
from src.load_sql import load_database
app = Flask(__name__)

# Load the dataset
df = load_database()
logger.info(f"Column names: {df.columns}")

# Serve the Dash app
dash_app = serve_dash_app(app)

# Define Flask routes
@app.route('/')
def welcome_redirect():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/barchart')
def show_barchart():
    filtered_df = df[df['Total'].notnull()]
    countries = filtered_df['Country'].tolist()
    ratings = filtered_df['Total'].tolist()
    return render_template('barchart.html', countries=countries, ratings=ratings)

@app.route('/barchart_data')
def barchart_data():
    filtered_df = df[df['Total'].notnull()]
    data = {
        'labels': filtered_df['Country'].tolist(),
        'datasets': [{
            'label': 'Freedom Rating',
            'data': filtered_df['Total'].tolist(),
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)

@app.route('/home')
def index():
    top_countries = df.sort_values(by='Total', ascending=False).head(10)
    logger.info(f"top: {top_countries}")
    return render_template('index.html', top_countries=top_countries)

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/download')
def download_file():
    return redirect("https://freedomhouse.org/sites/default/files/2024-02/All_data_FIW_2013-2024.xlsx")

@app.route('/dash')
def render_dash():
    return dash_app.index()

if __name__ == '__main__':
    app.run(debug=True)
