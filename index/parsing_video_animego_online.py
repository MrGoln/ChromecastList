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

driver.get('https://animego.online/571-drakonij-zhemchug-zet-c1.html')
driver.execute_script("window.scrollTo(0, 1800)")

#driver.find_element(By.XPATH, '/html/body/div[1]/div/main/article/div[3]/div[6]/div[2]/iframe').click() # Клик по запуску

driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div[1]/div/main/article/div[3]/div[6]/div[2]/iframe'))
driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/iframe'))
driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div/iframe'))
driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[4]/div[2]/span').click()
driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[4]/div[1]/div/div[2]').click()
flag = True
for i in range(1, 5):
    if flag:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]').click()
        flag = False
    else:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]').click()
    driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div[1]/div[1]/div[2]/div[{i}]').click()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/a').click()


# Вытаскивание всех запросов network
url_videos = []
for request in driver.requests:
    if request.response:
        if 'https://cloud.kodik-storage.com/useruploads/' in str(request.url):
            request_video = str(request.url).replace(':hls:manifest.m3u8', '')
            if '720.mp4' in request_video:
                url_videos.append(request_video)
            elif '480.mp4' in request_video:
                url_videos.append(request_video.replace('480.mp4', '720.mp4'))
            elif '360.mp4' in request_video:
                url_videos.append(request_video.replace('360.mp4', '720.mp4'))
            print(request_video)

# Записывание всех запросов network
with open('videos_new.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for l in url_videos:
        spamwriter.writerow([l])
