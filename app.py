import os
import mysql.connector

# Connect using environment variables
conn = mysql.connector.connect(
    host=os.environ['DBHOST'],
    database=os.environ['DBNAME'],
    user=os.environ['DBUSER'],
    password=os.environ['DBPASS']
)

cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        department VARCHAR(100),
        salary DECIMAL(10, 2)
    )
""")

# Insert sample data
cursor.execute("DELETE FROM employees")  # Clear existing data
sample_data = [
    ("Alice", "Engineering", 85000.00),
    ("Bob", "Marketing", 65000.00),
    ("Charlie", "HR", 60000.00)
]
cursor.executemany("INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)", sample_data)
conn.commit()

# Query data
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

cursor.close()
conn.close()
