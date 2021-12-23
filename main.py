#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import requests
import json
import re
import os
import datetime

url = "https://стопкоронавирус.рф/information/"

webpage_html = requests.get(url)
region_codes = re.findall('data-code=\"(.*?)\"',webpage_html.text)

data_base_url = "https://xn--80aesfpebagmfblc0a.xn--p1ai/covid_data.json?do=region_stats&code={}"

datetime_str = datetime.datetime.now().strftime("%Y-%m-%d")

for code in region_codes:
    directory = "regions/{}/{}".format(code,datetime_str)
    data_base_url = data_base_url.format(code)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print(code)
    json_response = requests.get(data_base_url).json()
    
    with open(directory + "/data.json","w") as f:
        f.write(json.dumps(json_response))
