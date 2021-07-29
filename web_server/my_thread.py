from threading import Thread


class MyThread(Thread):
    def __init__(self, name, func_to_run):
        Thread.__init__(self)
        self.name = name
        self.func_to_run = func_to_run

    def run(self):
        print(str(self.name) + " thread is running")
        self.func_to_run()


class MyAsyncThread(Thread):
    def __init__(self, name, func_to_run):
        Thread.__init__(self)
        self.name = name
        self.func_to_run = func_to_run

    def run(self):
        print(str(self.name) + " thread is running")
        self.func_to_run()