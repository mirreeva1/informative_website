from sqlalchemy import create_engine, MetaData, Table, text
import pandas as pd
from loguru import logger


def load_database():
    # Create a SQLAlchemy engine to connect to the SQLite database
    engine = create_engine("sqlite:///data/db/countries.db")
    metadata = MetaData()

    # Reflect the existing table
    metadata.reflect(bind=engine)
    countries_table = Table('countries', metadata, autoload_with=engine)

    # Log the available column names
    logger.debug(f"Available columns in the 'countries' table: {[column.name for column in countries_table.columns]}")

    # Load just the columns Country, Edition, and Total
    with engine.connect() as connection:
        query = text("SELECT Country, Edition, Total FROM countries")
        result = connection.execute(query)
        rows = result.fetchall()

    # Convert the result to a pandas DataFrame
    df_result = pd.DataFrame(rows, columns=['Country', 'Edition', 'Total'])

    # Print the DataFrame
    logger.info(f"Loaded data:\n{df_result.head()}")
    return df_result

if __name__ == "__main__":
    load_database()
