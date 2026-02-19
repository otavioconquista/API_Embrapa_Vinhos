import os
import libsql

def get_connection():
    url = os.getenv("TURSO_DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")
    conn = libsql.connect(database=url, auth_token=auth_token)
    return conn
