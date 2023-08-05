'''
Error notes: 
- TypeError: cannot pickle '_thread.lock' object
- thread locked object is self
- works in simple example below


'''


import pickle
import queue


class A:
    def __init__(self):
        self.val_a = 1


class B(A):
    def __init__(self):
        self.val_b = 2
        self.queue = queue.PriorityQueue()
        super().__init__()

class C(B):
    def __init__(self):
        self.val_c = 3
        super().__init__()

    def persist(self):
        for i in range(3):
            self.queue.put((i, 2))
        self.queue = list(self.queue.queue)
        pickle.dump(self, open('demo.pkl', 'wb'))


c = C()
c.persist()
