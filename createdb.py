# -*- coding: utf-8 -*-
import sqlite3
import numpy as np

def get_user_coin_num(con, userid):
    sql = "select coins from user where uid=?"
    cursor = con.cursor()
    r = [num for num, in cursor.execute(sql, (userid,))][0]
    return int(r)

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

init_slogans = [
    "honey,实习任务多也不要着急哦,慢慢来~",
    "honey,真的好想到你身边~",
    "honey,给你寄了明信片，不知道能不能寄到，所以我拍了照片~",
    "honey,要好好吃饭，多吃水果，我就是这样的~",
    "honey,会平衡好写代码和生活啦，不然傻傻的了~我要为你保留一些诗意~",
    "只愿君心似我心，定不负君相思意~",
    "死生契阔，与子成说。执子之手，与子偕老。",
    "衣带渐宽终不悔，为伊消得人憔悴。",
    "两情若是久长时，又岂在朝朝暮暮。",
    "入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。",
    "曾经沧海难为水，除却巫山不是云。",
    "相思树底说相思，思郎恨郎郎不知。",
    "相思一夜情多少，地角天涯未是长。"
]

def add_test_user(con):
    username = "rw{}"
    for index, slogan in enumerate(init_slogans):
        create_account(username.format(index), con, slogan)
        add_one(username.format(index), con)

def main():
    con = sqlite3.connect("bitads")
    con.text_factory = str
    cursor = con.cursor()
    create_sql = "create table user(uid text, coins integer, slogan text)"
    cursor.execute(create_sql)
    '''
    slogan = ("我的爱豆是瑞瑞，我在这里给他打call，"
              "如果你也想给自己的爱豆打call，那么就设置slogan,"
              "然后点击挖矿按钮挖矿,"
              "我们会根据你拥有的爱豆币数量让你的slogan上首页哦~")
    create_account("weiyanjie", con, slogan)
    add_one("weiyanjie", con)
    '''
    add_test_user(con)
    cursor.close()
    con.close()

if __name__ == '__main__':
    main()
