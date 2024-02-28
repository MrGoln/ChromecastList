import time
import csv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Нажатие нужных кнопок для network
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://animego.org/anime/istorii-ran-chast-1-zheleznaya-krov-909')
driver.execute_script("window.scrollTo(0, 1800)")
driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/button[2]').click()
driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[1]/button').click() # доп
driver.find_element(By.XPATH, '/html/body/nav/div[2]/div/div/ul/li[2]/span').click()# доп
driver.find_element(By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/span[2]/span').click() # доп
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[4]/div[2]').click() # доп
for i in driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[2]/select/option'):
    i.click()
    driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/iframe'))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[5]/a'))).click()
    time.sleep(8)
    driver.switch_to.window(driver.window_handles[0])

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
