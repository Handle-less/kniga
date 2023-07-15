import sqlite3


def connect():
    global db, sql
    db = sqlite3.connect("Data/database.db")
    sql = db.cursor()


def close():
    global db, sql
    db.close()


def add_user(user_id, username, name, city, phone):
    connect()
    sql.execute("INSERT INTO users (user_id, username, name, city, phone)"
                f"VALUES ({user_id}, '{username}', '{name}', '{city}', '{phone}')")
    db.commit()
    close()


def get_user(user_id):
    connect()
    sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    row = sql.fetchone()
    close()
    return row


def find_user(user):
    connect()
    sql.execute(f"SELECT * FROM users WHERE username = '{user}' OR name = '{user}'")
    rows = sql.fetchall()
    close()
    return rows


def add_book(book_name, count, price):
    connect()
    sql.execute("INSERT INTO books (book_name, count, price)"
                f"VALUES ('{book_name}', {count}, {price})")
    db.commit()
    close()


def set_book(id_, count):
    connect()
    sql.execute(f"UPDATE books SET count = {count} WHERE id = '{id_}'")
    db.commit()
    close()


def get_books():
    connect()
    sql.execute(f"SELECT * FROM books")
    row = sql.fetchall()
    close()
    return row


def get_book(book_name):
    connect()
    sql.execute(f"SELECT * FROM books WHERE book_name = '{book_name}'")
    row = sql.fetchone()
    close()
    return row


def add_check(user_id, book_name, count, price):
    connect()
    sql.execute("INSERT INTO checks (user_id, book, count, price)"
                f"VALUES ({user_id}, '{book_name}', {count}, {price})")
    db.commit()
    close()


def get_checks():
    connect()
    sql.execute("SELECT * FROM checks")
    row = sql.fetchall()
    close()
    return row


def get_user_checks(user_id):
    connect()
    sql.execute(f"SELECT * FROM checks WHERE user_id = {user_id}")
    row = sql.fetchall()
    close()
    return row


def get_check(user_id, book_name):
    connect()
    sql.execute("SELECT * FROM checks"
                f" WHERE user_id = {user_id}"
                f" AND book = '{book_name}'")
    row = sql.fetchone()
    close()
    return row


def delete_row_check(user_id, book_name):
    connect()
    sql.execute("DELETE FROM checks"
                f" WHERE user_id = {user_id}"
                f" AND book = '{book_name}'")
    db.commit()
    close()


def delete_check(user_id):
    connect()
    sql.execute(f"DELETE FROM checks WHERE user_id = {user_id}")
    db.commit()
    close()


def add_order(time_check, user_id, book_name, price):
    connect()
    sql.execute("INSERT INTO orders (time_check, user_id, book_name, price)"
                f"VALUES ({time_check}, {user_id}, '{book_name}', {price})")
    db.commit()
    close()


def get_count_order(book_name):
    connect()
    sql.execute(f"SELECT * FROM orders WHERE book_name = '{book_name}'")
    row = sql.fetchall()
    close()
    return row


def get_orders():
    connect()
    sql.execute("SELECT * FROM orders")
    row = sql.fetchall()
    close()
    return row


def get_user_orders(user_id):
    connect()
    sql.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
    row = sql.fetchall()
    close()
    return row


def get_book_order(book_name, count):
    connect()
    sql.execute(f"SELECT * FROM orders WHERE book_name = '{book_name}'")
    row = sql.fetchall()
    close()
    return row[:count]


def get_book_order_past(book_name, count):
    connect()
    sql.execute(f"SELECT * FROM orders WHERE book_name = '{book_name}'")
    row = sql.fetchall()
    close()
    return row[count:]


def get_order(user_id, book_name):
    connect()
    sql.execute(f"SELECT * FROM orders WHERE user_id = {user_id} AND book_name = '{book_name}'")
    row = sql.fetchall()
    close()
    return row


# def set_id(id_book):
#     connect()
#     sql.execute(f"UPDATE orders SET id = {id_book}-1 WHERE id = {id_book}")
#     db.commit()
#     close()


def delete_order(time_check, user_id):
    connect()
    sql.execute(f"DELETE FROM orders WHERE time_check = {time_check} AND user_id = {user_id}")
    db.commit()
    close()


def delete_orders():
    connect()
    sql.execute(f"DELETE FROM orders")
    db.commit()
    close()


def set_time(time_end):
    connect()
    sql.execute(f"UPDATE timeout SET time_end = {time_end}")
    db.commit()
    close()


def get_time():
    connect()
    sql.execute("SELECT * FROM timeout")
    row = sql.fetchone()
    close()
    return row


def end_once(book_name):
    connect()
    sql.execute(f"DELETE FROM books WHERE book_name = '{book_name}'")
    db.commit()
    close()
    if len(get_books()) == 0:
        set_time(0)
    connect()
    sql.execute(f"DELETE FROM orders WHERE book_name = '{book_name}'")
    db.commit()
    close()


def end_time():
    set_time(0)
    connect()
    sql.execute("DELETE FROM books")
    sql.execute("DELETE FROM orders")
    db.commit()
    close()
