import os
import pymysql

db = pymysql.connect(host="localhost", user="root", password="cyb88888", database="ai_data", charset="utf8")
cursor = db.cursor()


path = r'D:\datasets\transformerrandom\randomdata1'
walker = os.walk(path)
for path,dir_list,file_list in walker:
    for file_name in file_list:
        # print(file_name)
        namelist = file_name.split('.')
        # print(namelist[1])
        file_id = namelist[1]
        file_label = namelist[0]
        add = str(os.path.join(path,file_name))
        if 'val' in add:
            sql = 'SELECT * FROM val_data WHERE id ="' + str(file_id) + '"'
            cursor.execute(sql)
            res = cursor.fetchall()
            temp_label = res[0][2]
            if temp_label ==file_label:
                pass
            else:
                print(os.path.join(path,file_name))
        elif 'train' in add:
            sql = 'SELECT * FROM train_data WHERE id ="' + str(file_id) + '"'
            cursor.execute(sql)
            res = cursor.fetchall()
            temp_label = res[0][2]
            if temp_label ==file_label:
                pass
            else:
                print(os.path.join(path,file_name))
        else:
            pass
            # print('??')
            # print(os.path.join(path,file_name))