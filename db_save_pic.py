import sqlite3


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(name, photo, user_id):
    try:
        sqliteConnection = sqlite3.connect('users_db.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_blob_query = """ INSERT INTO Student
								(Mentor, image, user_id) VALUES (?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)

        data_tuple = (name, empPhoto, user_id)

        # using cursor object executing our query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
