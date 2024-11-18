import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)


def execute_query(raw_query, query_type="select"):
    """
    Executes the given raw SQL query.
    - For SELECT queries: returns fetched rows.
    - For INSERT, UPDATE, DELETE: commits changes and returns nothing.
    
    Parameters:
    raw_query (str): The raw SQL query to execute.
    query_type (str): The type of query ('select', 'insert', 'update', 'delete').
    """
    try:
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(text(raw_query))
                
                if query_type == "select":
                    return result.fetchall()
                else:
                    return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
