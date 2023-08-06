from datetime import datetime
import time
import requests
import urllib.parse
import sys


class LineNotify:
    def __init__(self, token, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = None
        self.token = token
        self.line_url = "https://notify-api.line.me/api/notify"

    #####################
    ### Log Function ###
    #####################

    def log(self, input_str, level=None):
        ident = "[LINE]"
        if not self.logger:
            dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("[" + dt_str + "] " + ident + " " + input_str)
        else:
            self.logger.log(ident + " " + input_str, level)

    def timer_start(self):
        self.log(F"[LINENOTIFY] Timer Start")
        self.time = time.time()

    def timer_stop(self):
        t = time.time()
        i = t - self.time
        txt = "{:.3f}".format(i)
        self.log(F"[LINENOTIFY] Finished in {txt}s")
        return txt

    #####################
    ### Main Function ###
    #####################

    def send(self, message):
        try:
            self.log("Sending...")
            message = str(message)
            msg = urllib.parse.urlencode({"message": message})
            line_header = {'Content-Type': 'application/x-www-form-urlencoded',
                           "Authorization": "Bearer " + self.token}
            session = requests.Session()
            a = session.post(self.line_url, headers=line_header, data=msg)
            self.log(a)
            self.log("Done")
        except Exception as e:
            self.log(str(e))

    def fail(self, message):
        try:
            self.log("Sending...")
            message = str(message)
            msg = urllib.parse.urlencode({"message": message})
            line_header = {'Content-Type': 'application/x-www-form-urlencoded',
                           "Authorization": "Bearer " + self.token}
            session = requests.Session()
            a = session.post(self.line_url, headers=line_header, data=msg)
            self.log(a)
            self.log("Done")
            sys.exit(-1)
        except Exception as e:
            self.log(str(e))

