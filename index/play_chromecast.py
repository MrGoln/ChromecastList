import csv
import pychromecast
import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


# Загрузка ссылок
def load_videos():
    with open('videos_new.csv', newline='') as File:
        reader = csv.reader(File)
        videos_url = []
        for row in reader:
            videos_url.append(row)
        return videos_url


# Воспроизведения видео на тв
def play_chromecast(url):
    # List chromecasts on the network, but don't connect
    services, browser = pychromecast.discovery.discover_chromecasts()

    # Shut down discovery
    pychromecast.discovery.stop_discovery(browser)

    # Discover and connect to chromecasts named Living Room
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["B866"])
    #print(chromecasts)
    # print([cc.device.friendly_name for cc in chromecasts])

    cast = chromecasts[0]
    # Start worker thread and wait for cast device to be ready
    cast.wait()
    #print(cast.status)

    mc = cast.media_controller
    mc.play_media(url, 'video/mp4')
    mc.block_until_active()
    # print(mc.status)

    mc.pause()
    time.sleep(5)
    mc.play()

    # Shut down discovery
    pychromecast.discovery.stop_discovery(browser)


# Проверка перехода на следующее или предыдущие
def status_volume_video():
    try:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["B866"])
        print(chromecasts)
        cast = chromecasts[0]
        cast.wait()
        print(cast.status.volume_level) # проверка
        return cast.status.volume_level
    except:
        return None


# Основной код
def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('192.168.0.250', 8000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()


cnt_select = 103  # Видео с которого стартовать
cnt_select -= 1  # так как начинается с нуля

class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""
    videos_url = load_videos()
    play_chromecast(videos_url[cnt_select][0])  # Первый запуск
    print('start')

    def do_POST(self):
        global cnt_select
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('POST request received'.encode('utf-8'))
        self.videos_url = load_videos()

        #print(post_data)

        #print(self.headers.items())
        if 'next' == post_data:
            if not (cnt_select + 1 > len(self.videos_url)):
                cnt_select += 1
                print(cnt_select + 1)
                play_chromecast(self.videos_url[cnt_select][0])
                print('Переход вперёд')
        elif 'preview' == post_data:
            if not (cnt_select - 1 < 0):
                cnt_select -= 1
                print(cnt_select + 1)
                play_chromecast(self.videos_url[cnt_select][0])
                print('Переход назад')

run(handler_class=HttpGetHandler)
