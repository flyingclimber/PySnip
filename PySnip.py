#!/usr/bin/python

#CORE
import hashlib
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def pySet(s):
    snip = hashlib.md5(s).hexdigest()
    if not (r.get(s)):
        r.set(snip, s)
    else:
        return False

def pyGet(s):
    return r.get(s)

#FLASK
from flask import Flask
app = Flask(__name__)

@app.route("/add")
def add():
    return pySet('https://stackoverflow.com/questions/742013/how-to-code-a-url-shortener')

@app.route("/get/<id>")
def get(id):
    res = pyGet(id)
    return res if res else "Key not found"

if __name__ == "__main__":
    app.run()
