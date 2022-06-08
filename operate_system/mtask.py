# -*- encoding=utf-8 -*-

import uuid
import threading


class Task:
    def __init__(self,func, *args, **kwargs):
        #任务具体逻辑，自定义函数（函数引用传递进来）
        self.callable = func
        self.id = uuid.uuid4()
        self.args = args
        self.kwargs = kwargs
        
    def __str__(self):
        return 'Task id: ' +str(self.id)
    



# 异步任务对象,继承基本Task
class AsyncTask(Task):

    def __init__(self, func, *args, **kwargs):
        self.result = None
        self.condition = threading.Condition()
        # 调用父类Task的构造函数
        super().__init__(func, *args, **kwargs)

    # 设置运行结果
    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    # 获取任务结果
    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result



def test_function():
    print('this is a task test.')
    
if __name__ == '__main__':
    task = Task(func=test_function)
    # Task id: ec308339-9671-45c4-8678-478c95563ca2
    print(task)