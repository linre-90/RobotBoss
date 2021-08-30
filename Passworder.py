import hashlib
import os

class Passworder:
	"""Class does password related stuff like creating key, salt. Also provides method to compare old key with new key."""

	def create_hash(self, password):
		""" 
			Creates password key and salt
			
			Parameters:
				password (str) Plain text password

			Returns:
				dictionary (dict) {"salt": *salt used*, "key": *hash algorithm result*}
		"""
		salt = os.urandom(32)
		key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 150_000, dklen=128)
		return {"salt": salt, "key":key}

	def check_password(self, salt, user_input_password, old_key):
		"""
			Checks if password is correct. Creates new key and compares it to old_key
			
			Parameters:
				salt (str) Random byte string must be same that was used when password was hashed
				user_input_password (str) Password that user entered to login
				old_key (str) old key corresponding what was hash key when user signed up

			returns:
				Password correctnes (bool) True if passwords are same False otherwise 
		"""
		new_key = hashlib.pbkdf2_hmac("sha256", user_input_password.encode("utf-8"), salt, 150_000, dklen=128)
		if new_key == old_key:
			return True
		else:
			return False


