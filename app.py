import os
import time
import json
import redis
from flask import Flask
from string import Template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    key = os.environ.get('KEY')
    return 'Hi, this docker compose example sets some services, see below. And this page has been seen {} times and has a environment variable with {}.<p>'\
           '{}'.format(count, key, getUrls())

def readSites():
    with open('sites.json') as f: 
        data = f.read()
    return json.loads(data)

def getUrls():
    sites = readSites()
    text = getUrlTraefik()
    for site in sites:
      text += getUrl(site, sites[site])
    return text

def getUrl(linkname, description):
    name = linkname[0:1].upper() + linkname[1:]
    return '<a href=\"http://{}.localhost\">{}</a> - {}<br>'.format(linkname,name, description)
 
def getUrlTraefik():
    return '<a href=\"http://localhost:8080\">{}</a> - {}<br>'.format("Traefik","Reverse proxy")

@app.route('/test')
def test():
    count = get_hit_count()
    return 'Hello World! I am still debugging and have been seen {} times.\n'.format(count)
