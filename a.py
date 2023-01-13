x = []

class A:
    def __init__(self, x):
        self.x = x
    
    def delete(self):
        x.remove(self)
        del self
    def __str__(self):
        return str(self.x)
x.append(A(1))
x.append(A(2))

x[0].delete()

for i in x:
    print(i)