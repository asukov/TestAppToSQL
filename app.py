from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Connect to the MySQL database using environment variables
        conn = mysql.connector.connect(
            host=os.environ['AZURE_MYSQL_HOST'],
            database=os.environ['AZURE_MYSQL_NAME'],
            user=os.environ['AZURE_MYSQL_USER'],
            password=os.environ['AZURE_MYSQL_PASSWORD']
        )
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                department VARCHAR(100),
                salary DECIMAL(10, 2)
            )
        """)

        # Clear existing data and insert sample data
        cursor.execute("DELETE FROM employees")
        sample_data = [
            ("Alice", "Engineering", 185000.00),
            ("Bob", "Marketing", 165000.00),
            ("Charlie", "HR", 160000.00)
        ]
        cursor.executemany("INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)", sample_data)
        conn.commit()

        # Query the data
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        result = [
            {"id": row[0], "name": row[1], "department": row[2], "salary": float(row[3])}
            for row in rows
        ]

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
