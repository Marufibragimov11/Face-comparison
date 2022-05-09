import sqlite3
from PIL import Image

#
# def convertToBinaryData(filename):
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData
#
#
# def insertBLOB(first_name, last_name, directory, image):
#     try:
#         con = sqlite3.connect('Second.db')
#         cur = con.cursor()
#         print("Connected to SQLite")
#         # cur.execute("""CREATE TABLE students_3 (
#         #             id INTEGER PRIMARY KEY UNIQUE ,
#         #             first_name TEXT NOT NULL,
#         #             last_name TEXT NOT NULL,
#         #             directory TEXT NOT NULL,
#         #             face BLOB NOT NULL,
#         #             encode_face TEXT NOT NULL)""")
#         sqlite_insert_blob_query = """INSERT INTO students_2(first_name, last_name, directory, face)
#                                       VALUES (?, ?, ?, ?)"""
#
#         empPhoto = convertToBinaryData(image)
#         data_tuple = (first_name, last_name, directory, empPhoto)
#         cur.execute(sqlite_insert_blob_query, data_tuple)
#         # cur.execute("""SELECT face FROM students_4""")
#         # rows = cur.fetchall()
#         # for row in rows:
#         #     data = str(row)
#         #     print(data[2:-3])
#         con.commit()
#         print("Image and file inserted successfully as a BLOB into a table")
#         cur.close()
#
#     except sqlite3.Error as error:
#         print("Failed to insert blob data into sqlite table", error)
#         print(error)
#     finally:
#         if con:
#             con.close()
#             print("the sqlite connection is closed")
#
#
# insertBLOB("Maruf", "Ibragimov", "Data Science", "D:\python\Astrocoin\images\Maruf.jpg")

# def select():
#     try:
#         con = sqlite3.connect('Second.db')
#         cur = con.cursor()
#         # print("Connected to SQLite")
#         cur.execute(
#             """SELECT first_name, last_name, directory FROM students WHERE paths = "D:\python\Astrocoin\images\Asal.jpg" """)
#         datas = cur.fetchall()
#         for data in datas:
#             print(f'Ismi: {data[0]} \n'
#                   f'Familiyasi: {data[1]} \n'
#                   f'Yo\'nalishi: {data[2]}')
#         con.commit()
#         cur.close()
#     except sqlite3.Error as error:
#         print("Failed to insert blob data into sqlite table", error)
#         print(error)
#     finally:
#         if con:
#             con.close()
#             # print("the sqlite connection is closed")
#
#
# select()


try:
    con = sqlite3.connect('astrocoinapi (2).sql')
    cur = con.cursor()
    # print("Connected to SQLite")
    cur.execute("""SELECT students_2.id, students_2.first_name, students_2.directory, wallets.amount 
                   FROM students_2 LEFT JOIN wallets ON students_2.id = wallets.wallet_id""")
    rows = cur.fetchall()
    print(rows)
    con.commit()
    cur.close()

except sqlite3.Error as error:
    # print("Failed to insert blob data into sqlite table", error)
    print(error)
finally:
    if con:
        con.close()
        # print("the sqlite connection is closed")