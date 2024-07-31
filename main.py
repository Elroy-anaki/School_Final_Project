import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DB.DB_CONFIG import *
from utils import *
from classes.manager import *
from classes.teacher import Teacher
from classes.student import Student


def create_user(conn: odbc.Connection, email: str, password: str) -> object:
    ROLE_CLASSES = {"student": Student, "teacher": Teacher, "manager": Manager}
    role = get_role(conn, email)
    return ROLE_CLASSES[role](conn, email)


def main():
    SERVER = connect_server()

    user_email = input("Enter Email: ")
    user_password = input("Enter Password: ")
    m = create_user(SERVER, user_email, user_password)
    print(m.analyze_the_teachers())


# if __name__ == "__main__":
#     main()
