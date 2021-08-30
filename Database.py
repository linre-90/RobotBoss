import sqlite3
from pathlib import Path
from sqlite3 import Error
from Passworder import Passworder


class DatabaseHandler:
	"""
		Class provides methods to interact with sqlite3 database.
	"""
	def __init__(self):
		# TODO Check windows compatibly
		if not Path("data").exists():
			Path("data").mkdir()

		self.__database_path = Path("data/users.db")



	def try_open_database(self):
		"""
			Tries to connect to database. If cannot connect file propably does not exists (app is never run before) creates users table. 
		"""
		connection = None
		try:
			connection = sqlite3.connect(self.__database_path)
			statement = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text NOT NULL, password text NOT NULL, salt text NOT NULL);"
			cursor = connection.cursor()
			cursor.execute(statement)
		except Error as e:
			print(e)
		finally:
			if connection:
				connection.close()


	def check_user_exists(self, username):
		"""
			Method to check if username exists in users table.

			Parameters:
				username (string) Username that will be check if exists
			
			Returns:
				(bool) True if user exists False otherwise
		"""
		connection = self.__connect()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (username,))
		rows = cursor.fetchall()
		self.__close_connection(connection)
		if len(rows) > 0:
			return True
		else:
			return False


	def insert_user(self, username, password):
		"""
			Inserts user to database. Checks that user does not already exists.
			Returns last row id if user was not found and inserting is complete.

			Parameters:
				username (str) Username
				password (str) Password still in string format
			Returns:
				last row index (int) or (None) if user exists
		"""
		if not self.check_user_exists(username):
			password_data = Passworder().create_hash(password)
			connection = self.__connect()
			statement = "INSERT INTO users (username, password, salt) VALUES (?,?,?)"
			cursor = connection.cursor()
			cursor.execute(statement, (username, password_data["key"], password_data["salt"]))
			connection.commit()
			x = cursor.lastrowid
			self.__close_connection(connection)
			return x
		return None


	def log_user_in(self, username, password):
		"""
			Methods tries to log user in. Checks first that user exists -> then fetches user row -> then collaborates with Passworder to check password

			Parameters:
				username (str) Username entered by user
				password (str) Password enetered by user
			Returns:
				username (str) if login succesfull otherwise (None)
		"""
		if self.check_user_exists(username):
			connection = self.__connect()
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM users WHERE username=?", (username,))
			rows = cursor.fetchall()
			db_user_data = rows[0]
			password_correct = Passworder().check_password(db_user_data[3], password, db_user_data[2])
			self.__close_connection(connection)
			if password_correct:
				return username
			else:
				return None

	def __connect(self):
		"""
			Private method to make connection to sqlite3.

			Returns:
				connection to sqlite3 db
		"""
		connection = None
		try:
			connection = sqlite3.connect(self.__database_path)
		except Error as e:
			print(e)
		return connection


	def __close_connection(self, connection):
		"""
			Private method to close connection to sqlite3.
		"""
		if connection:
			connection.close()
