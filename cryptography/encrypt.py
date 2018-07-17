import argparse
from cryptography.fernet import Fernet
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(usage='%(prog)s [options]')
# Read (optional flag (default))
ap.add_argument("-d", "--decrypt",
	help="decrypt txt file", action='store_true')
# Write (optional flag)
ap.add_argument("-e", "--encrypt",
	help="encrypt txt file", action='store_true')
# Generate key (optional flag)
ap.add_argument("-g", "--generate",
	help="generate encryption txt file", action='store_true')
# Data (either img path or text)
ap.add_argument('data', help="Path to txt file or string of data")
# Path
ap.add_argument('encryption', help="Path to/name to create of encryption txt file")
args = vars(ap.parse_args())

# Runs when -w argument is flagged
if args['encrypt']:
	# Runs when -g argument is flagged
	if args['generate']:
		key = Fernet.generate_key()
		# Save encryption key to file
		with open(args['encryption'], "wb+") as file:
			file.write(key)
			file.close()
		key = None
		
	# Load encryption key
	with open(args['encryption'], "rb") as file:
			key = file.read()
			file.close()

	cipher_suite = Fernet(key)

	try:
		# Attempt to load data file
		with open(args['data'], 'r') as file:
			data = file.read()
			file.close()

		cipher_text = cipher_suite.encrypt(data.encode())
		# Save encryped data to file
		with open("encrypted_{}".format(args['data']), 'wb') as file:
			file.write(cipher_text)
			file.close()
	# Encrypt data passed in argument
	except Exception:
		cipher_text = cipher_suite.encrypt(args['data'].encode())
		print(cipher_text)
	

# Runs when -r is flagged
elif args['decrypt'] or not args['decrypt']:
	# Load encryption key
	with open(args['encryption'], "rb") as file:
			key = file.read()
			file.close()

	cipher_suite = Fernet(key)

	try:
		# Attempt to load data file
		with open(args['data'], 'rb') as file:
			data = file.read()
			file.close()

		# Decrypt data
		plain_text = cipher_suite.decrypt(data)
		
		# Save decrypted data
		with open("decrypted_{}".format(args['data']), 'w') as file:
			file.write(plain_text.decode())
			file.close()

	# Decrypt data passed in argument
	except Exception:
		plain_text = cipher_suite.decrypt(args['data'].encode())
		print(plain_text)