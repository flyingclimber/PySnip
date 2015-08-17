#!/usr/bin/python

#CORE
import hashlib
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def pySet(s):
    snip = hashlib.md5(s).hexdigest()
    if not (r.get(snip)):
        r.set(snip, s)
        return 'Added'
    else:
        return 'Duplicate'

def pyGet(s):
    return r.get(s)

#FLASK
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/addUrl")
def addUrl():
    return render_template('addUrl.html')

@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        if request.form['url']:
            return pySet(request.form['url'])
        else:
            return "Invalid URL"

@app.route("/get/<id>")
def get(id):
    res = pyGet(id)
    return res if res else "Key not found"

if __name__ == "__main__":
    app.debug = True
    app.run()
