import multiprocessing,os

def worker(val):
    return "worker {} PID {}".format(val,os.getpid())

if __name__=="__main__":
    pool = multiprocessing.Pool(processes=4)
    result = pool.map(worker,range(0,16))
    print(result)

    
