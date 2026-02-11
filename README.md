# PythonAnywhere Activator

Automatically logs into one or multiple **PythonAnywhere** accounts and
extends web apps for one more month using Selenium.

It also sends a daily execution report via **ntfy** showing which
accounts succeeded or failed.

------------------------------------------------------------------------

## 🚀 Features

-   Login to multiple PythonAnywhere accounts
-   Extend web apps automatically
-   Handles failures per account (won't stop on errors)
-   Sends execution report via `ntfy.sh`
-   Designed to run daily (e.g., with cron)
-   Uses Dockerized Selenium Chrome

------------------------------------------------------------------------

## 🧰 Requirements

-   Python 3.10+
-   Docker
-   Google Chrome Selenium container
-   Python dependencies:
    -   selenium
    -   python-dotenv
    -   requests

------------------------------------------------------------------------

## 📦 Installation

### Clone the repository

``` bash
git clone https://github.com/MrMrProgrammer/pythonanywhere-activator.git
cd pythonanywhere-activator
```

### Create virtual environment

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🐳 Start Selenium

Run Selenium Chrome container:

``` bash
docker run -d \
  --name selenium-chrome \
  -p 4444:4444 \
  -p 7900:7900 \
  -e SE_VNC_PASSWORD=your_strong_password \
  selenium/standalone-chrome
```

### 🔐 Changing the Default VNC Password

By default, Selenium images use a predefined VNC password.

You can (and should) change it using:

    -e SE_VNC_PASSWORD=your_strong_password

Then access the VNC viewer at:

    http://localhost:7900

and use your custom password.

### Selenium WebDriver Endpoint

    http://localhost:4444/wd/hub
------------------------------------------------------------------------

## ⚙️ Environment Configuration

Create a `.env` file:

    ACCOUNTS=[{"username":"user1","password":"pass1"}]
    DOMAIN=https://www.pythonanywhere.com
    SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
    TOPIC=your-ntfy-topic

For multiple accounts:

    ACCOUNTS=[{"username":"user1","password":"pass1"},{"username":"user2","password":"pass2"}]

------------------------------------------------------------------------

## ▶️ Run

``` bash
python script.py
```

------------------------------------------------------------------------

## 📬 Report Example

    PythonAnywhere Activator Report

    ⏰ 2026-02-12 08:00

    Success: 1
    Failed: 1

    AccountOne ✅
    AccountTwo ❌

------------------------------------------------------------------------

## ⏰ Cron (Daily Run)

``` bash
0 8 * * * /path/to/venv/bin/python /path/to/script.py
```

------------------------------------------------------------------------

## 🔐 Security

-   Never commit credentials
-   Use `.env` and `.gitignore`
-   Enable 2FA on PythonAnywhere

------------------------------------------------------------------------

## 📄 Disclaimer

Not affiliated with PythonAnywhere.\
Use at your own risk.
