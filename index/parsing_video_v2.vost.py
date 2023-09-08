import time
import csv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Нажатие нужных кнопок для network
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

driver.get('https://v2.vost.pw/tip/tv/1444-dragon-ball-z1.html')
driver.execute_script("window.scrollTo(0, 1800)")


with open('videos_new.csv', 'r') as file:
    lines = file.readlines()


redact_serias = 1 # выбрать с какой серии начать запись в csv
with open('videos_new.csv', 'w') as file:
    file.writelines(lines[:redact_serias - 1])


for i in driver.find_elements(By.XPATH, '/html/body/div/div[3]/div[2]/div[2]/div[1]/div[3]/span/div[1]/div/div/div'):
    i.click()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div/div[3]/div[2]/div[2]/div[1]/div[3]/span/div[2]/div/iframe'))

    with open('videos_new.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([driver.find_element(By.XPATH, '/html/body/div[1]/pjsdiv/pjsdiv[1]/video').get_attribute('src')])
        driver.switch_to.default_content()
