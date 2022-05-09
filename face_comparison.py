import sqlite3
import io
import cv2
import numpy as np
import face_recognition
from glob import glob

lst = []
lst_bool = []


def face_recog():
    f_n = glob('db_images/*')[0]

    def adapt_array(arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)

    con = sqlite3.connect("Second.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("select id, arr from students_2")
    rows = cur.fetchall()
    # print(rows)
    for row in rows:
        data_path = row[1]
        img_id = int(row[0])
        # print(data_path, img_id)
        # db_image = face_recognition.load_image_file(data_path)
        # db_image = cv2.cvtColor(db_image, cv2.COLOR_BGR2RGB)
        test_image = face_recognition.load_image_file(f_n)
        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        # face_loc = face_recognition.face_locations(db_image)[0]
        # encoded = face_recognition.face_encodings(db_image)[0]
        # cv2.rectangle(db_image, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (20, 214, 17), 2)

        face_test = face_recognition.face_locations(test_image)[0]
        encoded_test = face_recognition.face_encodings(test_image)[0]
        cv2.rectangle(test_image, (face_test[3], face_test[0]), (face_test[1], face_test[2]), (20, 214, 17), 2)

        results = face_recognition.compare_faces([data_path], encoded_test)
        face_distance = face_recognition.face_distance([data_path], encoded_test)
        print(results, face_distance)
        cv2.putText(test_image, f'{results} {round(face_distance[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 255), 2)
        if results[0] == True:
            print("O'xshash qiyofa topildi")
            # cv2.imshow('image1', db_image)
            # cv2.imshow('image2', test_image)
            # cv2.waitKey(0)
            cur.execute(
                """SELECT id, first_name, last_name, directory FROM students_2 WHERE id = ? """, (img_id,))
            datas = cur.fetchall()
            for data in datas:
                lst.append(data)
                print(lst[0][0])
                # print(f'\n'
                #       f'Ismi: {data[0]} \n'
                #       f'Familiyasi: {data[1]} \n'
                #       f'Yo\'nalishi: {data[2]} \n')
            break
        elif results[0] == False:
            notfound = "Bizning ma'lumotlar bazamizda bunday talaba yo'q!!!"
            lst_bool.append(notfound)
            print(notfound)

    con.commit()
    cur.close()
    con.close()
