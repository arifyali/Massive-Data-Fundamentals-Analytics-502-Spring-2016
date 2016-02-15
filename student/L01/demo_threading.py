import threading,time

class CountingThread(threading.Thread):
    def __init__(self,name,high):
        super(CountingThread,self).__init__()
        self.name = name
        self.high = high
        self.count = 0

    def run(self):
        for i in range(0,self.high):
            print("{}: {}".format(self.name,i))
            time.sleep(.5)
            self.count += 1

if __name__=="__main__":
    foo = CountingThread("foo",5)
    foo.start()
    bar = CountingThread("bar",5)
    bar.start()
    foo.join()                  # Waits for completion
    bar.join()
    print("foo.count:{}  bar.count:{}".format(foo.count,bar.count))
