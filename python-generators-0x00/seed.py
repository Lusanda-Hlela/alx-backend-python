#!/usr/bin/python3
import mysql.connector
import csv
import uuid


def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="lusanda",
            password="Man8244251",
        )
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None


def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()


def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="lusanda",
            password="Man8244251",
            database="ALX_prodev",
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """
    )
    cursor.execute("CREATE INDEX idx_user_id ON user_data(user_id)")
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]
            # Check if email already exists to prevent duplicates
            cursor.execute("SELECT email FROM user_data WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age),
                )
    connection.commit()
    cursor.close()
