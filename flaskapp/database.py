import pymysql
import os

def load_password():
    path = os.path.join(os.path.expanduser("~"), "i211s25-password.txt")
    with open(path) as fh:
        return fh.read().strip()


DB_PASSWORD = load_password()

def get_connection():
    return pymysql.connect(
        host="db.luddy.indiana.edu",
        user="i211s25_millsmat",  # Update with your actual username
        password=DB_PASSWORD,
        database="i211s25_millsmat",  # Update with your actual database name
        cursorclass=pymysql.cursors.DictCursor,
    )

# People functions
def get_people():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM people")
        people = cur.fetchall()
    conn.close()
    return people

def get_one_person(person_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM people WHERE id = %s", (person_id,))
        person = cur.fetchone()
    conn.close()
    return person


def add_person(person):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO people (name, email, height, shoe_size)
            VALUES (%s, %s, %s, %s)
        """, (person["Name"], person["Email"], person["Height"], person["Shoe Size"]))
    conn.commit()
    conn.close()

# Add this function to your database.py
def update_person(person):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE people
            SET name = %s, email = %s, height = %s, shoe_size = %s
            WHERE id = %s
        """, (person["name"], person["email"], person["height"], person["shoe_size"], person["id"]))
    conn.commit()
    conn.close()


#equipment
def get_miscellaneous():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM miscellaneous")
        miscellaneous = cur.fetchall()
    conn.close()
    return miscellaneous

def add_equipment(item):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO equipment (name, quantity, max_quantity)
            VALUES (%s, %s, %s)
        """, (item["name"], item["quantity"], item["max_quantity"]))
    conn.commit()
    conn.close()

def get_boots():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM boots")
        boots = cur.fetchall()
    conn.close()
    return boots

def get_skis():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM skis")
        skis = cur.fetchall()
    conn.close()
    return skis

def get_poles():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM poles")
        poles = cur.fetchall()
    conn.close()
    return poles

