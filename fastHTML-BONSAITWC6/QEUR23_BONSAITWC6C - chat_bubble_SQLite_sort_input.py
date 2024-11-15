# !pip install -U fastai
# ----
import sqlite3
import pandas as pd
import numpy as np

###########################
# CREATE DATABASE
###########################

import sqlite3

# TEST.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = './data/todos_qa.db'
conn = sqlite3.connect(dbname)

# データベースへのコネクションを閉じる。(必須)
conn.close()





###########################
# テーブルを生成する
###########################
# ---
import sqlite3

dbname = 'data/todos_qa.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute(
    'CREATE TABLE todos(id INTEGER PRIMARY KEY AUTOINCREMENT, QAtype STRING, QAcontent STRING, Goal STRING, Step STRING, Language STRING)')

# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()




##############################
######################################



# ---
# csvからtableを作成する (pandas利用)
# csv内のデータをpandasデータフレームとして読み出し、データベースへ書き込む。
import sqlite3
import pandas as pd

# ---
dbname = 'data/todos_qa.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

###########################
# 連続してデータを入力する
###########################
# ---
def input_data(filename):
    # ---
    ########################################
    # READ EXCEL FILE
    ########################################
    # -----
    # EXCELファイルを読み込む
    df_excel = pd.read_excel(f'{filename}.xlsx')
    #df_excel

    ########################################
    # CONVERTING TO CONVERSATION TYPE
    ########################################
    # ----
    acc_talk = []
    for i in range(len(df_excel)):
        # ---
        str_question = df_excel.loc[i, "QInitial"]
        str_answer = df_excel.loc[i, "AInitial"]
        str_goal = df_excel.loc[i, "Goal"]
        str_step = df_excel.loc[i, "Step"]
        str_language = df_excel.loc[i, "Language"]
        # ---
        arr_question = ["question", str_question, str_goal, str_step, str_language]
        arr_goal_AB = [f"GOAL_{str_goal}_at_step{str_step}", str_answer, str_goal, str_step, str_language]
        # ---
        acc_talk.append(arr_question)
        acc_talk.append(arr_goal_AB)
    # ---
    mx_conversation = np.array(acc_talk)
    #print(mx_conversation)

    # ---
    # QAtype STRING, QAcontent STRING, done bool)
    arr_column = ["QAtype","QAcontent","Goal","Step","Language"]
    df_conversation = pd.DataFrame(mx_conversation, columns = arr_column)
    print(f"--- {filename} ---")
    print(df_conversation[0:5])

    ###########################
    # DATABASE WRITING
    ###########################
    # dbのnameをsampleとし、読み込んだcsvファイルをsqlに書き込む
    # if_existsで、もしすでにexpenseが存在していたら、書き換えるように指示
    #df_conversation.to_sql('todos', conn, if_exists='replace')
    df_conversation.to_sql('todos', conn, if_exists='append', index=False)

# ---
arr_filename = [
    "cut_TWC_BONSAI3_step2A",
    "cut_TWC_BONSAI3_step2B",
    "cut_TWC_BONSAI3_step1B",
    "cut_TWC_BONSAI3_step1A",
    "cut_TWC_BONSAI3_step2B_jp"
]

# ---
for i in range(len(arr_filename)):
    str_filename = arr_filename[i]
    #print(str_filename)
    input_data(str_filename)

# ---
# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()





###########################
# データを消す
###########################

import sqlite3

dbname = 'data/todos_qa.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# personsというtableを作成してみる
# 大文字部はSQL文。小文字でも問題ない。
cur.execute(
    'DELETE FROM todos;')

# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()





###########################
# DATABASE WRITING
###########################

# csvからtableを作成する (pandas利用)
# csv内のデータをpandasデータフレームとして読み出し、データベースへ書き込む。
import sqlite3
import pandas as pd

dbname = 'data/todos_qa.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 作成したデータベースを1行ずつ見る
select_sql = 'SELECT * FROM todos'
for row in cur.execute(select_sql):
    print(row)

cur.close()
conn.close()







###########################
# DATABASE WRITING TO DF
###########################

# csvからtableを作成する (pandas利用)
# csv内のデータをpandasデータフレームとして読み出し、データベースへ書き込む。
import sqlite3
import pandas as pd

dbname = 'data/todos_qa.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# dbをpandasで読み出す。
df_sql = pd.read_sql('SELECT * FROM todos', conn)
#df_sql

# ---
cur.close()
conn.close()








