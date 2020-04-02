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


"""
使用Queue组件实现的缺点就是，实现了多少个消费者consumer进程，就需要在最后往队列中添加多少个None标识，方便生产完毕结束消费者
consumer进程。否则，p.get() 不到任务会阻塞子进程，因为while循环，直到队列q中有新的任务加进来，才会再次执行。而我们的生产者只
能生产这么多东西，所以相当于程序卡死

作者：丘山Ivan
链接：https://www.jianshu.com/p/2d3e6a21f6fe
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""






