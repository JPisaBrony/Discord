import requests
import os
import sys

def get_selection_id(selection, selection_text):
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
    
    return raw_json[id_selected]["id"]

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

servers_by_id = get_selection_id(servers, "Select Server")

chosen_server = requests.get("https://discordapp.com/api/guilds/" + str(servers_by_id) + "/channels", headers=headers)
chosen_server = chosen_server.json()

print get_selection_id(chosen_server, "Select Channel")
