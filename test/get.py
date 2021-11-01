import requests,threading

class RQ_get(threading.Thread):
    """docstring for RQ_get."""
    def __init__(self):
        super(RQ_get, self).__init__()

    def run(self):
        try:
            rq = requests.get("http://192.168.91.1:9000/index.html")
            print(rq.headers)
            print(rq.content.decode("utf8"))
        except:
            print("提前关闭了链接，因为要释放")
        # print(rq.content.decode("utf8"))

class RQ_head(threading.Thread):
    """docstring for RQ_head."""
    def __init__(self, ):
        super(RQ_head, self).__init__()
    def run(self):
        try:
            rq = requests.head("http://192.168.91.1:9000/index.html")
            print(rq.headers)
            print(rq.content.decode("utf8"))
        except:
            print("提前关闭了链接，因为要释放")


class RQ_post(threading.Thread):
    """docstring for RQ_head."""

    def __init__(self,a=2,b=3):
        super(RQ_post, self).__init__()
        self.a=str(a)
        self.b=str(b)

    def run(self):
        try:
            rq = requests.post("http://192.168.91.1:9000/cgi-bin/cal.py",
                               data="a={a}&b={b}".format(a=self.a, b=self.b))
            print(rq.headers)
            print(rq.content.decode("utf8"))
        except:
            print("提前关闭了链接，因为要释放")
        
l=[]
for r in range(1):
#    l.append(RQ_post(3,4)) 
#    l.append(RQ_get()) 
   l.append(RQ_head()) 

for r in l:
    r.start()
