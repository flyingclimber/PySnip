#!/usr/bin/python

'''
PySnip - Flask based Url Shortner
'''

#CORE
import hashlib, redis

DOMAIN = '127.0.0.1'
PORT = 5000
PROTO = 'http'

R = redis.StrictRedis(host='localhost', port=6379, db=0)

def pyset(url):
    """Given a url record it in redis"""

    snip = hashlib.md5(url).hexdigest()
    if not (R.get(snip)):
        R.set(snip, url)
        return snip
    else:
        return False

def pyget(snip):
    """Given a key return the url"""
    return R.get(snip)

def pyincr(snip):
    """Given a key increment the amount of times it's been accessed"""
    count = 'count'
    pipe = R.pipeline()
    pipe.incr(snip + ":" + count)
    pipe.execute()

#FLASK
from flask import Flask, render_template, request
from flask_wtf.csrf import CsrfProtect
APP = Flask(__name__)
CsrfProtect(APP)

@APP.route("/addUrl")
def addurl():
    """Load the web page that allows you to do a url"""
    return render_template('addUrl.html')

@APP.route("/add", methods=['POST'])
def add():
    """Add a new url to the DB"""
    if request.method == 'POST':
        url = request.form['url']
        if url:
            key = pyset(url)
            if key:
                return render_template('view.html', key=key, url=url, \
                                       domain=DOMAIN, port=PORT, proto=PROTO)
            else:
                return "Duplicate"
        else:
            return "Invalid URL"

@APP.route("/get/<snip>")
def get(snip):
    """
       Return the url for a given ID
       per http://flask.pocoo.org/docs/0.10/security/ input should be autoescaped through Jinja2
     """
    res = pyget(snip)
    if res:
        pyincr(snip)
        return res
    else:
        return "Key not found"

if __name__ == "__main__":
    APP.debug = True
    KEY_SIZE = 32
    APP.secret_key = open("/dev/urandom","rb").read(KEY_SIZE)
    APP.run()
