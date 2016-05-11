import requests
import json
from pprint import pprint


def get_latest_commit(URL, *args):
    try:
        if args:
            username = args[0]
            password = args[1]
            response = requests.get(URL, auth=(username, password))
            data = response.json()
            commit_id = data[0]["commit"]["sha"]
            return commit_id
        else:
            response = requests.get(URL)
            data = response.json()
            commit_id = data[0]["commit"]["sha"]
            return commit_id
    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


def commit_checker_and_downloader(latest_commit, *args):
    try:
        if args:
            username = args[0]
            password = args[1]
            with open("commit_tracker.json", "r") as commit_tracker_json_r:
                data_load = json.load(commit_tracker_json_r)

            dct = {"last_commit": latest_commit}

            last_commit = data_load["last_commit"]
            print "Latest Commit: " + latest_commit
            print "Last Commit: " + last_commit

            if latest_commit == last_commit:
                print "No changes found"
            else:
                print "Changes in commit found. Downloading latest blog file."
                with open("commit_tracker.json", "w") as commit_tracker_json_w:
                    print "Updated JSON"
                    json.dump(dct, commit_tracker_json_w)
                    hash_list = hash_value_of_latest_files(latest_commit, username, password)
                    download_from_URL(hash_list, username, password)
            print ""
        else:
            with open("commit_tracker.json", "r") as commit_tracker_json_r:
                data_load = json.load(commit_tracker_json_r)

            dct = {"last_commit": latest_commit}

            last_commit = data_load["last_commit"]
            print "Latest Commit: " + latest_commit
            print "Last Commit: " + last_commit

            if latest_commit == last_commit:
                print "No changes found"
            else:
                print "Changes in commit found. Downloading latest blog file."
                with open("commit_tracker.json", "w") as commit_tracker_json_w:
                    print "Updated JSON"
                    json.dump(dct, commit_tracker_json_w)
                    hash_list = hash_value_of_latest_files(latest_commit)
                    download_from_URL(hash_list)
            print ""

    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


def hash_value_of_latest_files(lates_commit, *args):
    try:
        if args:
            username = args[0]
            password = args[1]
            response = requests.get("https://api.github.com/repos/shank7485/Blog_Files/commits/" + latest_commit,
                                    auth=(username, password))
            files = response.json()["files"]

            lst = []

            for hash in files:
                lst.append(hash["sha"])

            return lst
        else:
            response = requests.get("https://api.github.com/repos/shank7485/Blog_Files/commits/" + latest_commit)
            files = response.json()["files"]

            lst = []

            for hash in files:
                lst.append(hash["sha"])

            return lst
    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


def download_from_URL(hash_list, *args):
    try:
        if args:
            username = args[0]
            password = args[1]
            response = requests.get("https://api.github.com/repos/shank7485/Blog_Files/contents/",
                                    auth=(username, password))
            data = response.json()

            for hash in hash_list:
                for i in data:
                    if i["sha"] == hash:
                        file_name = i["name"]
                        URL = i["download_url"]
                        print "Downloading " + file_name + " from URL: " + URL
                        response = requests.get(URL, stream=True)
                        with open(file_name, 'wb') as fil:
                            for content in response.iter_content(1024):
                                if content:
                                    fil.write(content)
        else:
            response = requests.get("https://api.github.com/repos/shank7485/Blog_Files/contents/")
            data = response.json()

            for hash in hash_list:
                for i in data:
                    if i["sha"] == hash:
                        file_name = i["name"]
                        URL = i["download_url"]
                        print "Downloading " + file_name + " from URL: " + URL
                        response = requests.get(URL, stream=True)
                        with open(file_name, 'wb') as fil:
                            for content in response.iter_content(1024):
                                if content:
                                    fil.write(content)
    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


username = "shank7485"
password = "ahs&&2556"

latest_commit = get_latest_commit("https://api.github.com/repos/shank7485/Blog_Files/branches", username, password)
commit_checker_and_downloader(latest_commit)
