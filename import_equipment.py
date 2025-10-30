import csv
from flaskapp.database import get_connection

def drop_and_create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Drop tables if they exist
    tables = ["people", "boots", "skis", "poles", "miscellaneous"]
    for table in tables:
        cur.execute(f"DROP TABLE IF EXISTS {table}")

    # Create tables
    cur.execute("""
        CREATE TABLE people (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            height DECIMAL(4,1),
            shoe_size DECIMAL(4,1)
        )
    """)
    cur.execute("""
        CREATE TABLE boots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(20),
            quantity INT,
            max_quantity INT
        )
    """)
    cur.execute("""
        CREATE TABLE skis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(20),
            quantity INT,
            max_quantity INT
        )
    """)
    cur.execute("""
        CREATE TABLE poles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(20),
            quantity INT,
            max_quantity INT
        )
    """)
    cur.execute("""
        CREATE TABLE miscellaneous (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            quantity INT,
            max_quantity INT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully.")

def import_csv(csv_filename, table_name, columns):
    conn = get_connection()
    cur = conn.cursor()
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute(
                f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['%s']*len(columns))})",
                tuple(row[col] for col in columns)
            )
    conn.commit()
    conn.close()
    print(f"✅ Imported data from {csv_filename} into {table_name}")

if __name__ == "__main__":
    drop_and_create_tables()
    import_csv("people.csv", "people", ["Name","Email","Height","shoe_size"])
    import_csv("boots.csv", "boots", ["name","quantity","max_quantity"])
    import_csv("skis.csv", "skis", ["name","quantity","max_quantity"])
    import_csv("poles.csv", "poles", ["name","quantity","max_quantity"])
    import_csv("misc.csv", "miscellaneous", ["name","quantity","max_quantity"])
    print("🎉 Database rebuilt and populated successfully!")
