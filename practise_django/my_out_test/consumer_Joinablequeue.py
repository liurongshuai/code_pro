from multiprocessing import JoinableQueue,Process
import time,random


# 生产者方法
def producer(name,food,q):
    for i in range(4):
        time.sleep(random.randint(1, 2))
        f = '%s生产的%s%s'%(name,food,i)
        q.put(f)
        print(f)
    q.join()  # 一直阻塞，等待消耗完所有的数据后才释放


# 消费者方法
def consumer(name,q):
    while True:
        food = q.get()
        print('\033[31m%s消费了%s\033[0m' % (name, food))
        time.sleep(random.randint(4,8))
        q.task_done() # 每次消耗减1


if __name__ == '__main__':
    q = JoinableQueue()  # 创建队列
    # 模拟生产者队列
    p1 = Process(target=producer,args=('p1','包子',q))
    p1.start()
    p2 = Process(target=producer,args=('p2','烧饼',q))
    p2.start()

    # 模拟消费者队列
    c1 = Process(target=consumer,args=('c1',q))
    c1.daemon = True # 守护进程：主进程结束，子进程也会结束
    c1.start()
    c2 = Process(target=consumer,args=('c2',q))
    c2.daemon = True
    c2.start()

    p1.join() # 阻塞主进程，等到p1子进程结束才往下执行
    p2.join()

    # q.task_done() 每次消耗队列中的 任务数减1
    # q.join() 一直阻塞，等待队列中的任务数消耗完才释放
    # 因为有 q.join 所有一直会等待 c1,c2 消耗完毕。才会执行 p.join 后面的代码
    # 因为 c1 c2 是守护进程，所以到这一步主进程代码执行完毕，主进程会释放死掉，
    # 所以 c1 c2 也会跟随 主进程释放死掉。

"""
使用JoinableQueue组件，是因为JoinableQueue中有两个方法：task_done()和join() 。首先说join()和Process中的join()的效果类似，
都是阻塞当前进程，防止当前进程结束。但是JoinableQueue的join()是和task_down()配合使用的。
  Process中的join()是等到子进程中的代码执行完毕，就会执行主进程join()下面的代码。而JoinableQueue中的join()是等到队列中的任务
数量为0的时候才会执行q.join()下面的代码，否则会一直阻塞。
  task_down()方法是每获取一次队列中的任务，就需要执行一次。直到队列中的任务数为0的时候，就会执行JoinableQueue的join()后面的
方法了。所以生产者生产完所有的数据后，会一直阻塞着。不让p1和p2进程结束。等到消费者get()一次数据，就会执行一次task_down()方法
，从而队列中的任务数量减1,当数量为0后，执行JoinableQueue的join()后面代码,从而p1和p2进程结束。
  因为p1和p2添加了join()方法，所以当子进程中的consumer方法执行完后，才会往下执行。从而主进程结束。因为这里把消费者进程c1和c2 
设置成了守护进程，主进程结束的同时，c1和c2 进程也会随之结束，进程都结束了。所以消费者consumer方法也会结束。

作者：丘山Ivan
链接：https://www.jianshu.com/p/2d3e6a21f6fe
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""