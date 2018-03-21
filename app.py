from github import Github
from datetime import datetime

import sys, getopt, mmap, getpass

# First create a Github instance:
# using username and password and access token
username = input("Username:")
password = getpass.getpass("GitHub Password")
accessToken = input("GitHub access token:")
print("Got", username, password, accessToken)
g = Github(username, password)
g = Github(accessToken)

# Open file for searching
f = open('github_repos.csv')
s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

# Get all the repos for the given username.
for repo in g.get_user().get_repos():
    # look to see if we already have the repo in our output file.  We do this because
    # Github API limits us to 5000 requests/hour.
    print(repo.name)
    name_as_bytes = str.encode(repo.name)
    if s.find(name_as_bytes) != -1:
        message = "We already processed " + repo.name
        print(message)
    else:
        fh = open("github_repos.csv", "a")
        count = 0
        since = datetime(2001, 1, 1)
        first_contributor = ""

        created = repo.created_at.strftime('%m/%d/%Y')
        updated = repo.updated_at.strftime('%m/%d/%Y')
        commits = repo.get_commits(since=since)
        reponame = repo.name
        # Go Get the Commits for the Repo.
        try:
            if commits:
                for commit in commits:
                    count = count + 1
                    if commit is not None:
                        if commit.author is not None:
                            first_contributor = commit.author.login
                            print(commit.author.login)
        except:
            print("Error processing repo.")


        print (count)
        # write the comma delimited line to our output file
        line = reponame + "," + created + "," + updated + "," + str(count) + "," + first_contributor + "\n"
        fh.write(line)
        fh.close()
