import requests,threading

class RQ_get(threading.Thread):
    """docstring for RQ_get."""
    def __init__(self):
        super(RQ_get, self).__init__()

    def run(self):
        # self.start()
        # for i in range(10):
        try:
            rq = requests.get("http://192.168.91.1:9000/bigfile.zip")
            # print(rq.content)
            print("OK")
        except:
            print("提前关闭了链接，因为要释放")
        # print(rq.content.decode("utf8"))
        
l=[]
for r in range(100):
   l.append(RQ_get()) 

for r in l:
    r.start()
