from selenium import webdriver as WD
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from time import ctime, time, sleep
from selenium import webdriver
import tgmessage
import schoolcount
# from xvfbwrapper import Xvfb
 # Initiate Chrome Browser
def loginMySAT():
    driver.get("https://mysat.collegeboard.org/") # Login to website
    driver.refresh()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div/div/div/div/div/div/div/a'))).click() # Click the first continue button
    sleep(2)
    elementIdpUsername = driver.find_element(By.XPATH, '//*[@id="idp-discovery-username"]') # Identify username inout field
    elementIdpUsername.clear()
    elementIdpUsername.send_keys("***@gmail.com") # Enter required email, to be prompted in next update if required
    
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idp-discovery-submit"]'))).click() # Trigger click event on Next "submit" type button after entering email
    except ElementClickInterceptedException:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idp-discovery-submit"]'))).click() # Trigger click event on Next "submit" type button after entering email
    else:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="okta-signin-password"]')))
        elementIdpPasswd = driver.find_element(By.XPATH, '//*[@id="okta-signin-password"]') # Identify Password input field
        elementIdpPasswd.clear()
        elementIdpPasswd.send_keys("***") # Enter required password TODO: remove password before pushing to GitHub!!!!!!
        driver.find_element(By.XPATH, '//*[@id="okta-signin-submit"]').click() # Trigger click event to submit password and email
        #print(driver.title)


def satreg():
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-id-header-register-button"]'))).click()
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div/div[2]/div[2]/button'))).click()
    except TimeoutException:
        print("reloading")
        driver.get("https://mysat.collegeboard.org/dashboard")
        satreg()
    except ElementClickInterceptedException:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div/div[2]/div[2]/button'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="graddate-save-button"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grade-save-button"]'))).click()
    sleep(5)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="continue-to-demographics-btn"]'))).click()
    sleep(5)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save-exit-demographics-btn"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div[2]/div[2]/button[1]'))).click() # SAT Registration. Get Started Button
    driver.find_element(By.XPATH, '//*[@id="terms-desc"]').send_keys(Keys.END)
    sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/label/span').click() # Click the checkbox
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="forward-btn"]'))).click() # Continue
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="testlocation-continue-button"]'))).click()


def refreshTestCenter():
    sleep(2)
    if driver.title == "SAT Registration":
        driver.refresh()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div[2]/div[2]/button[1]'))).click() # SAT Registration. Get Started Button
    findtestcenter()


def chooseTestDate():
    driver.execute_script("window.scrollTo(0,600)")
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "test-center-date-button-JUN-3"))).click() # No need for May 6, deadline passed
    print("Jun 3 checked: ", driver.find_element(By.ID, 'test-center-date-button-JUN-3').get_attribute('aria-current'))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="testdate-continue-button"]'))).click()


def findtestcenter():
    global jun_3
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div[1]/div/div/div/div[4]/div/div/div/div[1]/div/div/div[3]/div/div[3]/div/div/div[3]/button'))).click() # Find a test center
    sleep(2)
    driver.find_element(By.CLASS_NAME, 'toggle-btn').click()
    jun_3 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div[1]/div/div/div/div[4]/div/div/div/div[1]/div/div/div[3]/div/div[3]/div/div/div[4]/div[2]/div[1]').text # Save text
    print("June 3: {0}, Checked: {1}".format(jun_3, ctime(time())))

previous = 0
def checkSchools(counter: str):
    global previous
    Message = [f"Last update: {ctime(time())}\n\n"]
    if ((int)(counter) > 0):
        print(driver.find_element(By.ID, 'undefined_next').get_attribute("aria-disabled"))
        while (driver.find_element(By.ID,'undefined_next').get_attribute("aria-disabled") != "true"):
            table = driver.find_element(By.CLASS_NAME, 'cb-table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            for tr in table:
                school_name = tr.find_element(By.CLASS_NAME, 'test-center-name').text
                seat_available = tr.find_element(By.CLASS_NAME, 'seat-label').text
                Message.append("{0} : {1}\n".format(school_name, seat_available))
            driver.find_element(By.CLASS_NAME, 'cb-right').click()
        table = driver.find_element(By.CLASS_NAME, 'cb-table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
        for tr in table:
            school_name = tr.find_element(By.CLASS_NAME, 'test-center-name').text
            seat_available = tr.find_element(By.CLASS_NAME, 'seat-label').text
            Message.append("{0} : {1}\n".format(school_name, seat_available))
        print(previous)
        Message = "\n".join(Message)
        print(Message)
        if previous == 0:
            print(tgmessage.telegram_sendmessage(***, Message))
            print(tgmessage.telegram_sendmessage(***, Message))
            print(tgmessage.telegram_sendmessage(***, Message))
            print("Email sent, sleeping...")
    previous = (int)(schoolcount.stripresult(jun_3))
    

op = webdriver.ChromeOptions()
#op.add_argument("--headless")
op.add_argument("--disable-browser-side-navigation")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")
while(1):
    try:
        driver = WD.Chrome(options=op)
        print("Logging in")
        loginMySAT()
        print("Entering registration")
        satreg()
        print("Choosing test date:")
        chooseTestDate()
        print("Finding test centers")
        findtestcenter()
        checkSchools(schoolcount.stripresult(jun_3))
        while(1): # Infinite loop which breaks if an exception appears
            try:
                refreshTestCenter()
            except:
                break
            else:
                checkSchools(schoolcount.stripresult(jun_3))            
        #sleep(60)
        print("Restarting the loop")
    except TimeoutException:
        print(TimeoutException)
        continue
    #except ElementClickInterceptedException:
    #    print(ElementClickInterceptedException)
    #    continue
