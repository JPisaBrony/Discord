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
messages = requests.get("https://discordapp.com/api/channels/" + str(channel) + "/messages?limit=" + str(100), headers=headers)
msg_json = messages.json()
for x in msg_json:
	for y in x["attachments"]:
		url = y["url"]
		img = requests.get(url, stream=True)
		if img.status_code == 200:
			name = url.split("/")
			with open(str("images/") + name[6], "wb+") as f:
				for chunk in img:
					f.write(chunk)
		print url
