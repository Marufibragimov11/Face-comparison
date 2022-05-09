import sqlite3


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(first_name, last_name, amount):
    try:
        con = sqlite3.connect('Second.db')
        cur = con.cursor()
        print("Connected to SQLite")
        # cur.execute("""CREATE TABLE students_3 (
        #             id INTEGER PRIMARY KEY UNIQUE ,
        #             first_name TEXT NOT NULL,
        #             last_name TEXT NOT NULL,
        #             directory TEXT NOT NULL,
        #             face BLOB NOT NULL,
        #             encode_face TEXT NOT NULL)""")
        sqlite_insert_blob_query = """INSERT INTO wallets(first_name, last_name, amount)
                                      VALUES (?, ?, ?)"""

        data_tuple = (first_name, last_name, amount)
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        print("Data inserted successfully as a BLOB into a table")
        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        print(error)
    finally:
        if con:
            con.close()
            print("the sqlite connection is closed")


insertBLOB("Gozal", "Gozalina", 750)
insertBLOB("Steve", "Johnson", 23300)
insertBLOB("Sardor", "Qudratov", 268)
