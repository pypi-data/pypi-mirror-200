from rubip.ser_cli import Server
from rubip.encryption import encryption
from json import loads,dumps
from random import choice,randint
from requests import get,post
import datetime
from re import findall

android = {"app_name":"Main","app_version":"3.1.0","platform":"Web","package":"app.rbmain.a","lang_code":"fa"}

rubix = {"app_name":"Main","app_version":"3.0.4","platform":"Web","package":"ir.rubx.bapp","lang_code":"fa"}

web = {"app_name":"Main","app_version":"4.2.0","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}


class rubip:
	def __init__(self,auth,proxies=None):
		self.auth = auth
		self.enc = encryption(auth)
		self.server = choice(Server.matnadress)
		self.file = choice(Server.filesadress)
		self.proxies = proxies
	
	def requestfile(self,inData):
		data = self.enc.encrypt(dumps(inData))
		inda = {"api_version":"5","auth":self.auth,"data_enc":data}
		while True:
			try:
				return loads(self.enc.decrypt(post(self.file,json=inda,proxies=self.proxies).json()["data_enc"]))
			except:continue
			
	def request(self,inData):
		data = self.enc.encrypt(dumps(inData))
		inda = {"api_version":"5","auth":self.auth,"data_enc":data}
		while True:
			try:
				return loads(self.enc.decrypt(post(self.file,json=inda,proxies=self.proxies).json()["data_enc"]))
			except:continue
			
	def getMessage(self,chat_id,m_id):
		inData = {"method":"getMessages","input":{"object_guid":chat_id,"sort":"FromMax","filter_type":None,"max_id":m_id},"client":android}
		while True:
			try:
				return self.request(inData).get("data").get("messages")
			except:continue
			
	def getMessagesUpdates(self,chat_id):
			time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
			inData = {"method":"getMessagesUpdates","input":{"object_guid":chat_id,"state":time_stamp},"client":android}
			while True:
				try:
					return self.request(inData)
				except:continue
	def _request(self):
		inData = {"method":"requestSendFile","input":{"file_name":"15.png","size":242388,"mime":"png"},"client":android}
		while True:
			try:
				return self.request(inData).get("data")
			except:continue
	def leave_group(self,chat_id):
		inData = {
			"method":"leaveGroup",
			"input":{
				"group_guid": chat_id
			},
			"client": android
		}
		while True:
			try:
				return self.request(inData)
			except:continue
	def getInfoByUsername(self, username):
		inData = {
		    "method":"getObjectByUsername",
		    "input":{
		        "username":username
		    },
		    "client": rubix
		}
		while True:
			try:
				return self.request(inData)
			except:continue
			
	def join_channel(self,channel_guid):
		
		inData = {"method":"joinChannelAction","input":{"action":"Join","channel_guid":channel_guid},"client": android}
		while True:
			try:
				return self.request(inData)
			except:continue
	def join_group(self,link):
		hashLink = link.split("/")[-1]
		inData = {
			"method":"joinGroup",
			"input":{
				"hash_link": hashLink
			},
			"client": android
		}
		while True:
			try:
				return self.request(inData)
			except:continue
	def leave_group(self,chat_id):
		inData = {
			"method":"leaveGroup",
			"input":{
				"group_guid": chat_id
			},
			"client": android
		}
		while True:
			try:
				return self.request(inData)
			except:continue
			
	def search_global(self,text):
		inData = {"method":"searchGlobalObjects","input":{"search_text":text},"client":rubix}
		while True:
			try:
				return self.request(inData).get("data").get("objects")
			except:continue
	def forward_message(self,From,message_ids,to):
		inData = {
			"method":"forwardMessages",
			"input":{
				"from_object_guid": From,
				"message_ids": [message_ids],
				"rnd": f"{randint(100000,999999999)}",
				"to_object_guid": to
			},
			"client":android
		}
		while True:
			try:
				return self.request(inData)
			except:continue
	def get_post_info(self,post_url):
		inData = {
			"method":"getLinkFromAppUrl",
			"input":{
				"app_url":post_url
			},
				"client":rubix
		}
		while True:
			try:
				return self.request(inData).get("data").get("link").get("open_chat_data")
			except:continue
	def get_channel_info(self,channel_guid):
		inData = {
			"method":"getChannelInfo",
			"input":{
				"channel_guid":channel_guid
			},
			"client": android
		}
		while True:
			try:
				return self.request(inData)
			except:continue
	def get_chats(self,start_id=None):
		inData = {
		    "method":"getChats",
		    "input":{
		        "start_id":start_id
		    },
		    "client": rubix
		}
		while True:
			try:
				return self.request(inData).get("data").get("chats")
			except:continue
	def get_chat_update(self):
		time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
		inData = {
			"method":"getChatsUpdates",
			"input":{
				"state":time_stamp,
			},
			"client": android
		}
		while True:
			try:
				return self.request(inData).get("data").get("chats")
			except:continue
		
	def get_message_info(self,chat_id,message_ids):
		inData = {
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": [message_ids]
			},
			"client": android
		}
		while True:
			try:
				return self.request(inData).get("data").get("messages")
			except:continue
	
	def sendMessage(self, chat_id,text,metadata=[],message_id=None):
		inData = {
			"method":"sendMessage",
			"input":{
				"object_guid":chat_id,
				"rnd":f"{randint(100000,999999999)}",
				"text":text,
				"reply_to_message_id":message_id
			},
			"client": android
		}
		if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
		while True:
			try:
				return self.request(inData)
			except:continue