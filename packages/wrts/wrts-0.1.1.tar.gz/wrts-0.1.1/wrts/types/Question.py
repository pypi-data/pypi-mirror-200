import json, requests

class QuestionNotFound(Exception):
	pass

class Answer:
	def __init__(self, obj, token):
		self.token = token
		self.body = obj["body"]
		self.can_edit = obj["can_edit"]
		self.can_flag = obj["can_flag"]
		self.correct = obj["correct"]
		self.id = obj["id"]
		self.is_flagged = obj["is_flagged"]
		self.is_own_answer = obj["is_own_answer"]
		self.attachments = obj["qna_attachments"]
		self.upvoted_by_self = obj["is_upvoted"]
		
def vote(self):
		result = requests.post(f"https://api.wrts.nl/api/v3/qna/answers/{self.id}/votes", headers={"x-auth-token": self.token}).text
		print(result)
		if self.upvoted_by_self:
			self.votes -= 1
			self.upvoted_by_self = False
		else:
			self.votes += 1
			self.upvoted_by_self = True
class Question:
	def __init__(self, id, token):
		def gen(answers, token):
			for answer in answers:
				yield Answer(answer, token)
		obj = requests.get(f"https://api.wrts.nl/api/v3/public/qna/questions/{id}", headers={"x-auth-token":token}).json()
		#print(obj)
		if obj["qna_question"] == None:
			raise QuestionNotFound("The question has not been found!")
		obj = obj["qna_question"]
		self.token = token
		self.body = obj["body"]
		self.can_answer = obj["can_answer"] # lets see if this is even enforced
		self.can_edit = obj["can_edit"] # i dont think this is necassery...
		self.flag = obj["can_flag"] # what does this even mean
		self.contents = obj["contents"]
		self.creation = obj["created_at"]
		self.id = id
		self.is_flagged = obj["is_flagged"] # so the questions still exist even after removal?
		self.answers = gen(obj["other_qna_answers"]+obj["tutor_qna_answers"], token) # why need another field for *tutor* answers
		self.attachments = obj["qna_attachments"] # do not forget to parse this later
		self.moderated = obj["requires_forced_moderation"] # this is public?
		self.title = obj["title"]
		self.topic = obj["topic"] # should be converted
		self.subject = obj["subject"] # this too
		self.user = obj["user"] # same with this one
	def answer(self, body, attachments=[]):
		resp = requests.post(f"https://api.wrts.nl/api/v3/public/questions/{id}/answers", json={"body": body, "qna_attachments": attachments}, headers={"x-auth-token":self.token}).json()
		return Answer(resp["id"], self.token)
