from backend.db.db_manager import execute_query

def login_user(email, password):
    existing_user_query = f"SELECT name FROM users WHERE email = '{email}' AND password = '{password}'"
    existing_user = execute_query(existing_user_query, query_type="select")

    if existing_user:
        return existing_user[0][0]
    return None
