##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import re

from typing import List, Tuple


# Remove characters that are overwritten by newline characters
def fixCarriageReturn(txt: str):
    txt = re.compile(r"\r+\n", re.M).sub("\n", txt)  # \r followed by \n --> newline
    while not re.search(r"\r[^$]", txt) is None:
        base = re.compile(r"^(.*)\r+", re.M).match(txt)[1]
        insert = re.compile(r"\r+(.*)$", re.M).match(txt)[1]
        insert = insert + base.slice(len(insert), len(base))
        txt = re.compile(r"\r+.*$", re.M).sub("\r", txt)
        txt = re.compile(r"^.*\r", re.M).sub(insert, txt)
    return txt


# Remove characters that are overwritten by backspace characters
def fixBackspace(txt: str):
    tmp = txt
    while True:
        txt = tmp
        # Cancel out anything-but-newline followed by backspace
        tmp = re.sub(r"\n?[^\x08]\x08", "", txt)
        if len(tmp) >= len(txt):
            break
    return txt


def collapseUpdates(updates: List[Tuple[str, str]]):
    message = ""
    last_non_detail = ""
    for line, modifier in updates:
        if line != "error" and line != "stop" and line != "launched" and line != "closed" and line != "":
            if not modifier.startswith("{"):
                # Suppress duplicate update messages
                if line != last_non_detail:
                    last_non_detail = line
            message += line
            if not message.endswith("\n"):
                message += "\n"

    return fixBackspace(fixCarriageReturn(message))
