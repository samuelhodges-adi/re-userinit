from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import http.server
import socketserver
import threading
import psutil


import argparse


# --------- Argument Parser ---------
parser = argparse.ArgumentParser(description="Automate Chrome with Selenium")


default_chrome_data_dir = os.path.join(
    os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data"
)
parser.add_argument(
    "--chrome-data-dir",
    type=str,
    default=default_chrome_data_dir,
    help="Path to Chrome's user data directory (profile root folder)",
)
parser.add_argument(
    "--profile-directory",
    type=str,
    default="Default",
    help="Profile directory to use (e.g., 'Default', 'Profile 1', ...)",
)


args = parser.parse_args()


chrome_data_dir = args.chrome_data_dir
profile_directory = args.profile_directory


print(f"got chrome data dir = {chrome_data_dir}")
print(f"got profile dir {profile_directory}")


# Function to check if the server is already running
def is_http_server_running(port=8000):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            return True
    return False


# Function to start the HTTP server if not already running
def start_http_server(port=8000):
    if not is_http_server_running(port):
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("localhost", port), handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"HTTP server started on localhost:{port}")
    else:
        print(f"HTTP server is already running on localhost:{port}")


# Determine the directory where the script and camera_feed.html live
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Start the HTTP server if it's not already running
start_http_server(port=8000)


# --------- Selenium Config ---------
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"]
)
options.add_argument("--hide-crash-restore-bubble")
options.add_argument("--no-sandbox")
options.add_argument(f"--user-data-dir={chrome_data_dir}")
options.add_argument(f"profile-directory={profile_directory}")
options.add_argument("--disable-dev-shm-usage")


# Download the latest webdriver
service = ChromeService(ChromeDriverManager().install())


driver = webdriver.Chrome(options=options, keep_alive=True)


driver.implicitly_wait(30)


def open_url_and_login(
    url,
    username="",
    password="",
    username_xpath="",
    password_xpath="",
    submit_button_xpath="",
    open_new_tab=True,
) -> bool:
    try:
        if open_new_tab:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        time.sleep(1)


        if username and username_xpath:
            driver.find_element(By.XPATH, username_xpath).send_keys(username)


        if password and password_xpath:
            if not submit_button_xpath:
                password += Keys.RETURN


            driver.find_element(By.XPATH, password_xpath).send_keys(password)


        if submit_button_xpath:
            driver.find_element(By.XPATH, submit_button_xpath).click()


        time.sleep(1)
    except:
        return False


    return True


def open_url(url, open_new_tab=True) -> bool:
    try:


        if open_new_tab:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
    except:
        return False


    time.sleep(1)
    return True


driver.set_window_size(1000, 1200)
driver.set_window_position(0, 0)


# Open PXA
open_url("http://192.168.0.51/", open_new_tab=False)


# Open sma
open_url_and_login(
    "http://192.168.0.50/webpages/instrumentctrl/vnc/novnc/vnc_auto.html?host=192.168.0.50&port=5900&true_color=1",
    password="instrument",
    password_xpath="/html/body/div/div/table/tbody/tr/td/div/form/input",
)


# Open power switch
open_url_and_login(
    "http://192.168.0.100/login.asp",
    "admin",
    "password",
    "/html/body/div/div/div/form/div[2]/input",
    "/html/body/div/div/div/form/div[4]/input",
    "/html/body/div/div/div/form/div[6]",
)


html_file_path = os.path.join(current_dir, "camera_feed.html")
# connect to the local http server and serve the html file
open_url(f"http://localhost:8000/{os.path.basename(html_file_path)}")


driver.refresh()  # make sure extension loads correctly
time.sleep(1)


open_url("https://forms.office.com/r/VChHZ6NQ0Y", open_new_tab=True)


driver.switch_to.window(driver.window_handles[0])


# Click on the PXA: Control Instrument subtab
try:
    driver.find_element(By.XPATH, "/html/body/header/div[3]/div/div[2]/ul/li[2]").click()
except:
    ...
