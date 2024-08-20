from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

user_home_dir = os.path.expanduser("~")
chrome_data_dir = os.path.join(
    user_home_dir, "AppData", "Local", "Google", "Chrome", "User Data"
)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option(
    "excludeSwitches", ["enable-automation", "enable-logging"]
)
options.add_argument("--hide-crash-restore-bubble")
options.add_argument("--no-sandbox")
# options.add_argument("--remote-debugging-port=9292")
options.add_argument(f"--user-data-dir={chrome_data_dir}")
options.add_argument("profile-directory=Default")
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
):
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


def open_url(url, open_new_tab=True):
    if open_new_tab:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(1)


driver.set_window_size(1000, 1200)
driver.set_window_position(0, 0)

# Open PXA
open_url("http://169.254.149.210/", open_new_tab=False)

# Open sma
open_url_and_login(
    "http://169.254.2.20/webpages/instrumentctrl/vnc/novnc/vnc_auto.html?host=169.254.2.20&port=5900&true_color=1",
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

# Open camera feed
webcam_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Feed</title>
</head>
<body>
    <h1>Board Camera Feed</h1>
    <video id="video" width="1920" height="1080" autoplay></video>

    <script>
        // Get access to the camera
        async function getCameraFeed() {
            try {
                const constraints = {
                    video: {
                        width: 1920,
                        height: 1080,
                    }
                };
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                const video = document.getElementById('video');
                video.srcObject = stream;
            } catch (error) {
                console.error('Error accessing camera: ', error);
            }
        }

        // Initialize the camera feed
        window.onload = getCameraFeed;
    </script>
</body>
</html>
"""
open_url(f"data:text/html;charset=utf-8,{urllib.parse.quote(webcam_html)}", open_new_tab=True)


driver.refresh()  # make sure extension loads correctly
time.sleep(1)

driver.switch_to.window(driver.window_handles[0])

# Click on the PXA: Control Instrument subtab
driver.find_element(By.XPATH, "/html/body/header/div[3]/div/div[2]/ul/li[2]").click()
