import requests
import os
import sys

if len(sys.argv) < 4:
	print "usage " + str(sys.argv[0]) + " email password channel"
	exit(0)

email = sys.argv[1]
password = sys.argv[2]
channel = sys.argv[3]

if not os.path.exists("images"):
	os.makedirs("images")

r = requests.post("https://discordapp.com/api/auth/login", data = {"email":email, "password":password})
token = r.json()["token"]
headers = {"authorization": token}
messages = requests.get("https://discordapp.com/api/channels/" + str(channel) + "/messages", headers=headers)
msg_json = messages.json()

processed_urls = 0
finished = True

while finished:
	for x in msg_json:
		for y in x["attachments"]:
			url = y["url"]
			img = requests.get(url, stream=True)
			img_name = ""
			if img.status_code == 200:
				name = url.split("/")
				img_name = name[6]
				with open(str("images/") + name[6], "wb+") as f:
					for chunk in img:
						f.write(chunk)
			print img_name
		processed_urls += 1
	if processed_urls == 50:
		last_msg = msg_json[49]["id"]
		messages = requests.get("https://discordapp.com/api/channels/" + str(channel) + "/messages?before=" + str(last_msg), headers=headers)
		msg_json = messages.json()
		processed_urls = 0
	else:
		finished = False
