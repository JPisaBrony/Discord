from multiprocessing import Process
import requests
import os
import sys

def get_selection(selection, selection_text):
    print selection_text
    sel = 0
    id_selected = 0
    raw_json = []
    
    for s in selection:
        raw_json.append(s)
        print str(sel) + " " + s['name']
        sel += 1

    try:
        id_selected = int(raw_input())
        if id_selected > sel - 1:
            print "Bad input"
            return 0
    except ValueError:
        print "Bad input"
        return 0
    
    return raw_json[id_selected]

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

servers_by_id = get_selection(servers, "Select Server")

chosen_server = requests.get("https://discordapp.com/api/guilds/" + str(servers_by_id['id']) + "/channels", headers=headers)
chosen_server = chosen_server.json()

channel = get_selection(chosen_server, "Select Channel")

messages = requests.get("https://discordapp.com/api/channels/" + str(channel['id']) + "/messages", headers=headers)
msg_json = messages.json()

processed_urls = 0
finished = True

if not os.path.exists("images"):
	os.makedirs("images")

def fileDownload(url, dir):
        img = requests.get(url, stream=True)
        img_name = ""
        if img.status_code == 200:
		name = url.split("/")
		img_name = name[6]
		with open(str(dir) + name[6], "wb+") as f:
			for chunk in img:
				f.write(chunk)
	print img_name

while finished:
        jobs = []
	for x in msg_json:
		for y in x["attachments"]:
			url = y["url"]
                        p = Process(target=fileDownload, args=(url, "images/"))
                        p.start()
                        jobs.append(p)
		processed_urls += 1
        
        for x in jobs:
            x.join()
        
	if processed_urls == 50:
		last_msg = msg_json[49]["id"]
		messages = requests.get("https://discordapp.com/api/channels/" + str(channel['id']) + "/messages?before=" + str(last_msg), headers=headers)
		msg_json = messages.json()
		processed_urls = 0
	else:
		finished = False
