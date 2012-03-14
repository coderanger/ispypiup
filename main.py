import os
import json
import time
import requests
from flask import Flask, render_template
app = Flask(__name__)

class IsUp(object):
    TIMEOUT = 60
    CHECK_ID = 519682
    USER = os.environ['PINGDOM_USER']
    PASS = os.environ['PINGDOM_PASSWORD']
    APP = os.environ['PINGDOM_APP_KEY']

    def __init__(self):
        self.last_check = 0
        self.up = None

    def __call__(self):
        now = time.time()
        if now - self.last_check >= self.TIMEOUT:
            self.up = self._check()
            self.last_check = now
        return self.up

    def _check(self):
        try:
            r = requests.get('https://api.pingdom.com/api/2.0/checks/%s'%self.CHECK_ID, auth=(self.USER, self.PASS), headers={'App-Key': self.APP})
            data = json.loads(r.text)
            return data['check']['status'] == 'up'
        except Exception:
            return False

is_up = IsUp()

@app.route('/')
def main():
    return render_template('up.html' if is_up() else 'down.html')

if __name__ == '__main__':
    app.run()
