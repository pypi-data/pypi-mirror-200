import requests

class Topic:
	def __init__(self, obj, supercat, subcat):
		self.supercat = supercat
		self.subcat = subcat

		self.combined_grade = obj["combined_grade"] # why not do this client side??
		self.country = obj["country"] # i should probably make this into some class aswell
		self.draft = obj["draft"] # what does this even mean
		self.grade_nums = obj["grade_numbers"] # convert later on
		self.id = obj["id"]
		self.relations = obj["learning_relations"] # i wonder what this means aswell
		self.question_count = obj["questions_count"] # wait this is available information???
		self.stream_ids = obj["stream_ids"] # this is very weird
		self.school_tracks = obj["school_tracks"] # this is also very weird
		self.title = obj["title"]
		self.unpublished_question_count = obj["unpublished_questions_count"] # THIS IS ALSO AVAILABLE?!?!?

class Subject:
	def __init__(self, obj, token):
		self.id = obj["id"]

		self.fallback = obj["fallback"] # i wonder what this is
		self.icon = obj["icon_url"]
		self.locale = obj["locale"] # language or somethnig
		self.logo = obj["logo"] # what is the point???
		self.mutliple_methods = obj["multiple_methods"] # wtf is this supposed to mean?
		self.name = obj["name"]
		self.quick_answer = obj["quick_answer"] # what is the point? maybe its a priority thing (french has this turned out & french is a hard language)
		self.selected_book = obj["selected_book"] # gotta do some more research on this

		self.topics = []
		response = requests.get(f"https://api.wrts.nl/api/v3/public/subjects/{self.id}/topics",headers={"x-auth-token": token}).json()["results"]
		for supercat in response:
			for subcat in supercat["subcategories"]:
				for topic in subcat["topics"]:
					self.topics.append(Topic(topic,supercat,subcat))
