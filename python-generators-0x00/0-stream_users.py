import mysql.connector


def stream_users():
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="lusanda",
        password="Man8244251",
        database="ALX_prodev",
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
