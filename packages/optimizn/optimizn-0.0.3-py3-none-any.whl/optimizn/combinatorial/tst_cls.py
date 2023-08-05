class A():
    def __init__(self):
        self.val1 = 1
        print('A:', self.__class__.__name__)

class B(A):
    def __init__(self):
        self.val2 = 2
        print('B:', self.__class__.__name__)
        super().__init__()

class C(B): 
    def __init__(self):
        self.val3 = 3
        print('C:', self.__class__.__name__)
        super().__init__()

b = B()
print()
c = C()
print(isinstance(c, B))