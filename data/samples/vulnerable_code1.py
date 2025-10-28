# vulnerable_code1.py
user_input = input()
query = "SELECT * FROM users WHERE id = " + user_input

password = 'admin123'  # Hardcoded password

query = "SELECT * FROM users WHERE name = '" + user_input + "'"  # SQL Injection
cursor.execute(query)

