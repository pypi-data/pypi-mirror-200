from .User import User
import requests

class NotifError(Exception):
	pass

class Notif:
	def __init__(self, obj, token):
		self.token = token
		self.id = obj["id"]
		self.created_at = obj["created_at"]
		self.icon = obj["icon"]
		self.image = obj["image"] # ???
		self.is_recent = obj["is_recent"]
		self.landing_url = obj["landing_url"]
		self.message = obj["message"]
		self.read = obj["read"]
		self.retrieved_at = obj["retrieved_at"] # aka read_at i think
		self.creator = User(obj["creator"]["public_profile_name"],token)
	def read(self):
		resp = requests.patch(f"https://api.wrts.nl/api/v3/users/notifications/{self.id}",headers={"x-auth-token": self.token}).json()
		if not resp["success"]:
			raise NotifError(resp["error"]+" or something like that") # bro how does one even mess that up
		return true
