#!/usr/bin/env python3


import re
import pprint
import ipaddress


logs = """
2026-10-13 18:01:12 INFO user=tony ip=192.168.1.10 action=login_success
2026-10-13 18:02:15 WARNING user=admin ip=203.0.113.25 action=login_failed
2026-10-13 18:02:40 WARNING user=admin ip=203.0.113.25 action=login_failed
2026-10-13 18:03:01 WARNING user=root ip=203.0.113.25 action=login_failed
2026-10-13 18:04:10 INFO user=mary ip=192.168.1.15 action=login_success
2026-10-13 18:04:45 WARNING user=admin ip=198.51.100.8 action=login_failed
2026-10-13 18:05:02 WARNING user=admin ip=203.0.113.25 action=login_failed
2026-10-13 18:05:30 ERROR user=guest ip=198.51.100.8 action=login_failed
2026-10-13 18:06:10 WARNING user=guest ip=198.51.100.8 action=login_failed
2026-10-13 18:07:00 INFO user=admin ip=203.0.113.25 action=login_success
INVALID LOG ENTRY
2026-10-13 18:08:10 WARNING user=test ip=999.999.999.999 action=login_failed
2026-10-13 18:09:10 WARNING user=guest ip=198.51.100.8 action=login_failed
"""
pattern = (
    r'(\d{4}-\d{2}-\d{2})\s+'
    r'(\d{2}:\d{2}:\d{2})\s+'
    r'(INFO|WARNING|ERROR)\s+'
    r'user=(\w+)\s+'
    r'ip=([0-9.]+)\s+'
    r'action=([a-z_]+)'
   # r'INVALID LOG ENTRY'
    
)

entries = []
malformed_count = 0
invalid_ip_count = 0
failed_login_attempts = {}

for line in logs.splitlines():
    line = line.strip()

    match = re.fullmatch(pattern, line)

    if not match:
        print("malformed line:", line)
        malformed_count += 1
        continue

    ip = match.group(5)

    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:
        invalid_ip_count += 1
        print(f"Invalid IP address: {ip}")
        continue    

    entry = {
            "date": match.group(1),
            "time": match.group(2),
            "level": match.group(3),
            "username": match.group(4),
            "IP": match.group(5),
            "action": match.group(6)
        }

    entries.append(entry)

for entry in entries:
    if entry["action"] == "login_failed":
        ip = entry["IP"]

        if ip in failed_login_attempts:
           failed_login_attempts[ip] += 1
        else:
            failed_login_attempts[ip] = 1

print("\nFailed login counts:")

for ip, count in failed_login_attempts.items():
    print(f"{ip}: {count}")


        
        

print("Total valid-format entries:", len(entries))

print("Malformed entries:", malformed_count)
print("Invalid IP entries:", invalid_ip_count)


