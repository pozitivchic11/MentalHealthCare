from backend.db.db_manager import execute_query

def register_user(name, surname, email, password):
    existing_user_query = f"SELECT * FROM users WHERE email = '{email}'"
    existing_user = execute_query(existing_user_query, query_type="select")

    if existing_user:
        return 400

    save_data_query = f"INSERT INTO users (name, surname, email, password) \
                        VALUES ('{name}', '{surname}', '{email}', '{password}')"

    execute_query(save_data_query, query_type="insert")
    return 201
