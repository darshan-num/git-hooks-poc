#!/usr/bin/env python3

import sys
import re
import subprocess

import http.client
import json



def main():
    branch = ""
    try:
        branch = subprocess.check_output(["git","symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
        
        branch_name = branch.split('_')
        project_name = branch_name[1]
        task_key = branch_name[2]

        domain = "numerator"

        issue_key = project_name + "-" + task_key
        url = "https://" + domain + ".atlassian.net/rest/agile/1.0/issue/" + issue_key + ""

        headers = {
            "Accept": "application/json",
            "Authorization": "Basic ZGFyc2hhbi5zaGV0aEBudW1lcmF0b3IuY29tOnFnS1ZmTFBaTVRiUnBZUU5DazFNOUVDNQ=="
        }
        connection = http.client.HTTPSConnection('www.atlassian.net')
        connection.request("GET", url, headers=headers)
        response = connection.getresponse().read()
        reponse = (json.dumps(json.loads(response), sort_keys=True, indent=4, separators=(",", ": ")))
        response = json.loads(response)

        if response.get('errorMessages'):
            raise SystemExit("Invalid branch name!" + "\nMessage:" + str(response.get('errorMessages')))

        assignee = response.get("fields")["assignee"]["displayName"]
        creator = response.get("fields")["creator"]["displayName"]
        status = response.get("fields")["aggregateprogress"]["percent"]
        print("==============")
        print(
            "Commiting to Jira task = " + issue_key + "\nAssigned to = " + assignee + "\nAssigned by = " + creator + "\nTask Status = " + str(
                status) + "%")
        print("==============")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    exit(main())
