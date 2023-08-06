import requests

class UserError(Exception):
	pass

class Rank:
	def __init__(self, text, logo):
		self.rank = text.split(" ")[0]
		self.points = int(text.split(" ")[1][1:]) # <--- evil string manipulation
		self.logo = logo

class User:
	def __init__(self, path, token):
		resp = requests.get("https://api.wrts.nl/api/v3/public/users/"+path, headers={"x-auth-token": token}).json()
		if "success" in resp:
			raise UserError(resp["error"])
		obj = resp["user"]
		self.first_name = obj["first_name"]
		self.id = obj["id"]
		self.path = path
		self.is_self = obj["is_own_profile"] # why would anybody need this
		self.profile_image = obj["profile_image"]
		self.profile_image_path = obj["profile_image_path"] # BRO, WHY, profile_image.image_url EXISTS!!!
		self.rank = Rank(obj["qna_rank_and_points_display"], obj["qna_rank_logo"])
		self.tutor = obj["tutor"] # <-- aka self.gay = obj["gay"]
		
