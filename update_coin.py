import sqlite3
from face_comparison import lst


def databased(summa, id):
    try:
        con = sqlite3.connect('Second.db')
        cur = con.cursor()
        # print("Connected to SQLite")
        # cur.execute("""SELECT students.id, students.first_name, students.directory, students.paths, wallets.amount
        #                FROM students LEFT JOIN wallets ON students.id = wallets.wallet_id""")
        # rows = cur.fetchall()
        # print(rows[0][0])
        Steve = """UPDATE wallets
                   SET amount = ?
                   WHERE wallet_id = ?;"""
        data_tuple = (summa, id)
        cur.execute(Steve, data_tuple)
        con.commit()
        # print("Data inserted successfully as a BLOB into a table")
        cur.close()

    except sqlite3.Error as error:
        # print("Failed to insert blob data into sqlite table", error)
        print(error)
    finally:
        if con:
            con.close()
            # print("the sqlite connection is closed")






