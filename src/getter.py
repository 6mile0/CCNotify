# Get calendar data from TEU Inside Page
import re
import filecmp
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()

# Load form project root .env file
MAIL_ADDRESS = os.getenv('EMAIL')
PASSWORD = os.getenv('PASS')
DATA_DIR = os.getenv('DATADIR')


# 独自例外


class GetterError(Exception):
    pass


# 生データ取得


def get_raw_data():
    try:
        # Seleniumへ接続
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=webdriver.ChromeOptions())

        driver.implicitly_wait(10)

        # カレンダー画面へ遷移
        driver.get("https://service.cloud.teu.ac.jp/aesc/cal/index.php")

        # 2秒待機
        time.sleep(2)

        # メールアドレス入力
        driver.find_element(By.ID, "identifierId").send_keys(MAIL_ADDRESS)

        # メールアドレス送信
        driver.find_element(By.ID, "identifierId").send_keys(Keys.ENTER)

        # 2秒待機
        time.sleep(2)

        # パスワード入力
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        # パスワード送信
        driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

        # 1秒待機
        time.sleep(3)

        # カレンダーのタイトルを取得
        cal_name = driver.find_element(By.ID, 'month').text
        file_name = cal_name.replace('年', '-').replace('月', '')

        # カレンダーのHTMLを取得
        cal_html = driver.find_element(By.TAG_NAME, 'script')

        # ファイルに書き込み
        with open(f"{DATA_DIR}/raw/{file_name}.txt", 'w') as f:
            f.write(cal_html.get_attribute('innerHTML'))

        time.sleep(3)

        return file_name

    except Exception as e:
        raise GetterError(e)
    finally:
        driver.quit()

# 生データをパースしてJSONに変換


def parse_data(filename):
    with open(filename, "r") as f:
        r = re.search(r'var schedules = (.+?);', f.read()).group(1)
        r.replace('var', '').replace(';', '')
        return json.loads(r)

# JSONをファイルに保存


def save(filename, data, indent=4):
    with open(filename, "w") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

# ファイルを比較


def compare(filename1, filename2):
    return filecmp.cmp(filename1, filename2)

# メイン処理


if not (os.path.exists(f"{DATA_DIR}/latest.json")):
    f = open(f"{DATA_DIR}/latest.json", 'w')
    f.write("newfile")
    f.close()

# データ取得開始
try:
    print('Step 1 / 4 > Getting calendar data...')
    file_name: str = get_raw_data()
    print('>> Success...')
    print('Step 2 / 4 > Parsing calendar data...')
    result: dict = parse_data(f"{DATA_DIR}/raw/{file_name}.txt")
    print('>> Success...')
    print('Step 3 / 4 > Saving calendar data...')
    save(f"{DATA_DIR}/processed/{file_name}.json", result)
    print('>> Success...')
    print('Step 4 / 4 > Comparing calendar data..')
    if compare(f"{DATA_DIR}/processed/{file_name}.json", f"{DATA_DIR}/latest.json"):
        print('>> Same data...')
        print('> Skip...')
    else:
        print('>> New data...')
        print('> Update...')
        save(f"{DATA_DIR}/latest.json", result)
        print('>> Success...')
except Exception as e:
    print(e)
    print('>> Failed...')
    exit(1)
