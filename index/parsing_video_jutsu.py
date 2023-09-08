import csv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Нажатие нужных кнопок для network
chrome_options = Options()
chrome_options.add_argument("--headless")  # Включение режима без головы
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

with open('videos_new.csv', 'r') as file:
    lines = file.readlines()

redact_serias = 1 # выбрать с какой серии начать запись в csv
with open('videos_new.csv', 'w') as file:
    file.writelines(lines[:redact_serias - 1])

url_videos = []
for i in range(redact_serias, 153):
    driver.get(f'https://jut.su/dragonball/season-2/episode-{i}.html')
    with open('videos_new.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[2]/div/div[4]/div/div[1]/div[1]/div/video/source[1]').get_attribute('src')])

