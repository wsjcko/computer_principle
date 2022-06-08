# -*- encoding=utf-8 -*-

import time
import threading


class ThreadSafeQueueException(Exception):
    pass

# 线程安全的队列
class ThreadSafeQueue(object):
    def __init__(self, max_size=0):
        self.queue =[]
        self.max_size = max_size
        self.lock = threading.Lock()
        self.condition = threading.Condition()

    # 当前队列的元素的数量
    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    #往队列里面加入元素
    def put(self, item):
        if self.max_size!=0 and self.size() >self.max_size:
            return ThreadSafeQueueException()
        
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        # 通知 原先queue.size() =0时，取元素阻塞的线程
        self.condition.notify() 
        self.condition.release()
        

    def batch_put(self, item_list):
        # 判断不是列表，先转换为列表
        if not isinstance(item_list,list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    # 从队列取出元素
    # block: 当队列中没有元素，我们是否要阻塞等待
    # timeout: 我们要等待，需要等待多久
    def pop(self, block=False, timeout=0):
        if self.size()==0:
            # 需要阻塞等待
            if block:
                self.condition.acquire()
                self.condition.wait(timeout)
                self.condition.release()
            else:
                return None
        # 等待timeout时间后，还是没有取到值,
        # 需要和 pop 同时加锁判断，否则有可能当时判,队列元素不为空，再次加锁取出就有问题
        # if self.size()==0:
        #     return None
        item = None
        self.lock.acquire()
        if len(self.queue)>0:
            item = self.queue.pop()
        self.lock.release()
        return item

    def get(self,index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item

if __name__ == '__main__':
    queue = ThreadSafeQueue(max_size=100)
    def producer():
        while True:
            queue.put(1)
            time.sleep(3)
    
    def consumer():
        while True:
            item = queue.pop(block=True,timeout=2)
            print('get item from queue: %d',item)
            time.sleep(1)

    thread1= threading.Thread(target=producer)
    thread2 = threading.Thread(target=consumer)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()