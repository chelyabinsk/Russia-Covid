#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import requests
import json
import re
import os
import datetime
import random

url = "https://стопкоронавирус.рф/information/"
data_base_url_format = "https://xn--80aesfpebagmfblc0a.xn--p1ai/covid_data.json?do=region_stats&code={}"
datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")

webpage_html = requests.get(url)
#region_codes = re.findall('data-code=\"(.*?)\"',webpage_html.text)

# Dictionary of names
with open("full/regions name map.json", "r", encoding="utf8") as f:
    region_name_dictionary = json.loads(f.read())

# Extract today's json from html
today_json = json.loads(re.findall("spread-data='(.*?)'",webpage_html.text)[0])
for region in today_json:
    code = region["code"]
    directory = "regions/{}/{}".format(code,datetime_str)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + "/vaccines.json", "w", encoding="utf8") as f:
        f.write(json.dumps(region))
        
# Write full table
if not os.path.exists("full/vaccines.csv"):
    header_row = "Folder name, Region name Russian, Region name English, Date, Extract Date, Infected, Recovered, Deceased, First jab, Second jab, Immunity pct\n"
    with open("full/vaccines.csv","w",encoding="utf8") as f:
        f.write(header_row)
with open("full/vaccines.csv","a",encoding="utf8") as f:
    for region in today_json:
        row_text = ",".join(
            str(i) for i in [
                region["code"],
                region_name_dictionary[region["code"]]["ru"],
                region_name_dictionary[region["code"]]["en"],
                region["date"],
                datetime_str,
                region["sick"],
                region["healed"],
                region["died"],
                region["first"],
                region["second"],
                float(region["immune_percent"]),
                ]
            ) + "\n"
        f.write(row_text)



region_codes = list(region_name_dictionary.keys())


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

json_list = []
# Download and save raw JSON files
for code in region_name_dictionary.keys():
    directory = "regions/{}/{}".format(code,datetime_str)
    data_base_url = data_base_url_format.format(code)
    if not os.path.exists(directory):
        os.makedirs(directory)
    useragent = "".join([alphabet[random.randint(0,len(alphabet)-1)] for i in range(random.randint(0,36))])
    headers = {"User-Agent": useragent}
    print(code)
    json_response = requests.get(data_base_url,headers=headers).json()
    json_list.append(json_response)
    
    with open(directory + "/data.json","w") as f:
        f.write(json.dumps(json_response))
        


# Process tables
with open("full/infections.csv", "w") as f:
    # Write header
    f.write("Folder name, Region name Russian, Region name English, Date, Infected, Recovered, Deceased\n")
    for region_count, region_data in enumerate(json_list):
        for line_count,line in enumerate(region_data):
            line_data = ",".join(str(i) for i in [region_codes[region_count],
                  region_name_dictionary[region_codes[region_count]]["ru"],
                  region_name_dictionary[region_codes[region_count]]["en"],
                  line["date"],line["sick"],line["healed"],line["died"]]) + "\n"
            f.write(line_data)