from Database import DatabaseHandler
from LoginHandler import LoginHandler
import kivy
kivy.require("2.0.0")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

class Login(Screen):
	"""
		Startup screen that is first to presented when app launches.
	"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.__username = self.ids.username
		self.__password = self.ids.password
		self.__sign_in = self.ids.sign_in
		self.__sign_up = self.ids.sign_up
		Window.bind(on_key_down=self.validate_key_up)

	def login(self):
		"""
			Login button callback.
		"""
		LoginHandler()
		result = DatabaseHandler().log_user_in(self.__username.text, self.__password.text)
		if result is not None:
			global LOGGED_IN_USER
			LOGGED_IN_USER = self.__username.text
			#TODO transition to other page
		else:
			WrongPasswordOrUserName().open()
				

	def create_account(self):
		"""
			Create account button callback. Notice that CreateUserPopUp actually tries to make calls to create user.
		"""
		popup = CreateUserPopUp(self.__username.text, self.__password.text)
		popup.open()

	def validate_key_up(self, *args):
		"""
			onKeyUp callback. Disables buttons (login, createuser) if fields are not valid.
		"""
		if len(self.__username.text) >= 6 and len(self.__password.text) >= 6:
			self.__sign_in.disabled = False
			self.__sign_up.disabled = False
		else:
			self.__sign_in.disabled = True
			self.__sign_up.disabled = True


class CreateUserPopUp(Popup):
	"""
		Pop up for verifying user creation. Asks if user really wants ro create user.
		
		Parameters:
			username (str) Username
			password (str) Password
	"""
	def __init__(self, username, password, **kwargs):
		super().__init__(**kwargs)
		self.__username = username
		self.__password = password

	def make_user(self):
		"""
			Method makes actual shots to create user
		"""
		LoginHandler()
		x = DatabaseHandler().insert_user(self.__username, self.__password)
		if x is None:
			popup = UserExistPopUp()
			popup.open()
		self.dismiss()


class UserExistPopUp(Popup):
	"""Just to display info if user exists already"""
	pass


class WrongPasswordOrUserName(Popup):
	"""Just to display info about wrong credential"""
	pass


class MyApp(App):
	"""Kivy Entry point"""
	def build(self):
		sm = ScreenManager()
		sm.add_widget(Login(name='Login'))
		return sm

if __name__ == "__main__":
	initialize_db = DatabaseHandler()
	initialize_db.try_open_database()
	MyApp().run()



