import platform
from selenium import webdriver


GOOGLE_GRIVE_URL_PATTERN = "https://drive.google.com/"
MEGA_URL_PATTERN = "https://mega.nz/"

XPATH_G = "//*[contains(text(),'{}')]".format(GOOGLE_GRIVE_URL_PATTERN)
XPATH_M = "//*[contains(text(),'{}')]".format(MEGA_URL_PATTERN)

if platform.system() == 'Windows':
    chromedriver = 'chromedriver_win.exe'
elif platform.system() == 'Mac':
    chromedriver = 'chromedriver_mac'
elif platform.system() == 'Linux':
    chromedriver = 'chromedriver_linux'

# headless
option = webdriver.ChromeOptions()
option.add_argument('headless')

# login
driver = webdriver.Chrome('driver/'+ chromedriver, chrome_options=option)
driver.get('http://www.eyny.com/member.php?mod=logging&action=login')
driver.find_element_by_name('username').send_keys('ACCOUNT')
driver.find_element_by_name('password').send_keys('PASSWORD')
driver.find_element_by_name('loginsubmit').submit()


driver.get('http://www.eyny.com/thread-11855148-1-3DN3CFFH.html')


elements_g = driver.find_elements_by_xpath(XPATH_G)
elements_m = driver.find_elements_by_xpath(XPATH_M)

for ele in elements_g:
    if ele.get_attribute('href') is not None and GOOGLE_GRIVE_URL_PATTERN in ele.get_attribute('href'):
        print(ele.get_attribute('href'))
    elif GOOGLE_GRIVE_URL_PATTERN in ele.text:
        print(ele.text)

for ele in elements_m:
    if ele.get_attribute('href') is not None and MEGA_URL_PATTERN in ele.get_attribute('href'):
        print(ele.get_attribute('href'))
    elif MEGA_URL_PATTERN in ele.text:
        print(ele.text)
