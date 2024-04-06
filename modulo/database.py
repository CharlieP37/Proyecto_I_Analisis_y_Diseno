import psycopg2

def connect_to_database():
    return psycopg2.connect(database="disagrodb", user="postgres", password="admin")