import time
import requests
import threading
from queue import Queue

header={
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
}
url='https://pic.sogou.com/pics?query=%B0%AE%D0%C4%CD%BC%C6%AC&st=255&mode=255&start={start}&reqType=ajax&reqFrom=result&tn=0'
page=48
response_queue=Queue()
#url存入队列中
def url_queue():
    url_queue = Queue()
    for i in range(1,3):
        url_queue.put(url.format(start=page * i))
    return url_queue
#派生多线程类
class Mythreads(threading.Thread):
    def __init__(self,url_queue,thread_name):
        threading.Thread.__init__(self,name=thread_name)
        self.url_queue=url_queue

    def run(self):
        print('当前线程',threading.current_thread())
        while not self.url_queue.empty():
            response=get_request(self.url_queue.get(block=False))
            #get_parse(response)
            get_response_queue(response)

def get_response_queue(response):
    response_queue.put(response)

class parse_Threads(threading.Thread):
    def __init__(self,threading_name,response_queue):
        threading.Thread.__init__(self,name=threading_name)
        self.response=response_queue
    def run(self):
        print('当前parse线程',threading.current_thread())
        while not self.response.empty():
            get_parse(self.response.get(block=False))

def get_request(url):
    response = requests.get(url, headers=header)
    return response.json()
def get_img_request(url):
    response=requests.get(url,headers=header,allow_redirects=False)
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
        print(num)#体现多线程
def get_save(name,data):
    #为防止写入数据正确，对写入上锁
    lock=threading.Lock()
    lock.acquire()
    with open('./图片/{}.jpg'.format(name), 'wb')as f:
        f.write(data)
    lock.release()

url_queue=url_queue()
threads=[]
re_threads=[]

time.sleep(2)
for i in range(2):
    thread=Mythreads(url_queue,i)
    threads.append(thread)
    thread.start()

threads[0].join()#保证有一个线程执行完毕，这样不仅保证response队列不为空，还可以节约时间
'''
# 不需要循环保证所有线程执行完毕，浪费时间
for thread in threads:
    thread.join()
'''
for i in range(2):
    re_thread=parse_Threads(i,response_queue)
    re_thread.start()
    re_threads.append(re_thread)








