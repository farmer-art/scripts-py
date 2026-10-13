#!/usr/bin/env python3

""" log praser. Extracting logs """ 

import re

logs = """
2026-10-08 10:15:23 INFO User logged in
2026-10-08 10:17:45 ERROR Database connection failed
2026-10-08 10:20:11 WARNING Disk space low
2026-10-08 10:22:31 INFO User logged out
2026-10-08 10:25:00 DEBUG Retrying database connection
2026-10-08 10:27:00 CRITICAL Database server unavailable
"""
pattern = ( 
    r'(\d{4}-\d{2}-\d{2})\s+'
    r'(\d{2}:\d{2}:\d{2})\s+'
    r'(INFO|ERROR|WARNING|DEBUG|CRITICAL)\s+'
    r'(.+)'
)

result = []

for line in logs.splitlines():
    match = re.fullmatch(pattern, line)
    if match:
        entry = {
            "date": match.group(1),
            "time": match.group(2),
            "level": match.group(3),
            "message": match.group(4) }
        result.append(entry)

for entry in result:
    if entry["level"] in ("ERROR", "CRITICAL"):
        print(entry)       
