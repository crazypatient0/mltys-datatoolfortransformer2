import os
import time
import xlwings as xw
import pymysql


# 将train 样本集，读取到数据库
def get_train():
    # 直接读excel 了
    train = r'D:\datasets\thyroid N0vsN1\train.xlsx'
    time1 = time.time()
    # 生成excel 实例 不显示 不添加表
    app=xw.App(visible=False,add_book=False)
    # 打开工作表
    wb=app.books.open(train)
    # 选定sheet
    sht=wb.sheets['sheet']
    # 获取表结构a
    table_info = sht.used_range
    nrows = table_info.last_cell.row
    ncolumns = table_info.last_cell.column
    # 读取
    dataform = sht[:nrows,:ncolumns].value
    time2 = time.time()
    delta = time2-time1
    print('读取excel完成，总耗时'+str(round(delta,4))+'秒')
    db = pymysql.connect(host="localhost", user="root", password="cyb88888", database="ai_data", charset="utf8")
    cursor = db.cursor()
    for i in dataform:
        # print(i)
        path1 = r'D:\datasets\thyroid N0vsN1\viz'
        filename = i[1]
        filepath = os.path.join(path1,filename)
        exsitence = os.path.exists(filepath)
        label = i[2]
        if exsitence:
            sql = 'INSERT INTO  train_data (filename,label)VALUES ("'+str(filename)+'","' +label+'")'
            # print(sql)
            # time.sleep(100)
            cursor.execute(sql)
        else:
            assert 0,'%s,不存在'%i[1]

    db.commit()

# 将val 样本集，读取到数据库
def get_val():
    # 直接读excel 了
    val = r'D:\datasets\thyroid N0vsN1\valid.xlsx'
    time1 = time.time()
    # 生成excel 实例 不显示 不添加表
    app = xw.App(visible=False, add_book=False)
    # 打开工作表
    wb = app.books.open(val)
    # 选定sheet
    sht = wb.sheets['sheet']
    # 获取表结构a
    table_info = sht.used_range
    nrows = table_info.last_cell.row
    ncolumns = table_info.last_cell.column
    # 读取
    dataform = sht[:nrows, :ncolumns].value
    time2 = time.time()
    delta = time2 - time1
    print('读取excel完成，总耗时' + str(round(delta, 4)) + '秒')
    db = pymysql.connect(host="localhost", user="root", password="cyb88888", database="ai_data", charset="utf8")
    cursor = db.cursor()
    for i in dataform:
        # print(i)
        path1 = r'D:\datasets\thyroid N0vsN1\viz'
        filename = i[1]
        filepath = os.path.join(path1, filename)
        exsitence = os.path.exists(filepath)
        label = i[2]
        if exsitence:
            sql = 'INSERT INTO val_data (filename,label)VALUES ("' + str(filename) + '","' + label + '")'
            # print(sql)
            # time.sleep(100)
            cursor.execute(sql)
        else:
            assert 0, '%s,不存在' % i[1]
    db.commit()

