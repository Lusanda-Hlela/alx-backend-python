import mysql.connector

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="lusanda",
        password="Man8244251",
        database="ALX_prodev"
    )


def stream_users_in_batches(batch_size):
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
