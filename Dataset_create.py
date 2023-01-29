import os
import time
import shutil
import pymysql
import numpy as np
from tqdm import tqdm

# 生成序列集，然后就用序列号去抽取文件
# train1-Tumer1N0 1-9001
# train2-Tumer1N0 9001-18002
# train3-Tumer1N0 18002-27003
# train1-Tumer1N1 68908-77909
# train2-Tumer1N1 77909-86910
# train3-Tumer1N1 86910-95911
id_list = np.arange(1,9001)
np.random.shuffle(id_list)
id_list2 = np.arange(9001,18002)
np.random.shuffle(id_list2)
id_list3 = np.arange(18002,27003)
np.random.shuffle(id_list3)
id_list4 = np.arange(68908,77909)
np.random.shuffle(id_list4)
id_list5 = np.arange(77909,86910)
np.random.shuffle(id_list5)
id_list6 = np.arange(86910,95911)
np.random.shuffle(id_list6)

# val1-Tumer1N0 1-1301
# val2-Tumer1N0 1301-2602
# val3-Tumer1N0 2602-3903
# val1-Tumer1N1 5569-6870
# val2-Tumer1N1 6870-8171
# val3-Tumer1N1 8171-9472
val_list = np.arange(1,1301)
np.random.shuffle(val_list)
val_list2 = np.arange(1301,2602)
np.random.shuffle(val_list2)
val_list3 = np.arange(2602,3903)
np.random.shuffle(val_list3)
val_list4 = np.arange(5569,6870)
np.random.shuffle(val_list4)
val_list5 = np.arange(6870,8171)
np.random.shuffle(val_list5)
val_list6 = np.arange(8171,9472)
np.random.shuffle(val_list6)


#生成一个类 用于制作训练集
class Datasetcreator():
    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root", password="cyb88888", database="ai_data", charset="utf8")
        self.cursor = self.db.cursor()
        self.path1 = r'D:\datasets\thyroid N0vsN1\viz'

    def train_find_copy(self,seq,path):
        self.seq = seq
        self.path2 = path
        for i in tqdm(range(len(self.seq)), desc='文件复制'):
            sql1 = 'SELECT * FROM train_data WHERE id ="' + str(seq[i]) + '"'
            sql2 = 'UPDATE train_data SET times =1 WHERE id ="' + str(seq[i]) + '"'
            self.cursor.execute(sql1)
            res = self.cursor.fetchall()
            fileid = res[0][0]
            filename = res[0][1]
            filelabel = res[0][2]
            patha = os.path.join(self.path1, filename)
            newname = str(filelabel) + '.' + str(fileid) + '.jpg'
            pathb = os.path.join(self.path2, newname)
            # print(patha)
            # print(pathb)
            # time.sleep(100)
            shutil.copyfile(patha, pathb)
            self.cursor.execute(sql2)
        self.db.commit()

    def val_find_copy(self,seq,path):
        self.seq = seq
        self.path2 = path
        for i in tqdm(range(len(self.seq)), desc='文件复制'):
            sql1 = 'SELECT * FROM val_data WHERE id ="' + str(seq[i]) + '"'
            sql2 = 'UPDATE val_data SET times =1 WHERE id ="' + str(seq[i]) + '"'
            self.cursor.execute(sql1)
            res = self.cursor.fetchall()
            fileid = res[0][0]
            filename = res[0][1]
            filelabel = res[0][2]
            patha = os.path.join(self.path1, filename)
            newname = str(filelabel) + '.' + str(fileid) + '.jpg'
            pathb = os.path.join(self.path2, newname)
            # print(patha)
            # print(pathb)
            # time.sleep(100)
            shutil.copyfile(patha, pathb)
            self.cursor.execute(sql2)
        self.db.commit()

    def test_and_prid(self,path,piece=300):
        sql1 = 'SELECT id FROM  val_data WHERE times is NULL'
        self.cursor.execute(sql1)
        res1 = self.cursor.fetchall()
        temp_val_list = []
        for i in range(len(res1)):
            temp_val = res1[i][0]
            temp_val_list.append(temp_val)
        # print(temp_val_list)
        valids = np.array(temp_val_list)
        np.random.shuffle(valids)
        # print(valids)
        # print(len(valids))
        sql2 = 'SELECT id FROM  train_data WHERE times is NULL'
        self.cursor.execute(sql2)
        res2 = self.cursor.fetchall()
        temp_train_list = []
        for i in range(len(res2)):
            temp_train = res2[i][0]
            temp_train_list.append(temp_train)
        # print(temp_val_list)
        trainids = np.array(temp_train_list)
        np.random.shuffle(trainids)
        # print(trainids)
        # print(len(trainids))

        percent1 = round(len(valids)*piece/(len(valids)+len(trainids)))
        percent2 = round(len(trainids)*piece / (len(valids) + len(trainids)))
        # print(percent1)
        # print(percent2)
        val_suck_id = valids[:percent1+1]
        train_suck_id = trainids[:percent2 + 1]
        # print(val_suck_id)
        for i in val_suck_id:
            sql3 = 'SELECT * FROM val_data WHERE id ="' + str(i) + '"'
            self.cursor.execute(sql3)
            res3 = self.cursor.fetchall()
            fileid = res3[0][0]
            filename = res3[0][1]
            filelabel = res3[0][2]
            patha = os.path.join(self.path1, filename)
            newname = str(filelabel) + '.' + str(fileid) + '.jpg'
            pathb = os.path.join(path, newname)
            # print(patha)
            # print(pathb)
            # time.sleep(100)
            shutil.copyfile(patha, pathb)
            sql4 = 'UPDATE val_data SET times =1 WHERE id ="' + str(i) + '"'
            self.cursor.execute(sql4)
        for i in train_suck_id:
            sql5 = 'SELECT * FROM train_data WHERE id ="' + str(i) + '"'
            self.cursor.execute(sql5)
            res5 = self.cursor.fetchall()
            fileid = res5[0][0]
            filename = res5[0][1]
            filelabel = res5[0][2]
            patha = os.path.join(self.path1, filename)
            newname = str(filelabel) + '.' + str(fileid) + '.jpg'
            pathb = os.path.join(path, newname)
            # print(patha)
            # print(pathb)
            # time.sleep(100)
            shutil.copyfile(patha, pathb)
            sql6 = 'UPDATE train_data SET times =1 WHERE id ="' + str(i) + '"'
            self.cursor.execute(sql6)
        self.db.commit()

    def pddd(self,path):
        sql1 = 'SELECT id FROM  train_data WHERE times is NULL AND label ="'+'Tumer1N1'+'"'
        self.cursor.execute(sql1)
        res1 = self.cursor.fetchall()
        for i in tqdm(range(len(res1)), desc='文件复制'):
            sql2 = 'SELECT * FROM train_data WHERE id ="' + str(res1[i][0]) + '"'
            self.cursor.execute(sql2)
            res2 = self.cursor.fetchall()
            fileid = res2[0][0]
            filename = res2[0][1]
            filelabel = res2[0][2]
            patha = os.path.join(self.path1, filename)
            newname = str(filelabel) + '.' + str(fileid) + '.jpg'
            pathb = os.path.join(path, newname)
            # print(patha)
            # print(pathb)
            # time.sleep(100)
            shutil.copyfile(patha, pathb)
        sql3 = 'SELECT id FROM  train_data WHERE times is NULL AND label ="'+'Tumer1N0'+'" LIMIT'
        self.cursor.execute(sql3)
        res3 = self.cursor.fetchall()
        for i in tqdm(range(len(res1)), desc='文件复制'):
            sql4 = 'SELECT * FROM train_data WHERE id ="' + str(res3[i][0]) + '"'
            self.cursor.execute(sql4)
            res4 = self.cursor.fetchall()
            fileid = res4[0][0]
            filename = res4[0][1]
            filelabel = res4[0][2]
            pathc = os.path.join(self.path1, filename)
            newname = str(filelabel) + '.' + str(fileid) + '.jpg'
            pathd = os.path.join(path, newname)
            # print(patha)
            # print(pathb)
            # time.sleep(100)
            shutil.copyfile(pathc, pathd)
        self.db.commit()



