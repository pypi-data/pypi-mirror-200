from abc import ABC,abstractproperty,abstractmethod

class Point(ABC):
    def __init__(self,*x):
        self.x = x

    @abstractmethod
    def euclideandistance(self,other):
        s = 0
        for i in range(len(self.x)):
            s += (self.x[i]-other.x[i])**2
        return s**0.5
    
    def __str__(self):
        p = ""
        for i in self.x:
            if i==self.x[-1]:
                s = str(i)
            else:
                s = str(i)+","
            p+=s
    
        return "("+p+")"

    def P1P2(self,P1,P2):
        l = [P1.x[i]-P2.x[i] for i in range(len(P1.x))]
        return l