import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlsplit
import pandas as pd
from tqdm import tqdm
import os
from selenium.webdriver.firefox.options import Options
import time

class OAuthHandler:
    def __init__(self, login: str, password: str) -> str:
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.login_xpath = '/html/body/div/div/div/div[2]/form/div/div/input[6]'
        self.password_xpath = '/html/body/div/div/div/div[2]/form/div/div/input[7]'
        self.button_xpath = '//*[@id="install_allow"]'
        self.login = login
        self.password = password

    def auth(self, link):
        self.driver.get(link)
        try:
            email_field = self.driver.find_element_by_xpath(self.login_xpath)
            password_field = self.driver.find_element_by_xpath(self.password_xpath)

            email_field.send_keys(self.login)
            password_field.send_keys(self.password)

            self.driver.find_element_by_xpath(self.button_xpath).click()
        except:
            pass
        return self.driver.current_url

def get_token(APP_ID: int) -> str:
    login = input('Phone or email: ')
    password = input('Password: ')
    AUTH_URL = "https://oauth.vk.com/authorize?client_id={APP_ID}&display=page&response_type=token&v=5.103"
    response = OAuthHandler(login, password).auth(AUTH_URL.format(APP_ID=APP_ID))
    token = urlsplit(response, scheme='https').fragment.split('&')[0].split('=')[-1]
    return token

def get_single_leader(uid: str, access_token: str, attempt: int=5) -> dict:
    url_single_execute = f"https://api.vk.com/method/execute.singleLeader?user={{}}&access_token={access_token}&v=5.103"
#     print(url_single_execute)

    for i in range(attempt):
        response = requests.get(url_single_execute.format(uid)).json()
        if response.get('response'):
            return response
        print("Sleep")
        time.sleep(1)
    raise Exception(f"After {attempt} attempts no response!!!")

def save_single_leader(uid: str, token: str, path: str):
    data = get_single_leader(uid, token)
    assert len(data["response"]) == 5
    with open(f"{path}/{uid}.json", 'w') as f:
        f.write(json.dumps(data))

def scrap():
    dirname = input('Name of directory to save to (default \'leadership-practice-practice/data/\'): ')
    APP_ID = int(input('VK Standalone App ID: '))
    TOKEN = get_token(APP_ID)
    savepath = f"../data/{dirname}"

    users = pd.read_csv("../notebooks/uids_for_vk_scrap.csv").iloc[::-1].uid[15000:]
    debug_data = []
    for uid in tqdm(users):
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        debug_data.append(save_single_leader(str(uid), TOKEN, savepath))

    with open('./debug_data.txt', encoding='utf-8', mode='w') as f:
        for dd in debug_data:
            f.write(dd+'\n')

if __name__=='__main__':
    scrap()
