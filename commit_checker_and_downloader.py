import requests
import json

def get_latest_commit(URL, *args):
    # URL will be https://api.github.com/repos/shank7485/Blog_Files/branches
    URL = URL + "branches"
    try:
        if args:
            # Private Repo
            username = args[0]
            password = args[1]

            # Do a get request to the URL passed.
            response = requests.get(URL, auth=(username, password))
            data = response.json()

            # Get latest commit hash from received JSON.
            commit_id = data[0]["commit"]["sha"]
            return commit_id
        else:
            # Public Repo
            response = requests.get(URL)
            data = response.json()
            commit_id = data[0]["commit"]["sha"]
            return commit_id
    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


def hash_value_of_latest_files(latest_commit, URL, *args):
    # URL will be https://api.github.com/repos/shank7485/Blog_Files/commits/<latest_commit>
    URL = URL + "commits/" + latest_commit
    try:
        if args:
            # Private Repo
            username = args[0]
            password = args[1]
            response = requests.get(URL,
                                    auth=(username, password))
            # Get files in from JSON
            files = response.json()["files"]

            lst = []

            # Create List of hash values of the files.
            for hash in files:
                lst.append(hash["sha"])

            return lst
        else:
            # Public Repo
            response = requests.get(URL)
            files = response.json()["files"]

            lst = []

            for hash in files:
                lst.append(hash["sha"])

            return lst

    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


def download_from_URL(hash_list, URL1, *args):
    # URL will be https://api.github.com/repos/shank7485/Blog_Files/contents/
    URL1 = URL1 + "contents/"
    try:
        if args:
            # Private Repo
            username = args[0]
            password = args[1]
            response = requests.get(URL1,
                                    auth=(username, password))
            data = response.json()

            # Iterate through hash list passed.
            for hash in hash_list:
                # Also Iterate through received JSON.
                for i in data:
                    # Check if hash in passed list of hash is equal to hash present in JSON.
                    # This checks for the URL of the hash passed. Links "commits" and "Contents"
                    if i["sha"] == hash:
                        file_name = i["name"]
                        URL2 = i["download_url"]
                        print "Downloading " + file_name + " from URL: " + URL2
                        response = requests.get(URL2, stream=True)
                        with open(file_name, 'wb') as fil:
                            for content in response.iter_content(1024):
                                if content:
                                    fil.write(content)
        else:
            # Public Repo
            response = requests.get(URL1)
            data = response.json()

            for hash in hash_list:
                for i in data:
                    if i["sha"] == hash:
                        file_name = i["name"]
                        URL2 = i["download_url"]
                        print "Downloading " + file_name + " from URL: " + URL2
                        response = requests.get(URL2, stream=True)
                        with open(file_name, 'wb') as fil:
                            for content in response.iter_content(1024):
                                if content:
                                    fil.write(content)
    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


def commit_checker_and_downloader(latest_commit, URL, *args):
    """
    Checks for changes in the commit. If there are any changes, it downloads the files which
    were uploaded during the commit.
    """
    try:

        # Check If there are any arguments.

        if args:

            # Arguments passed are username and password for private repository.

            username = args[0]
            password = args[1]

            # Load the last commit hash value from the JSON. This is needed to check for any commit changes

            with open("commit_tracker.json", "r") as commit_tracker_json_r:
                data_load = json.load(commit_tracker_json_r)

            # Create new dictionary for updating JSON

            dct = {"last_commit": latest_commit}

            last_commit = data_load["last_commit"]

            print "Latest Commit: " + latest_commit
            print "Last Commit: " + last_commit

            # Check if commits are same. If same, then do nothing.
            # If there are changes, update the new hash value into the JSON and get the hash values of the
            # files which was uploaded.

            if latest_commit == last_commit:
                print "No changes found"
            else:
                print "Changes in commit found. Downloading latest blog file."
                with open("commit_tracker.json", "w") as commit_tracker_json_w:
                    print "Updated JSON"
                    json.dump(dct, commit_tracker_json_w)

                # The hash values of the uploaded files are obtained.

                hash_list = hash_value_of_latest_files(latest_commit, URL, username, password)
                download_from_URL(hash_list, URL, username, password)
            print ""
        else:

            # If there are no arguments, repository is understood to be public.

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
                hash_list = hash_value_of_latest_files(latest_commit, URL)
                download_from_URL(hash_list, URL)
            print ""
    except:
        print "ERROR in getting latest commit. Check if GitHub repo is private."


username = ""
password = ""

private_repo_URL = "https://api.github.com/repos/shank7485/Blog_Files" + "/"
public_repo_URL = "https://api.github.com/repos/shank7485/Flask-APIs" + "/"

latest_commit = get_latest_commit(public_repo_URL)
commit_checker_and_downloader(latest_commit, public_repo_URL)
