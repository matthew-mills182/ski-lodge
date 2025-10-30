import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="mills",
        password="Grizzly2003!",
        database="ski_lodge",
        cursorclass=pymysql.cursors.DictCursor
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
        """, (person.get("name"), person.get("email"), person.get("height"), person.get("shoe_size")))
    conn.commit()
    conn.close()


def update_person(person):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE people
            SET name = %s, email = %s, height = %s, shoe_size = %s
            WHERE id = %s
        """, (person.get("name"), person.get("email"), person.get("height"), person.get("shoe_size"), person.get("id")))
    conn.commit()
    conn.close()


def checkin_guest(person_id, pass_type=None, boot_size=None, ski_length=None, pole_height=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE people
            SET status = 'in',
                pass_type = %s,
                boot_size = %s,
                ski_length = %s,
                pole_height = %s
            WHERE id = %s
        """, (pass_type, boot_size, ski_length, pole_height, person_id))

        if boot_size:
            cur.execute("UPDATE boots SET quantity = quantity - 1 WHERE name = %s", (boot_size,))
        if ski_length:
            cur.execute("UPDATE skis SET quantity = quantity - 1 WHERE name = %s", (ski_length,))
        if pole_height:
            cur.execute("UPDATE poles SET quantity = quantity - 1 WHERE name = %s", (pole_height,))

    conn.commit()
    conn.close()


def checkout_guest(person_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT boot_size, ski_length, pole_height
            FROM people
            WHERE id = %s
        """, (person_id,))
        person = cur.fetchone() or {}

        if person.get("boot_size"):
            cur.execute("UPDATE boots SET quantity = quantity + 1 WHERE name = %s", (person.get("boot_size"),))
        if person.get("ski_length"):
            cur.execute("UPDATE skis SET quantity = quantity + 1 WHERE name = %s", (person.get("ski_length"),))
        if person.get("pole_height"):
            cur.execute("UPDATE poles SET quantity = quantity + 1 WHERE name = %s", (person.get("pole_height"),))

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


def update_status(person_id, new_status):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE people SET status = %s WHERE id = %s", (new_status, person_id))
    conn.commit()
    conn.close()

# Equipment
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
        """, (item.get("name"), item.get("quantity"), item.get("max_quantity")))
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
