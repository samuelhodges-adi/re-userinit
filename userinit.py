from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# time.sleep(30)

user_home_dir = os.path.expanduser('~')
chrome_data_dir = os.path.join(user_home_dir, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')

options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument('--hide-crash-restore-bubble')
options.add_argument("--no-sandbox") 
# options.add_argument("--remote-debugging-port=9292")
options.add_argument(f"--user-data-dir={chrome_data_dir}")
options.add_argument("profile-directory=Default")
options.add_argument("--disable-dev-shm-usage")

# Download the latest webdriver
service=ChromeService(ChromeDriverManager().install())

driver = webdriver.Chrome(options=options, service=service ,keep_alive=True)

driver.implicitly_wait(30)

def open_url_and_login(url, username = "", password = "", username_xpath = "", password_xpath = "", submit_button_xpath = "", open_new_tab = True):
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


def open_url(url, open_new_tab = True):
    if open_new_tab:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(1)

driver.set_window_size(1000,1200)
driver.set_window_position(0,0)

# Open PXA 
open_url("http://169.254.149.210/", open_new_tab=False)

# Open sma
open_url_and_login("http://169.254.2.20/webpages/instrumentctrl/vnc/novnc/vnc_auto.html?host=169.254.2.20&port=5900&true_color=1",
                password="instrument",
                password_xpath="/html/body/div/div/table/tbody/tr/td/div/form/input")

# Open power switch
open_url_and_login("http://192.168.0.100/login.asp", 
                    "admin", 
                    "password", 
                    "/html/body/div/div/div/form/div[2]/input",
                    "/html/body/div/div/div/form/div[4]/input",
                    "/html/body/div/div/div/form/div[6]")
driver.refresh() # make sure extension loads correctly
time.sleep(1)

driver.switch_to.window(driver.window_handles[0])

def driver_is_connected():
    try:
        driver.title
        return True
    except:
        return False

SleepTime = 5
MaxWaitTimeInMinutes = 120

for _ in range(MaxWaitTimeInMinutes*60 // SleepTime):

    if not driver_is_connected():
        driver.quit()
        break
        
    time.sleep(5)

print("Done")
