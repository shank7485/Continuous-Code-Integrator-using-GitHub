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


def commit_checker_and_updater(latest_commit):
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
    print ""


def file_URLs_from_commit(URL, commit_sha, *args):
    try:
        if args:
            username = args[0]
            password = args[1]
            response = requests.get(URL + commit_sha,
                                    auth=(username, password))
            files_from_latest_commit = response.json()["files"]
            for URLs in files_from_latest_commit:
                raw_URL = URLs["raw_url"]
                print raw_URL
        else:
            response = requests.get(URL + commit_sha)
            files_from_latest_commit = response.json()["files"]
            for URLs in files_from_latest_commit:
                raw_URL = URLs["raw_url"]
                print raw_URL
    except:
        print "ERROR in getting file URLs. Check if GitHub repo is private."


username = ""
password = ""

latest_commit = get_latest_commit("https://api.github.com/repos/shank7485/Blog_Files/branches", username, password)
commit_checker_and_updater(latest_commit)
file_URLs_from_commit("https://api.github.com/repos/shank7485/Blog_Files/commits/", latest_commit, username, password)
