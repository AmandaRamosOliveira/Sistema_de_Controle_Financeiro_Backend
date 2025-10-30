import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amanda03",
        database="sistemadecontrolefinanceiro"
    )
    return conn
