from multiprocessing import Process, Queue  # 多进程组件,队列
import time, random


# 生产者方法
def producer(name, food, q):
    for i in range(4):
        time.sleep(random.randint(1, 3))  # 模拟获取数据时间
        f = '%s生产的%s%s' % (name, food, i)
        print(f)
        q.put(f)  # 添加进队列


# 消费者方法
def consumer(q, name):
    while True:
        food = q.get()  # 如果获取不到，会一直阻塞进程不会结束子进程
        # 当队列中的数据是None的时候结束while循环
        if food is None:
            print('%s获取到一个空' % name)
            break
        f = '\033[31m%s消费了%s\033[0m' % (name, food)
        print(f)
        time.sleep(random.randint(1, 3))  # 模拟消耗数据时间


if __name__ == '__main__':
    q = Queue()  # 创建队列

    # 模拟生产者 生产数据
    p = Process(target=producer, args=('p', '包子', q))  # 创建进程
    p.start()  # 启动进程
    p1 = Process(target=producer, args=('p1', '烧饼', q))
    p1.start()

    # 模拟消费者消费数据
    c = Process(target=consumer, args=(q, 'c'))
    c.start()
    c1 = Process(target=consumer, args=(q, 'c1'))
    c1.start()

    p.join()  # 阻塞主进程 直到p和p1 子进程结束后才执行q.put() 方法
    p1.join()  # 阻塞主进程 直到p和p1 子进程结束后才执行q.put() 方法

    # 为了确保生产者生产完所有数据后，
    # 最后一个是None,方便结束子进程中的while循环,
    # 否则会一直等待队列中加入新数据。
    q.put(None)
    q.put(None)









