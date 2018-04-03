from flask import Flask, request, g
import requests
import sqlite3
import hashlib
from createdb import add_one, select_slogan, get_user_slogan, set_user_slogan
import json
import redis
import redis_lock
r = redis.StrictRedis(host="localhost", port=6379, db=0)
app = Flask(__name__)


def get_latest():
    ret = r.get("latest")
    if ret is None:
        latest = {
                "code": "",
                "id": 0
                }   
        r.set("latest", json.dumps(latest))
        return get_latest()
    else:
        return json.loads(ret)

def set_latest(code, id_):
    lock = redis_lock.RedisLock(r, "latestlock")
    if lock.acquire():
        latest = {"code": code, "id": id_}
        r.set("latest", json.dumps(latest))
        lock.release()
        return False
    return False

def cache_from_redis(expire=None):
    def deractor(func):
        def _():
            if r.get(str(func)) is None:
                r.set(str(func), func())
                if expire is not None:
                    r.expire(str(func), expire)
            return r.get(str(func))
        return _
    return deractor
        

def get_db():
    if not hasattr(g, "db"):
        g.db = sqlite3.connect("bitads")
        g.db.text_factory = str
    return g.db

def valid(user_id, block_id, try_code):
    latest = get_latest()
    if int(block_id) != latest["id"]:
        return "invalid id"
    guess = "{}{}".format(latest["code"], try_code)
    guess_hash = hashlib.sha256(guess.encode()).hexdigest()
    print(guess_hash)
    if guess_hash[-1] == "0000":
        if int(block_id) != latest["id"]:
            return "invalid id"
        else:
            if set_latest(guess_hash, latest["id"]+1):
                add_one(user_id, get_db())
                return "True"
            return "others seted"
    return "wrong guess hash"

@app.route("/")
@cache_from_redis(3600)
def index():
    # return slogan respect to the coins ader have
    return select_slogan(get_db())

@app.route("/latest_code")
def latest_hash():
    # return the latest hash
    return json.dumps(get_latest())

@app.route("/get_coin", methods=["POST"])
def get_coin():
    try:
        user_id = request.form["user_id"]
        block_id = int(request.form["block_id"])
        try_code = request.form["try_code"]
        return valid(user_id, block_id, try_code)
    except:
        print("invalid form")
        return "False"

@app.route("/userlogin", methods=["POST", "GET"])
def login():
    try:
        code = request.form["code"]
    except:
        code = request.args["code"]
    appid = "wx3d718a6a8c233b95"
    appsecret = "4f7cba202fcc95f99217c7ce96798318"
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code"
    user_info = json.loads(requests.get(url.format(appid, appsecret, code)).text)
    open_id = user_info["openid"]
    return user_info["openid"]

@app.route("/get_user_slogan", methods=["GET"])
def getting_user_slogan():
    open_id = request.args["open_id"]
    return get_user_slogan(get_db(), open_id)


@app.route("/set_user_slogan", methods=["GET"])
def settting_user_slogan():
    open_id = request.args["open_id"]
    slogan = request.args["slogan"]
    return set_user_slogan(get_db(), open_id, slogan)
    

def main():
    lock = redis_lock.RedisLock(r, "latestlock")
    try:
        app.run(host="192.168.1.71", port=443, debug=True, ssl_context=("../pem", "../key"))
    except:
        app.run(debug=True)

if __name__ == '__main__':
    main()