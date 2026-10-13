#!/usr/bin/env python3

import re

logs = """
2026-10-08 10:15:23 INFO User logged in
2026-10-08 10:17:45 ERROR Database connection failed
2026-10-08 10:20:11 WARNING Disk] space low
2026-10-08 10:22:31 INFO User logged out
2026-10-08 10:25:00 DEBUG Retrying database connection
2026-10-08 10:27:00 CRITICAL Database server unavailable
"""
pattern = ( #Extraction pattern
    r'(\d{4}-\d{2}-\d{2})\s+'
    r'(\d{2}:\d{2}:\d{2})\s+'
    r'(INFO|ERROR|WARNING|DEBUG|CRITICAL)\s+'
    r'(.+)')
#Initialize the value of level to 0
counts = {
    "INFO": 0,
    "ERROR": 0,
    "WARNING": 0,
    "DEBUG": 0,
    "CRITICAL": 0,
         }
#parse the logs and count levels
for line in logs.splitlines():
    match = re.fullmatch(pattern, line)
    if match:
        level = match.group(3)
        counts[level] += 1

#print the summary
for level, count in counts.items():
    print(f"{level}: {count}")

