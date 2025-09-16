import threading


class Builder(threading.Thread):
    def __init__(self,function,result_queue = None,args=None):
        threading.Thread.__init__(self)
        self.args = args if args is not None else {}
        self.function = function
        self.result_queue = result_queue
        self.start()

    
    def run(self):

        if(self.result_queue==None):
            self.function(**self.args)
        else:
            result = self.function(**self.args)
            self.result_queue.put(result)



