import requests
import os
import json
import git

BASE_URL="http://gitlab.com/api/v4/groups/"
SUBGROUPS = "/subgroups"
PATH = "/tmp/gitlab/"

headers = {
    'PRIVATE-TOKEN': '',
    'Content-Type': 'application/json',
}

def clone_repo(path, url):
    if not os.path.exists(path):
        os.makedirs(path)
    git.Git(path).clone(url)

def get_projects(path, groupID):
    projects = requests.get(BASE_URL + str(groupID), headers=headers, verify=False)
    for project in projects.json()["projects"]:
        print(project["ssh_url_to_repo"])
        clone_repo(path, project["ssh_url_to_repo"])

    subgroups = requests.get(BASE_URL + str(groupID) + SUBGROUPS, headers=headers, verify=False)
    
    for subgroup in subgroups.json():
        get_projects(path + subgroup["name"] + "/",subgroup["id"])

def cloneAllProjects(groupID):
    get_projects(PATH,groupID)

def main():
    cloneAllProjects(70)

if __name__ == "__main__":
    main()