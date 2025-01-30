import psycopg2
from psycopg2 import sql


host = "localhost"
port = "5432"
user = "postgres"
password = "Datacraft"
dbname = "funfact_db"
#
# # Verbindung zur PostgreSQL-Server-Datenbank herstellen (normalerweise zur 'postgres'-Datenbank)
# connection = psycopg2.connect(
#     dbname="postgres",
#     host=host,
#     port=port,
#     user=user,
#     password=password
# )
#
# connection.autocommit = True
# cursor = connection.cursor()
#
# cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
#
#

#
# print(f"Datenbank {dbname} erfolgreich erstellt.")

connection = psycopg2.connect(host=host,
                              port=port,
                              user=user,
                              password=password,
                              dbname=dbname
)
connection.autocommit = True
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE facts (
        fact_id INT PRIMARY KEY,
        facts VARCHAR(255),
        status BOOLEAN
    );
""")

print('Tabelle "facts" erfolreich erstellt')

cursor.close()
connection.close()

