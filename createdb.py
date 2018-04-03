# -*- coding: utf-8 -*-
import sqlite3
import numpy as np

def add_one(user_id, con):
    sql = "update user set coins = coins+1 where uid = ?"
    cursor = con.cursor()
    cursor.execute(sql, (user_id,))
    con.commit()
    cursor.close()

def create_account(user_id, con, slogan=""):
    sql = "insert into user values(?, ?, ?)"
    cursor = con.cursor()
    cursor.execute(sql, (user_id, 0, slogan))
    con.commit()
    cursor.close()

def select_slogan(con):
    cursor = con.cursor()
    sql = "select slogan, coins from user"
    rows = [(slogan, coins) for slogan, coins in cursor.execute(sql)]
    coins = [r[1] for r in rows]
    scoins = sum(coins)
    p = [float(c)/scoins for c in coins]
    slogans = [r[0] for r in rows]
    return np.random.choice(slogans, p=p)

def get_user_slogan(con, uid):
    cursor = con.cursor()
    sql = "select slogan from user where uid=?"
    res = [slogan for slogan, in cursor.execute(sql, (uid,))]
    if not res:
        create_account(user_id=uid, con=con)
        return get_user_slogan(con, uid)
    cursor.close()
    return res[0]

def set_user_slogan(con, uid, slogan):
    cursor = con.cursor()
    sql = "update user set slogan=? where uid =?"
    cursor.execute(sql, (slogan, uid))
    con.commit()
    cursor.close()
    return slogan


def main():
    con = sqlite3.connect("bitads")
    con.text_factory = str
    cursor = con.cursor()
    create_sql = "create table user(uid text, coins integer, slogan text)"
    cursor.execute(create_sql)
    slogan = ("我的爱豆是瑞瑞，我在这里给他打call，"
              "如果你也想给自己的爱豆打call，那么就设置slogan,"
              "然后点击挖矿按钮挖矿,"
              "我们会根据你拥有的爱豆币数量让你的slogan上首页哦~")
    create_account("weiyanjie", con, slogan)
    add_one("weiyanjie", con)
    cursor.close()
    con.close()

if __name__ == '__main__':
    main()
