from selenium import webdriver as WD
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException
from time import ctime, time, sleep
import traceback
import threading as thrd
import tgmessage
import schoolcount
 # Initiate Chrome Browser
def loginMySAT(driver, email, password):
    driver.get("https://mysat.collegeboard.org/") # Login to website
    driver.refresh()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div/div/div/div/div/div/div/a'))).click() # Click the first continue button
    sleep(2)
    elementIdpUsername = driver.find_element(By.XPATH, '//*[@id="idp-discovery-username"]') # Identify username inout field
    elementIdpUsername.clear()
    elementIdpUsername.send_keys(email) # Enter required email, to be prompted in next update if required
    
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idp-discovery-submit"]'))).click() # Trigger click event on Next "submit" type button after entering email
    except ElementClickInterceptedException:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idp-discovery-submit"]'))).click() # Trigger click event on Next "submit" type button after entering email
    else:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="okta-signin-password"]')))
        elementIdpPasswd = driver.find_element(By.XPATH, '//*[@id="okta-signin-password"]') # Identify Password input field
        elementIdpPasswd.clear()
        elementIdpPasswd.send_keys(password) # Enter required password TODO: remove password before pushing to GitHub!!!!!!
        driver.find_element(By.XPATH, '//*[@id="okta-signin-submit"]').click() # Trigger click event to submit password and email
        #print(driver.title)


def satreg(driver):
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-id-header-register-button"]'))).click()
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div/div[2]/div[2]/button'))).click()
    except TimeoutException:
        print("reloading")
        driver.get("https://mysat.collegeboard.org/dashboard")
        satreg(driver)
    except ElementClickInterceptedException:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div/div[2]/div[2]/button'))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-id-personalinfo-button-graddateconfirm"]'))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-id-personalinfo-button-gradeconfirm"]'))).click()
    sleep(5)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="continue-to-demographics-btn"]'))).click()
    sleep(5)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save-exit-demographics-btn"]'))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div[2]/div[2]/button[1]'))).click() # SAT Registration. Get Started Button
    driver.find_element(By.XPATH, '//*[@id="qc-id-termsconditions-scrollbox-termsconditions"]').send_keys(Keys.END)
    sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/label/span').click() # Click the checkbox
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="forward-btn"]'))).click() # Continue
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-id-selectdatecenter-testlocation-button-next"]'))).click()


def refreshTestCenter(test_date, driver):
    sleep(2)
    if driver.title == "SAT Registration":
        driver.refresh()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div[2]/div[2]/button[1]'))).click() # SAT Registration. Get Started Button
    findtestcenter(test_date=test_date, driver=driver)


def chooseTestDate(test_date: str, driver):
    driver.execute_script("window.scrollTo(0,600)")
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, f"qc-id-selectdatecenter-testdate-button-{test_date}"))).click() # No need for May 6, deadline passed
    print(f"{test_date} checked: ", driver.find_element(By.ID, f'qc-id-selectdatecenter-testdate-button-{test_date}').get_attribute('aria-current'))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="testdate-continue-button"]'))).click()


def findtestcenter(test_date: str, driver):
    global jun_3
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'qc-id-selectdatecenter-testcenter-international-button-search'))).click() # Find a test center
    sleep(2)
    driver.find_element(By.CLASS_NAME, 'toggle-btn').click()
    jun_3 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[6]/div/div/div[3]/div/div[1]/div/div/div/div[4]/div/div/div/div[1]/div/div/div[3]/div/div[3]/div/div/div[4]/div[2]/div[1]').text # Save text
    print("{0}: {1}, Checked: {2}".format(test_date ,jun_3, ctime(time())))

