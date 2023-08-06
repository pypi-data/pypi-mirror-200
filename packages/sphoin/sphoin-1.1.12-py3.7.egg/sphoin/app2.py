"""Main module."""

__author__ = "pom11"
__copyright__ = "Copyright 2022, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.1.12"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

# from sphoin.utils import get_terminal_size

import requests
import json
import time
import sys,select
import os
import datetime as dt
from sphoin.models import Ohlcv, Study

class Slot:
	def __init__(self,**kwargs) -> None:
		self.show_banner = False
		self.base_url = "https://api.sphoin.app/api/v1"
		if "config" in kwargs:
			self.__from_file(file=kwargs["config"])
		else:
			self.__from_kwargs(kwargs)

	def __get_screenSize(self,data={}):
		if "sizeX" in data.keys():
			self.sizeX = data['sizeX']
		else:
			self.sizeX = None
		if "sizeY" in data.keys():
			self.sizeY = data['sizeY']
		else:
			self.sizeY = None

	def __from_file(self,file):

		if file != "example":
			with open(file,"r") as f:
				data = json.load(f)
		else:
			data = {
				"uid" : "111YOURUID111",
				"api-secret" : "111YOURSECRET111",
				"api-key":"111YOURAPIKEY111",
				"show" : [
					"line",
					"studies",
					"signals"
					]
				}
		self.api_key : str = data["api-key"]
		self.api_secret : str = data["api-secret"]
		self.uid : str = data["uid"]
			
		if not isinstance(data["show"],list):
			raise ValueError("show not list")
		elif not any([x in data["show"] for x in ['line','studies','signals']]):
			raise ValueError("show list expected values: line, studies, signals")
		else:
			self.loop : list = data["show"]

		self.__get_screenSize(data)
		self.__get_json()
		
	def __from_kwargs(self,kwargs):
		if "api_key" not in kwargs:
			raise ValueError("api_key")
		elif "api_secret" not in kwargs:
			raise ValueError("api_secret")
		elif "uid" not in kwargs:
			raise ValueError("uid")
		self.api_key = kwargs["api_key"]
		self.api_secret = kwargs["api_secret"]
		self.uid = kwargs["uid"]
		if 'show' is kwargs.keys():
			if not isinstance(kwargs["show"],list):
				raise ValueError("show not list")
			elif not any([x in kwargs["show"] for x in ['line','studies','signals']]):
				raise ValueError("show list expected values: line, studies, signals")
			else:
				self.loop : list = kwargs["show"]
		else:
			raise ValueError("show list missing")
		self.__get_screenSize(kwargs)
		self.__get_json()

	def __get_json(self):
		url = self.base_url+f"/data/json"
		headers = {
		'X-sphoin.app': 'LIadeCyi15FAwoRBkiu9fJsYPvWecSxb',
		'Content-Length': '0'}
		payload = json.dumps({
		  "uid": self.uid,
		  "api-key": self.api_key,
		  "api-secret": self.api_secret
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		data =  json.loads(response.text)
		if "slot_error" not in list(data):
			self.exchange : str = data["sphoin.slot"]["exchange"]
			self.market : str = data["sphoin.slot"]["market"]
			self.interval : str = data["sphoin.slot"]["interval"]
			self.max_flag : str = int(data["sphoin.slot"]["flag"].split('|')[0])
			self.min_flag : str = int(data["sphoin.slot"]["flag"].split('|')[1])
			self.ETA : int = int(data["sphoin.slot"]["ETA"])
			self.ohlcv : Ohlcv = Ohlcv(**data["sphoin.slot"]['ohlcv'])
			self.signals_sum : list = data["sphoin.slot"]['sum']
			self.ETA : int = data["sphoin.slot"]['ETA']
			self.latest_signal : int = data["sphoin.slot"]['latest_signal']
			self.colors = data["sphoin.slot"]['colors']
			if 'studies' in data["sphoin.slot"].keys():
				self.studies : list = [Study(**x) for x in data["sphoin.slot"]['studies']]
				self.nr_studies : int = int(len(data["sphoin.slot"]["studies"]))
			elif 'studies.example' in data["sphoin.slot"].keys():
				self.studies : list = [Study(**x) for x in data["sphoin.slot"]['studies.example']]
				self.nr_studies : int = int(len(data["sphoin.slot"]["studies.example"]))

		else:
			print("Error\nYou might want to check Pro Slot config from app")
			sys.exit()

