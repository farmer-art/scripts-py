#!/usr/bin/env python3

""" Python Security Log Analyzer sample """

import re
logs = """
 2026-10-13 18:01:12 INFO user=tony ip=192.168.1.10 action=login_success
 2026-10-13 18:02:15 WARNING user=admin ip=203.0.113.25 action=login_failed
 2026-10-13 18:02:40 WARNING user=admin ip=203.0.113.25 action=login_failed
 2026-10-13 18:03:01 WARNING user=root ip=203.0.113.25 action=login_failed
 2026-10-13 18:04:10 INFO user=mary ip=192.168.1.15 action=login_success
 2026-10-13 18:04:45 WARNING user=admin ip=198.51.100.8 action=login_failed
 2026-10-13 18:05:02 WARNING user=admin ip=203.0.113.25 action=login_failed
 """
pattern = (
    r'(\d{4}-\d{2}-\d{2})\s+'
    r'(\d{2}:\d{2}:\d{2})\s+'
    r'(INFO|WARNING)\s+'
    r'user=(\w+)\s+'
    r'ip=([0-9.]+)\s+'
    r'action=([a-z_]+)' )

entries = []
for line in logs.splitlines():
    line = line.strip()
    match = re.fullmatch(pattern, line)
    
    if match:
        entry = {
            "date": match.group(1),
            "time": match.group(2),
            "level": match.group(3),    #Creats a dictonary fo each log entered
            "username": match.group(4),
            "ip": match.group(5),
            "action": match.group(6)
                 }
        entries.append(entry)
print("Total logs entries:", len(entries)) #No of entries perfomed   


### Counting failed logins by IP ###

failed_attempts = {}

for entry in entries:
    if entry["action"] == "login_failed":
        ip = entry["ip"]

        if ip in failed_attempts:
            failed_attempts[ip] += 1
        else:
            failed_attempts[ip] = 1
print(failed_attempts)

### flagging suspicious IP address

threshold = 3

for ip, count in failed_attempts.items():
    if count >= threshold:
        usernames = set()

        for entry in entries:
            if (entry["ip"] == ip
                    and entry["action"] == "login_failed"):
                usernames.add(entry["username"])

        print(f"ALERT : {ip} had {count} login attempts")
        print(f"Targeted usernames: {', '.join(sorted(usernames))}")
