#!/usr/bin/python

import hashlib
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def pySet(s):
    snip = hashlib.md5(s).hexdigest()
    if not (r.get(s)):
        r.set(snip, s)
    else:
        print "Already have it"

pySet('https://stackoverflow.com/questions/742013/how-to-code-a-url-shortener')

