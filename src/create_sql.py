import re
from pathlib import Path

import pandas as pd
from loguru import logger
from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
    func,
    text,
)


def load_data(datafile):
    logger.info(f"Loading data from {datafile}")
    df = pd.read_csv(datafile, delimiter=";")
    # Clean column names by replacing spaces and special characters with underscores
    df.columns = [re.sub(r"\W+", "_", col) for col in df.columns]
    # Handle missing data
    df = df.fillna(value=0)
    return df


def get_table_scheme(df):
    logger.info("Creating table scheme")
    columns = []
    for column in df.columns:
        if df[column].dtype == "int64":
            col_type = Integer
        elif df[column].dtype == "float64":
            col_type = Float
        else:
            col_type = String
        columns.append(Column(column, col_type))
    return columns


def main():
    datafile = Path("data/processed/cleaned.csv")
    df = load_data(datafile)

    # Create a SQLAlchemy engine to connect to an SQLite database
    engine = create_engine("sqlite:///data/db/countries.db")
    metadata = MetaData()

    columns = get_table_scheme(df)
    table = Table("countries", metadata, *columns)
    # Create the table in the database
    metadata.create_all(engine)

    # Insert data into the database
    with engine.connect() as connection:
        expected = len(df)
        logger.info(f"Found {expected} rows in the dataset. Inserting into the database.")
        for index, row in df.iterrows():
            ins = table.insert().values(**row.to_dict())
            connection.execute(ins)
        connection.commit()

        # Check the number of rows in the table using raw SQL
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM countries"))
        row_count = result.scalar()
        if row_count == expected:
            logger.success("All rows have been inserted successfully.")
        else:
            logger.warning(f"Expected {expected} rows but found {row_count} rows in the table.")

