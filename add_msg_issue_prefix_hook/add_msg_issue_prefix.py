#!/usr/bin/env python3

import sys
import re
import subprocess

def main():
    commit_msg_filepath = sys.argv[1]

    branch = ""
    try:
        branch = subprocess.check_output(["git","symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
        print(commit_msg_filepath, branch)
    except Exception as e:
        print(e)
if __name__ == "__main__":
    exit(main())
