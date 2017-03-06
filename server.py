#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import time

from flask import Flask,request


DEFAULT = {"dht22": [12]}
BOARDS = {1337: {"dht22":[0,2], "a":[]}}

app = Flask(__name__)

@app.route("/", defaults={'path':''}, methods=['GET','POST'])
@app.route("/<path:path>", methods=['GET','POST'])
def index(path):
	content = request.data.decode("utf8")
	print(content)
	response = 'false'
	if "register" in path:
		data = json.loads(content)
		if not "board" in data:
			app.logger.error("register called without board: "+content)
		else:
			if data["board"] in BOARDS:
				response = BOARDS[data["board"]]
			else:
				app.logger.warn("using default for board "+ str(data["board"]))
				response = DEFAULT
	elif "1606980/dht22/" in path:
		#response = {"interval": 20}
		pass
	response_data = json.dumps(response)
	app.logger.info("%s %s: %s => %s", request.method, path, content, response_data)
	return response_data

if __name__ == "__main__":
	handler = TimedRotatingFileHandler("log", when="D", interval=1, atTime=time.min)
	handler.setLevel(logging.INFO)
	handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.INFO)
	app.run(host="0.0.0.0", port=5000)
