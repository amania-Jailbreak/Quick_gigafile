from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import os
import pyperclip,subprocess

# コマンドライン引数を取得します（最初の引数はスクリプト自体なので無視します）。
args = sys.argv[1:]

# ファイルパスを格納するためのリストを初期化します。
file_paths = ""

# 各引数について確認します。
for arg in args:
    if os.path.isdir(arg):
        print(f"{arg} is a directory. Exiting.")
    elif os.path.isfile(arg):
        file_paths += arg + "\n"
    else:
        print(f"{arg} does not exist. Exiting.")

# 結果のリストを表示します。
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument("--headless")
def upload_file_and_get_link(file_path:str, password=None):
        try:
            service = webdriver.EdgeService(service_args=['--log-level=OFF'],log_output=None)
            driver = webdriver.Edge(options=options,service=service)
            print("ページを読み込んでいます")
            driver.get("https://gigafile.nu/")
            print(file_path)
            upload_panel = driver.find_element(By.ID, 'upload_panel_button')
            file_input = upload_panel.find_element(By.XPATH,".//input[@type='file']")
            file_input.send_keys(file_path.rstrip('\n'))
            time.sleep(1)
            print("アップロードしています")
            while True:
                time.sleep(1)
                elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'prog file_info_prog')]")
                all_complete = True
                for elementss in elements:
                    if "width: 100%;" not in elementss.get_attribute('style'):
                        all_complete = False
                        break
                if all_complete:
                    break
            print("zipにしています")
            password_field = driver.find_element(By.ID,"zip_dlkey")
            password_field.send_keys(password)
            zip_file_field = driver.find_element(By.ID,"zip_file_name")
            zip_file_field.send_keys("FILE")
            set_button = driver.find_element(By.ID,"matomete_btn")
            driver.execute_script("arguments[0].click();", set_button)
            time.sleep(1)
            alert = Alert(driver)
            alert_text = alert.text
            print(alert_text)
            alert.accept()
            link_element = driver.find_element(By.XPATH,"//a[@id='matomete_link_btn']")
            link = link_element.get_attribute("href")
            print("成功")
            print("クリップボードにコピーされました")
            return link
        except Exception as e:
            print("失敗")
            return "共有リンクの作成に失敗しました"
pyperclip.copy(str(upload_file_and_get_link(file_paths, input("パスワード>>"))))