def create_train():
    path = r'D:\datasets\transformerrandom\randomdata1\train\Tumer1N0'
    path2 = r'D:\datasets\transformerrandom\randomdata2\train\Tumer1N0'
    path3 = r'D:\datasets\transformerrandom\randomdata3\train\Tumer1N0'
    p = Datasetcreator()
    p.train_find_copy(id_list,path)
    p.train_find_copy(id_list2,path2)
    p.train_find_copy(id_list3,path3)
    path4 = r'D:\datasets\transformerrandom\randomdata1\train\Tumer1N1'
    path5 = r'D:\datasets\transformerrandom\randomdata2\train\Tumer1N1'
    path6 = r'D:\datasets\transformerrandom\randomdata3\train\Tumer1N1'
    p.train_find_copy(id_list4,path4)
    p.train_find_copy(id_list5,path5)
    p.train_find_copy(id_list6,path6)

def create_val():
    path = r'D:\datasets\transformerrandom\randomdata1\val\Tumer1N0'
    path2 = r'D:\datasets\transformerrandom\randomdata2\val\Tumer1N0'
    path3 = r'D:\datasets\transformerrandom\randomdata3\val\Tumer1N0'
    p = Datasetcreator()
    p.val_find_copy(val_list,path)
    p.val_find_copy(val_list2,path2)
    p.val_find_copy(val_list3,path3)
    path4 = r'D:\datasets\transformerrandom\randomdata1\val\Tumer1N1'
    path5 = r'D:\datasets\transformerrandom\randomdata2\val\Tumer1N1'
    path6 = r'D:\datasets\transformerrandom\randomdata3\val\Tumer1N1'
    p.val_find_copy(val_list4,path4)
    p.val_find_copy(val_list5,path5)
    p.val_find_copy(val_list6,path6)

def create_test():
    p = Datasetcreator()
    p.test_and_prid(r'D:\datasets\transformerrandom\randomdata1\test')
    p.test_and_prid(r'D:\datasets\transformerrandom\randomdata2\test')
    p.test_and_prid(r'D:\datasets\transformerrandom\randomdata3\test')

# path = r'D:\datasets\transformerrandom\pd3'
# p = Datasetcreator()
# p.pddd(path)