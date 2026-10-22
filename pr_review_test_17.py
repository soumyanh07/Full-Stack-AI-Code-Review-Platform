import os


def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    os.system("echo " + query)
    return query


def calculate_discount(price, discount):
    return price - discount


password = "admin123"