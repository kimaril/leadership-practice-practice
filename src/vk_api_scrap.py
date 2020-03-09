import re
import requests
from requests.utils import requote_uri
from tqdm import tqdm
import json
import argparse
import pandas as pd
import os
import sys
import time
import logging

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

save_folder = "vk-api-saved"
os.makedirs(save_folder, exist_ok=True)

def get_single_leader(uid: str, attempt: int=100) -> dict:
    access_token = os.environ["ACCESS_TOKEN"]
    url_single_execute = f"https://api.vk.com/method/execute.singleLeader?user={{}}&access_token={access_token}&v=5.103"
    for i in range(attempt):        
        response = requests.get(url_single_execute.format(uid)).json()
        if response.get("response"):
            return response
        print("Sleep")
        time.sleep(1)      
    raise Exception(f"After {attempt} attempts no response!!!")

def save_single_leader(uid: str, path: str):
    data = get_single_leader(uid)
    assert len(data["response"]) == 3
    with open(f"{path}/{uid}.json", 'w') as f:
        f.write(json.dumps(data))

def get_batch_wall_leader(uids: list, attempt: int=15, batch: int=25) -> list:
    access_token = os.environ["ACCESS_TOKEN"]
    url_batch_execute = f"https://api.vk.com/method/execute.batchLeader?users={{}}&access_token={access_token}&v=5.103"
    uids_list = list(map(lambda x: str(x), uids))
    uids_str = f"'[{','.join(uids_list)}]'"
#     url = requote_uri(url_batch_execute.format(uids))
    for i in range(attempt):        
        response = requests.get(url_batch_execute.format(uids_str)).json()
        if response.get("response"):
            return response
        print("Sleep")
        time.sleep(1)      
    raise Exception(f"After {attempt} attempts no response!!!")

def main(access_token):
    try:
        os.environ["ACCESS_TOKEN"] = access_token
    except:
        raise Exception("Set ACCESS_TOKEN env")  

    users = pd.read_csv("../data/raw_data/users.csv")

    for uid in tqdm(users.uid):
#         print(uid)
        debug_data = save_single_leader(str(uid), "vk-api-saved")
    
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('token', metavar='token', type=str, help='VK API access token')
    args = parser.parse_args()

    print('Scraping began!')
    main(args.token)