from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres.vtidemueinilvqehlfjq:nyebVjXE3q!idgi@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

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
