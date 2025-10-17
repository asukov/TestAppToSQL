import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(
            host=os.environ['AZURE_MYSQL_HOST'],
            database=os.environ['AZURE_MYSQL_NAME'],
            user=os.environ['AZURE_MYSQL_USER'],
            password=os.environ['AZURE_MYSQL_PASSWORD']
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        result = {}
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            result[table_name] = [list(row) for row in rows]

        cursor.close()
        conn.close()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
