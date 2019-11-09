from tinydb import TinyDB, Query
from tinydb.operations import set as st

# user = Query()
# #accounts.update(st('location', {'city': 'Salinas', 'sate': 'California'}), user.userName == 'Michael')
# accounts.update(st('alarm', '1:30:PM'), user.userName == 'Michael')
# print(accounts.search((user.userName == "Michael") & (user.password == "1234")))

# db.close()

class Database:
	"""Database object is initialized with name and password
	which is used to create new accounts or check if account
	exist."""
	def __init__(self):
		self.db = TinyDB('database/db.json')
		self.accounts = self.db.table('accounts')
		self.User_query = Query()
		self.name = None
		self.password = None

	#check if you user exsist in database
	def user_exist(self):
		exist = self.accounts.search((self.User_query.username == self.name))
		if exist:
			return True
		else:
			return False
	def set_credentials(self, name, password):
		self.name = name
		self.password = password
	
	#Inserts a new user to the database
	def create_user(self):
		#Check the usernames doesn't already exist 
		if not self.user_exist():
			self.accounts.insert({'username': self.name, 'password': self.password})
			return "Account Successfully created"

		#Username already exist in database
		else:
			return f"Account with the username {self.name} already exist"

	def set_location(self, city, state, country):
		self.accounts.update(st('location', {'city': city,
		 'state': state, 'country': country}),
		  self.User_query.username == self.name)

	def get_location(self):
		user_Data = self.accounts.get((self.User_query.username == self.name))

		return user_Data['location']

	def set_alarm(self,time):
		self.accounts.update(st('alarm', time), self.User_query.username == self.name)

	def get_alarm(self):
		user_Data = self.accounts.get((self.User_query.username == self.name))

		if not user_Data['alarm']:
			return None

		else:
			return user_Data['alarm']

	def removeALL(self):
		self.db.purge_tables()

	def field_exist(self, field_name):
		fields = self.accounts.search((self.User_query.username == self.name))
		if field_name in fields[0]:
			return True
		else:
			return False

	def alarm_none(self):
		self.accounts.update(st('alarm', None),
		 self.User_query.username == self.name)

	def close_db():
		db.close()