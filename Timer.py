import time

class Timer(object):
    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        # Error handling here
        self.__finish = time.time()

    def duration_in_seconds(self):
        if hasattr(self, '__start'):
            return self.__finish - self.__start
        else:
            return "Timer was not started"
