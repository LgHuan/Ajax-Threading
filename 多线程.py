import requests
import threading
from queue import Queue

header={
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
}
url='https://pic.sogou.com/pics?query=%B0%AE%D0%C4%CD%BC%C6%AC&st=255&mode=255&start={start}&reqType=ajax&reqFrom=result&tn=0'
page=48

def url_queue():
    url_queue = Queue()
    for i in range(20,50):
        url_queue.put(url.format(start=page * i))
    return url_queue

class Mythreads(threading.Thread):
    def __init__(self,thread_name,url_queue):
        super().__init__(name=thread_name)
        self.url_queue=url_queue
    def run(self):
        print('当前线程',threading.current_thread())
        while not self.url_queue.empty():
            response=get_request(self.url_queue.get(block=False))
            get_parse(response)

def get_request(url):
    response = requests.get(url, headers=header)
    return response.json()
def get_img_request(url):
    response=requests.get(url,headers=header)
    return response.content
def get_parse(response):
    datas = response['items']
    num=0
    for data in datas:
        name=data['title']
        img_url=data['ori_pic_url']
        img=get_img_request(img_url)
        get_save(name,img)
        num+=1
        print(num)
def get_save(name,data):
    #为防止写入数据正确，对写入上锁
    lock=threading.Lock()
    lock.acquire()
    with open('.//图片//{}.jpg'.format(name), 'wb')as f:
        f.write(data)
    lock.release()


url_queue=url_queue()
for i in range(9):
    thread=Mythreads(i,url_queue)
    thread.start()








