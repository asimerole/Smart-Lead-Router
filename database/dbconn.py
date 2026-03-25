import os
import sqlite3

def db_conn():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'orders.db')
    return sqlite3.connect(db_path)
    
def db_init():
    
    connection = db_conn()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,        
            name TEXT,                   
            contact_info TEXT,   
            contact_type TEXT,               
            service TEXT,                
            budget INTEGER,              
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()

def sqlExecute(sql):
    connection = db_conn()
    cursor = connection.cursor()

    cursor.execute(sql)
    
    if sql.strip().upper().startswith("SELECT"):
        result = cursor.fetchall()
        connection.close()
        return result
    else:
        connection.commit()
        connection.close()
        return None

def delete_lead(lead_id):
    connection = db_conn()
    cursor = connection.cursor()
    sql_query = f"DELETE FROM Leads WHERE id = {lead_id}"
    sqlExecute(sql_query)


