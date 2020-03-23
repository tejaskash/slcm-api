from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

#WINDOW_SIZE = "1920,1080"
#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
#chrome_options.add_argument('--no-sandbox')
#driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="/usr/bin/chromedriver")

def getDetails(username=None,password=None):
    AttendanceHTML = None
    MarksHTML = None
    chrome_options = Options()
    #chrome_options.add_argument('--window-size=800,800')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    #Open SLCM Website
    driver = webdriver.Chrome("/usr/bin/chromedriver",chrome_options=chrome_options,service_log_path="./chrome.log")
    driver.get("https://slcm.manipal.edu")
    element = None

    #Enter Username and Password and Login
    try:
        element = driver.find_element_by_id("txtUserid")
    except:
        print("Internet Conncetion Error")
        driver.close()
        return None,None

    element.send_keys(username)
    element = driver.find_element_by_id("txtpassword")
    element.send_keys(password)
    element = driver.find_element_by_id("btnLogin")
    element.click()
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'rtpchkMenu_lnkbtn2_1')))
    except:
        print("Invalid Username/Password")
        driver.close()
        return None,None
    print ("Logged In")
    element.click()
    WebDriverWait(driver, 5)

    #Find Attendance Table 
    driver.find_element_by_xpath('//a[@href="#3"]').click();
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tblAttendancePercentage')))
    AttendanceHTML = element.get_attribute('outerHTML')
    #print(outer)

    #Find Internal Mark Table
    driver.find_element_by_xpath('//a[@href="#4"]').click()
    element = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,'PrintInternal')))
    MarksHTML = element.get_attribute('outerHTML')
    #print(marks)
    #Logout of SLCM and close chromewebdriver
    driver.get("https://slcm.manipal.edu/loginForm.aspx")
    driver.close()
    return AttendanceHTML,MarksHTML

if __name__ == "__main__":
    AttendanceHTML,MarksHTML = getDetails("username","password")
    print(AttendanceHTML)
    print(MarksHTML)