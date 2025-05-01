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
        user="i211s25_millsmat",  
        password=DB_PASSWORD,
        database="i211s25_millsmat",  
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

def checkin_guest(person_id, pass_type, boot_size, ski_length, pole_height):
    conn = get_connection()
    with conn.cursor() as cur:
        # 1. Update the person’s status and rental info
        cur.execute("""
            UPDATE people
            SET status = 'in',
                pass_type = %s,
                boot_size = %s,
                ski_length = %s,
                pole_height = %s
            WHERE id = %s
        """, (pass_type, boot_size, ski_length, pole_height, person_id))

        # 2. If renting, subtract equipment from inventory
        if boot_size:
            cur.execute("UPDATE boots SET quantity = quantity - 1 WHERE size = %s", (boot_size,))
        if ski_length:
            cur.execute("UPDATE skis SET quantity = quantity - 1 WHERE length = %s", (ski_length,))
        if pole_height:
            cur.execute("UPDATE poles SET quantity = quantity - 1 WHERE height = %s", (pole_height,))

    conn.commit()
    conn.close()

def update_status(person_id, new_status):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE people SET status = %s WHERE id = %s", (new_status, person_id))
    conn.commit()
    conn.close()

def checkout_guest(person_id):
    conn = get_connection()
    with conn.cursor() as cur:
        # Get their gear info before we wipe it
        cur.execute("""
            SELECT boot_size, ski_length, pole_height
            FROM people
            WHERE id = %s
        """, (person_id,))
        person = cur.fetchone()

        # Add 1 back to each item if they had it
        if person["boot_size"]:
            cur.execute("UPDATE boots SET quantity = quantity + 1 WHERE size = %s", (person["boot_size"],))
        if person["ski_length"]:
            cur.execute("UPDATE skis SET quantity = quantity + 1 WHERE length = %s", (person["ski_length"],))
        if person["pole_height"]:
            cur.execute("UPDATE poles SET quantity = quantity + 1 WHERE height = %s", (person["pole_height"],))

        # Update person’s status and clear equipment
        cur.execute("""
            UPDATE people
            SET status = 'out',
                pass_type = NULL,
                boot_size = NULL,
                ski_length = NULL,
                pole_height = NULL
            WHERE id = %s
        """, (person_id,))

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