previous = 0
def checkSchools(counter: str, test_date: str, driver):
    global previous
    Message = [f"{test_date}\nLast update: {ctime(time())}\n\n"]
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
            print(tgmessage.telegram_sendmessage(976908358, Message))
            print(tgmessage.telegram_sendmessage(5670908383, Message))
            print(tgmessage.telegram_sendmessage(584098198, Message))
            print(tgmessage.telegram_sendmessage(853226047, Message))
            print(tgmessage.telegram_sendmessage(1278150481, Message))
            print(tgmessage.telegram_sendmessage(809899348, Message))
            print(tgmessage.telegram_sendmessage(853226047, Message))
            print(tgmessage.telegram_sendmessage(716930078, Message))
            print("Email sent, sleeping...")
    previous = (int)(schoolcount.stripresult(jun_3))
    

op = WD.ChromeOptions()
#op.add_argument("--headless")
op.add_argument("--disable-browser-side-navigation")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-shm-usage")
PROXY="socks5://localhost:9050"
#op.add_argument(f"--proxy-server={PROXY}")
#op.add_argument("--user-data-dir='/root/.config/google-chrome/Profile 1'")
counter = 0
#logincreds = [[]] # logincreds[iterator][0] - email; logincreds[iterator][1]
iterator = 0
def main(test_date: str, email: str, password: str):
    print(f"Starting {test_date}")
    while 1:
        try:
            driver = WD.Chrome(options=op)
            print(f"{test_date} Logging in")
            loginMySAT(driver=driver, email=email, password=password)
            print(f"{test_date} Entering registration")
            satreg(driver=driver)
            print(f"{test_date} Choosing test date:")
            chooseTestDate(test_date, driver=driver)
            print(f"{test_date} Finding test centers")
            findtestcenter(test_date=test_date, driver=driver)
            checkSchools(schoolcount.stripresult(jun_3), test_date=test_date, driver=driver)
            while(1): # Infinite loop which breaks if an exception appears
                try:
                    refreshTestCenter(test_date=test_date,driver=driver)
                except:
                    break
                else:
                    checkSchools(counter=schoolcount.stripresult(jun_3), test_date=test_date, driver=driver)       
            #sleep(60)
            print(f"{test_date} Restarting the loop")
        except TimeoutException:
            print(TimeoutException)
            print(tgmessage.telegram_sendmessage(5670908383, f"{ctime(time())}, {TimeoutException}{test_date}"))
            trcbk = traceback.format_exc().replace('_', '\\_').replace('*', '\\*').replace('[','\\[').replace('`', '\\`')
            print(tgmessage.telegram_sendmessage(5670908383, f"{ctime(time())}, {test_date}\n```\n{trcbk}```"))
            driver.quit()
            continue
        except NoSuchWindowException:
            print("Killing application")
            break
        except:
            print(f"{test_date} Unknown error")
            print(tgmessage.telegram_sendmessage(5670908383, f"{ctime(time())}, {test_date} Error! Check server!"))
            print(traceback.format_exc())
            trcbk = traceback.format_exc().replace('_', '\\_').replace('*', '\\*').replace('[','\\[').replace('`', '\\`')
            print(tgmessage.telegram_sendmessage(5670908383, f"{ctime(time())}, {test_date}\n```\n{trcbk}```"))
            driver.quit()
            break

def testproxy():
    try:
        driver=WD.Chrome(options=op)
        driver.get("https://api.ipify.org/")
        sleep(60)
    except:
        sleep(60)
#aug = thrd.Thread(target=main, args=("AUG-26", "aasifov61@gmail.com", "Zz123456!"), name="august")
oct = thrd.Thread(target=main, args=("OCT-7", "supcollegeboard@gmail.com", "Zz123456!"), name="october")
#nov = thrd.Thread(target=main, args=("NOV-4", "gulamovkanan382@gmail.com", "Zz123456!"), name="november")
#dec = thrd.Thread(target=main, args=("DEC-2", "alirzaev997@gmail.com", "Zz123456!"), name="december")
#test = thrd.Thread(target=testproxy, args=())
#test.start()
#test.join()
#aug.start()
#aug.join()
oct.start()
oct.join()
#nov.start()
#dec.start()
