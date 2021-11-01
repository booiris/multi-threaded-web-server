import requests,threading

class RQ_get(threading.Thread):
    """docstring for RQ_get."""
    def __init__(self):
        super(RQ_get, self).__init__()

    def run(self):
        # self.start()
        rq = requests.get("http://192.168.91.1:9000/bigfile.zip")
        print(rq.content)
        print("OK")
        # print(rq.content.decode("utf8"))
        
l=[]
for r in range(100):
   l.append(RQ_get()) 

for r in l:
    r.start()
