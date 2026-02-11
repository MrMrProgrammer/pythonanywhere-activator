import json
import os
from datetime import datetime
from time import sleep

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

ACCOUNTS = json.loads(os.getenv("ACCOUNTS", "[]"))
DOMAIN = os.getenv("DOMAIN")
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL")
TOPIC = os.getenv("TOPIC")


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL,
        options=options
    )
    driver.maximize_window()
    return driver, WebDriverWait(driver, 20)


def is_login_page(driver):
    return "login" in driver.current_url


def login(driver, wait, username, password):
    if not is_login_page(driver):
        driver.get(f"{DOMAIN}/login/")

    wait.until(
        EC.presence_of_element_located((By.ID, "id_auth-username"))
    ).clear()
    wait.until(
        EC.presence_of_element_located((By.ID, "id_auth-username"))
    ).send_keys(username)

    driver.find_element(By.ID, "id_auth-password").clear()
    driver.find_element(By.ID, "id_auth-password").send_keys(password)

    driver.find_element(By.ID, "id_auth-password").submit()


def extend_webapp(driver, wait, username):
    driver.get(f"{DOMAIN}/user/{username}/webapps")
    run_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "webapp_extend"))
    )
    run_button.click()


def logout(driver, wait):
    logout_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "logout_link"))
    )
    logout_button.click()


def build_report(results: list[tuple[str, bool]]) -> str:
    if not results:
        return "PythonAnywhere Activator ⚠️\nNo accounts were processed."

    results = sorted(results, key=lambda x: x[0].lower())

    lines = []
    success_count = 0

    for username, status in results:
        icon = "✅" if status else "❌"
        if status:
            success_count += 1
        lines.append(f"{username} {icon}")

    fail_count = len(results) - success_count
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    header = f"PythonAnywhere Activator Report\n\n⏰ {now}\n\n"
    summary = f"Success: {success_count}\nFailed: {fail_count}\n\n"

    return header + summary + "\n".join(lines)


def send_report(results: list[tuple[str, bool]]):
    message = build_report(results)

    try:
        response = requests.post(
            f"https://ntfy.sh/{TOPIC}",
            data=message.encode("utf-8"),
            timeout=10
        )

        if response.status_code == 200:
            print("📨 Report sent successfully.")
        else:
            print(f"⚠️ Failed to send report. Status: {response.status_code}")

    except Exception as e:
        print(f"❌ Error sending notification: {e}")


results = []

for account in ACCOUNTS:
    driver, wait = create_driver()
    username = account["username"]

    try:
        login(driver, wait, account["username"], account["password"])
        extend_webapp(driver, wait, account["username"])
        sleep(2)
        logout(driver, wait)
        sleep(1)

        results.append((username, True))

    except Exception:
        print(f"❌ Error for {username}")
        results.append((username, False))

    finally:
        driver.quit()


send_report(results)
