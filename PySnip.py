#!/usr/bin/python

#CORE
import hashlib
import redis

domain = '127.0.0.1'
port = 5000
proto = 'http'

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def pySet(s):
    snip = hashlib.md5(s).hexdigest()
    if not (r.get(snip)):
        r.set(snip, s)
        return snip
    else:
        return False

def pyGet(s):
    return r.get(s)

def pyIncr(key):
    count = 'count'
    pipe = r.pipeline()
    pipe.incr(key + ":" + count)
    pipe.execute()

#FLASK
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/addUrl")
def addUrl():
    return render_template('addUrl.html')

@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            key = pySet(url)
            if key:
                return render_template('view.html', key=key, url=url, domain=domain, port=port, proto=proto)
            else:
                return "Duplicate"
        else:
            return "Invalid URL"

@app.route("/get/<id>")
def get(id):
    res = pyGet(id)
    if res:
        pyIncr(id)
        return res
    else:
        return "Key not found"

if __name__ == "__main__":
    app.debug = True
    app.run()
