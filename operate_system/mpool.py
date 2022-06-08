# -*- encoding=utf-8 -*-


from time import sleep
import psutil
import threading

from mtask import Task,AsyncTask
from mqueue import ThreadSafeQueue



class TaskTypeErrorException(Exception):
    pass

#任务处理线程
class ProcessThread(threading.Thread):

    def __init__(self,task_queue, *args, **kwargs):
        # 父类的构造函数
        threading.Thread.__init__(self, *args, **kwargs)
        # 线程停止的标记， 常用的标记，例如Go里也有dismiss
        self.dismiss_flag = threading.Event()
        # 任务队列（处理线程不断从队列中取出任务处理）
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        while True:
            # 判断线程是否被要求停止
            if self.dismiss_flag.is_set():
                break
            
            task = self.task_queue.pop()
            if not isinstance(task,Task):
                continue
            
            #执行task实际逻辑（通过函数调用引进）
            result = task.callable(*task.args,**task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)
            
    def dismiss(self):
        self.dismiss_flag.set()
        
    def stop(self):
        self.dismiss()
        
        
class ThreadPool:
    def __init__(self,size=0):
        if not size:
            # 约定线程池的大小为CPU核数的两倍（最佳实践）
            size = psutil.cpu_count() *2
            print('poolSize: %d' % size)
        # 线程池
        self.pool = ThreadSafeQueue(size)
        # 任务队列
        self.task_queue = ThreadSafeQueue()
        
        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))
            
    # 线程池大小
    def size(self):
        return self.pool.size()
    
    # 启动线程池
    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            print('mpool start thread: %d' % i)
            thread.start()
            

    # 停止线程池
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size() >0:
            thread = self.pool.pop()
            thread.join()
    
    # 向线程池提交任务
    def put(self,item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        
        self.task_queue.put(item)

    # 批量提交任务
    def batch_put(self):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)
    
    


    