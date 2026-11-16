from configparser import ConfigParser
from sqlalchemy import create_engine

import pandas as pd

# ====================================================================================


def load_config(filename='database.init', section='postgresql') -> dict:
    """Get the database configuration"""

    config = {}
    try:
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to postgresql
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception(f"""
                Section {section} not found in the {filename} file
            """)

    except Exception as e:
        print(f"Error [load_config()]: {e}")

    return config


def csv_to_db(csv_file: str, table_name: str) -> bool:
    """Import CSV data into a PostgreSQL table."""

    engine = None
    success = False

    try:
        if not isinstance(csv_file, str):
            raise ValueError("Invalid CSV file parameter!")

        if not isinstance(table_name, str):
            raise ValueError("Invalid table name parameter!")

        config = load_config(filename="config/database.init")

        if not config:
            raise Exception("Failed to load the configuration!")

        engine = create_engine(
            f"postgresql+psycopg2://"
            f"{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['database']}"
        )

        print(f"/> Import CSV: {csv_file}")
        print(f"/> Target table: {table_name}")

        df = pd.read_csv(csv_file)

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        print(f"==> {len(df)} rows inserted into '{table_name}'")

        success = True

    except Exception as e:
        print(f"Error [csv_to_db()]: {e}")

    finally:
        if engine is not None:
            engine.dispose()

    return success


def query_execution(query: str) -> pd.DataFrame:
    """Execute SQL query"""

    df = pd.DataFrame()
    engine = None

    try:
        if not isinstance(query, str):
            raise ValueError("Invalid parameter !")

        config = load_config(filename="config/database.init")
        if not config:
            raise Exception("Failed to load the configuration!")

        engine = create_engine(
            f"postgresql+psycopg2://"
            f"{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['database']}"
        )

        print("\n==> Query:")
        print(query)

        df = pd.read_sql_query(query, engine)

    except Exception as e:
        print(f"Error [query_execution()]: {e}")

    finally:
        if engine is not None:
            engine.dispose()

    return df
