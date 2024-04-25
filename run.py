import multiprocessing


def func1():
    print("start main code")
    import main


def func2():
    print("start schedule newsletter")
    import test2
    

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=func1)
    p2 = multiprocessing.Process(target=func2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
