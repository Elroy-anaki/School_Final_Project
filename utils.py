import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *


def get_all_emails(conn: odbc.Connection) -> list[str]:
    query = """ SELECT 
                    Users.email 
                FROM Users
            """
    cursor = conn.cursor()
    cursor.execute(query)
    emails_list = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return emails_list


def does_email_exist(conn: odbc.Connection, email: str) -> bool:
    emails = get_all_emails(conn)

    return email in emails


def get_password(conn: odbc.Connection, email: str) -> str:
    query = """ SELECT Users.[password]
                FROM Users
                WHERE Users.email = ?;
            """
    cursor = conn.cursor()
    cursor.execute(query, [email])
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


def is_correct_password(conn: odbc.Connection, email: str, password: str) -> bool:
    correct_password = get_password(conn, email)

    return password == correct_password


def get_id(conn: odbc.Connection, email: str) -> int:
    query = """ SELECT
                    Users.id 
                FROM Users 
                WHERE Users.email = ?
            """
    with conn.cursor() as cursor:
        cursor.execute(query, [email])
        id = cursor.fetchone()
    return id[0] if id else None


def get_role(conn: odbc.Connection, user_id: int) -> str:
    query = """ SELECT 
                    Users.role 
                FROM Users 
                WHERE Users.id = ?
            """
    cursor = conn.cursor()
    cursor.execute(query, [user_id])
    role = cursor.fetchone()
    cursor.close()
    return role[0] if role else None


def get_user_info(conn: odbc.Connection, user_id) -> str:
    info = {}

    info["id"] = user_id

    query = """ SELECT 
                    Users.first_name,
                    Users.last_name,
                    Users.city,
                    Users.phone,
                    Users.gender,
                    Users.email,
                    Users.password
                FROM Users
                WHERE Users.id = ?
                """
    with conn.cursor() as cursor:
        cursor.execute(query, [user_id])
        for row in cursor:
            info["first_name"] = row[0]
            info["last_name"] = row[1]
            info["city"] = row[2]
            info["phone"] = row[3]
            info["gender"] = row[4]
            info["email"] = row[5]
            info["password"] = row[6]

    return info
