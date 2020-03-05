多线程爬取搜狗的图片（threading,ajax,queue)

1、项目描述
下载1000张搜狗图片，时间限制在1min以内，因此采用多线程方式，节约时间。多线程有2种实现方式，一是派生thread子类，创建子类实例，二是创建threading实例。
2、技术难点
队列阻塞：block=False;      GIL锁：未上锁容易导致下载图片格式错误 ；       重定向较多;allow_redirects=False ；    
注意：url队列应当早于parse队列生成，否者还没出现请求线程时，解析线程就已经开始运行了。
3、技术实现
使用派生生成requets和parses多线程对象，生成url队列与respones队列，使用GIL下载图片保证图片格式正确。
