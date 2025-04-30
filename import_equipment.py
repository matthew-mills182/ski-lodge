import csv
from flaskapp.database import get_connection

def import_csv_to_table(csv_filename, table_name):
    with open(f"{csv_filename}", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]

    conn = get_connection()
    cursor = conn.cursor()

    for row in rows:
        cursor.execute(
            f"INSERT INTO {table_name} (name, quantity, max_quantity) VALUES (%s, %s, %s)",
            (row['name'], row['quantity'], row['max_quantity'])
        )

    conn.commit()
    conn.close()
    print(f"✅ Imported data from {csv_filename} to {table_name}.")

if __name__ == "__main__":
    import_csv_to_table("misc.csv", "miscellaneous")
    import_csv_to_table("boots.csv", "boots")
    import_csv_to_table("skis.csv", "skis")
    import_csv_to_table("poles.csv", "poles")
