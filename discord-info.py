import requests
import os
import sys

if len(sys.argv) < 3:
	print "usage " + str(sys.argv[0]) + " email password"
	exit(0)

email = sys.argv[1]
password = sys.argv[2]

r = requests.post("https://discordapp.com/api/auth/login", data = {"email":email, "password":password})
token = r.json()["token"]
headers = {"authorization": token}

servers = requests.get("https://discordapp.com/api/users/@me/guilds", headers=headers)
servers = servers.json()

channels = []

for s in servers:
    channels.append(requests.get("https://discordapp.com/api/guilds/" + str(s["id"]) + "/channels", headers=headers))

for x in channels:
    ch = x.json()
    for y in ch:
        print y["name"] + " " + y["id"]
