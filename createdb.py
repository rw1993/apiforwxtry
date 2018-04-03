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


def main():
    con = sqlite3.connect("bitads")
    con.text_factory = str
    cursor = con.cursor()
    create_sql = "create table user(uid text, coins integer, slogan text)"
    cursor.execute(create_sql)
    create_account("weiyanjie", con, "fuck")
    add_one("weiyanjie", con)
    cursor.close()
    con.close()

if __name__ == '__main__':
    main()
