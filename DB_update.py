import sqlite3
from PIL import Image
import numpy as np
import io
from os import listdir
from os.path import isfile, join
import cv2
import face_recognition


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def add_to_list():
    mypath = "D:\python\Astrocoin\images_db"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # print(onlyfiles)
    encode_list = []
    for file in onlyfiles:
        imgElon = face_recognition.load_image_file('images/' + file)
        imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
        encodeElon = face_recognition.face_encodings(imgElon)[0]
        encode_list.append(encodeElon)

    encoded = encode_list[0]

    # print(type(encoded))

    def adapt_array(arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    sqlite3.register_adapter(np.ndarray, adapt_array)

    sqlite3.register_converter("array", convert_array)

    try:
        con = sqlite3.connect("Second.db")  # , detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        # cur.execute("""create table students_2 (
        #             id INTEGER PRIMARY KEY UNIQUE ,
        #             first_name TEXT,
        #             last_name TEXT,
        #             directory TEXT,
        #             face BLOB,
        #             arr array)""")

        empPhoto = convertToBinaryData("D:\python\Astrocoin\images\Sardor.jpg")

        cur.execute("""INSERT INTO students_2 (first_name, last_name, directory, face, arr) values (?, ?, ?, ?, ?)""",
                    ("Sardor", "Qudratov", "Data Science", empPhoto, encoded))
        print("Successfully joined")

        # cur.execute("select first_name, last_name, directory, face, arr from students_6")
        # cur.execute("select id, arr from students_6")
        # data = cur.fetchall()[0][1]
        # print(data)
        # print(type(data))

        con.commit()
        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
        print(error)
    finally:
        if con:
            con.close()
            print("the sqlite connection is closed")


add_to_list()
