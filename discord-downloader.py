from multiprocessing import Process
import requests
import os 
import sys
import re
import uuid
import json

def get_selection(selection, selection_text):
    print(selection_text)
    sel = 0
    id_selected = 0
    raw_json = []
    
    for s in selection:
        raw_json.append(s)
        print(str(sel) + " " + s['name'])
        sel += 1

    try:
        id_selected = int(input())
        if id_selected > sel - 1:
            print("Bad input")
            exit(0)
    except ValueError:
        print("Bad input")
        exit(0)
    
    return raw_json[id_selected]

def fileDownload(url, dir, day):
    img = requests.get(url, stream=True)
    img_name = ""
    if img.status_code == 200:
        name = url.split("/")
        img_name = name[-1].split("?")
        folder_path = str(dir) + day
        folder_string = str(dir) + day + "/" + str(uuid.uuid4()) + "!" + img_name[0]
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        try:
            with open(folder_string, "wb+") as f:
                for chunk in img:
                    f.write(chunk)
        except IOError:
            ext = img.headers['content-type'].split('/')
            folder_string = str(dir) + day + "/" + str(uuid.uuid4()) + "!" + "was_to_long." + ext[1]
            with open(folder_string, "wb+") as f:
                for chunk in img:
                    f.write(chunk)
    print(img_name[0])

if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("usage " + str(sys.argv[0]) + " email password")
        exit(0)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    r = requests.post("https://discordapp.com/api/auth/login", data = json.dumps({"email":email, "password":password}) , headers = {'Content-Type': 'application/json'} )
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
    
    folder_dir = str(servers_by_id['name']) + "/" + str(channel['name']) + "/"
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
    
    while finished:
        jobs = []
        for x in msg_json:
            day = x["timestamp"]
            day = day.split("T")
            day = day[0]
            for y in x["attachments"]:
                url = y["url"]
                p = Process(target=fileDownload, args=(url, folder_dir, day))
                p.start()
                jobs.append(p)
            url_check = x['content']
            if url_check:
                if "http" in url_check:
                    url_list = re.split(r'[ \n<>]', url_check)
                    for u in url_list:
                        if "http" in u:
                            try:
                                check_if_real = requests.get(u, timeout=15)
                            except requests.exceptions.ConnectionError:
                                with open("skipped-urls.txt", "a") as file:
                                        file.write(u + "\n")
                            if check_if_real.status_code == 200:
                                if "text/html" not in check_if_real.headers['content-type']:
                                    p = Process(target=fileDownload, args=(u, folder_dir, day))
                                    p.start()
                                    jobs.append(p)
                                else:
                                    with open("skipped-urls.txt", "a") as file:
                                        file.write(u + "\n")
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
    
