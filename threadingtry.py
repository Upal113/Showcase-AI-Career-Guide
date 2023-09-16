from threading import Thread
from time import sleep

def threaded_function(arg):
    for i in range(arg):
        print("running")
        sleep(1)
        print("Complete")


if __name__ == "__main__":
    thread = Thread(target = threaded_function, args = (10, ))
    thread.start()
    thread.join()
    print("thread finished...exiting")