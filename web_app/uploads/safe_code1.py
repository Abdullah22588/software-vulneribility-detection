# safe_code1.py
user_id = int(input("Enter ID: "))
query = "SELECT * FROM users WHERE id = %s" % user_id

password = input("Enter password: ")
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))

