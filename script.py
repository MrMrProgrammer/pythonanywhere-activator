from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOMAIN = "https://www.pythonanywhere.com"
SELENIUM_REMOTE_URL = "http://localhost:4444/wd/hub"

ACCOUNTS = [
    # {"username": "", "password": ""},
]

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Remote(
    command_executor=SELENIUM_REMOTE_URL,
    options=options
)
driver.maximize_window()
wait = WebDriverWait(driver, 20)


def is_login_page():
    return "login" in driver.current_url


def login(username, password):
    if not is_login_page():
        driver.get(f"{DOMAIN}/login/")
    wait.until(EC.presence_of_element_located((By.ID, "id_auth-username"))).clear()
    wait.until(EC.presence_of_element_located((By.ID, "id_auth-username"))).send_keys(username)
    driver.find_element(By.ID, "id_auth-password").clear()
    driver.find_element(By.ID, "id_auth-password").send_keys(password)
    driver.find_element(By.ID, "id_auth-password").submit()
    wait.until(EC.presence_of_element_located((By.ID, "id_dashboard")))
    print(f"✅ Logged in as {username}")


def extend_webapp(username):
    driver.get(f"{DOMAIN}/user/{username}/webapps")
    run_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "webapp_extend"))
    )
    run_button.click()
    print(f"✅ Web app for {username} extended for 1 month")


def logout():
    logout_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "logout_link"))
    )
    logout_button.click()
    print("✅ Logged out")


for account in ACCOUNTS:
    try:
        login(account["username"], account["password"])
        extend_webapp(account["username"])
        sleep(2)
        logout()
        sleep(1)
    except Exception as e:
        print(f"❌ Error for {account['username']}: {e}")
        driver.save_screenshot(f"error_{account['username']}.png")

driver.quit()
