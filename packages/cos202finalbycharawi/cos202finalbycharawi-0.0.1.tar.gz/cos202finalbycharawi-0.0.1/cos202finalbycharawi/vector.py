from point import *

class Vector(Point):
  def __init__(self, *x):
     super().__init__(*x)
  
  def euclideandistance(self,other):
        s = 0
        for i in range(len(self.x)):
          s += (self.x[i]-other.x[i])**2
        return s**0.5
  
  def lenght(self):
    s = 0
    for i in range(len(self.x)):
      s += (self.x[i])**2
    return s**0.5
  
  def unit(self):
    l = [i/self.lenght() for i in self.x]
    return Vector(l)
  
  def dotproduct(self,other):
    l = [self.x[i]*other.x[i] for i in range(len(self.x))]
    return sum(l)

  def crossproduct(self,other):
    if len(self.x)==3:
      return Vector(self.x[1]*other.x[2]-other.x[1]*self.x[2],self.x[2]*other.x[0]-other.x[2]*self.x[1],self.x[0]*other.x[1]-other.x[0]*self.x[1])
    else:
      raise Exception("Your vectors must be three-dimensional vectors")

  def __add__(self,other):
    l = [self.x[i]+other.x[i] for i in range(len(self.x))]
    return Vector(*l)

  def __sub__(self,other):
    l = [self.x[i]-other.x[i] for i in range(len(self.x))]
    return Vector(*l)

  def __truediv__(self,other):
    l = [self.x[i]/other.x[i] for i in range(len(self.x))]
    return Vector(*l)

  def __mul__(self,other):
    if isinstance(other,Vector):
        l = [self.x[i]*other.x[i] for i in range(len(self.x))]
    elif isinstance(other,int) or isinstance(other,float):
        l = [self.x[i]*other for i in range(len(self.x))]
    return Vector(*l)

  def __str__(self):
        p = ""
        for i in self.x:
            if i==self.x[-1]:
                s = str(i)
            else:
                s = str(i)+","
            p+=s
    
        return "<"+p+">"

if __name__=="__main__":
  v1 = Vector(1,2)
  v2 = Vector(3,4)
  print(v1)
  print(v2)
  v1.euclideandistance(v2)
  print(v1.lenght())
  print(v1.unit())
  print(v1.dotproduct(v2))
  #print(v1.crossproduct(v2))
  print(v1+v2)
  print(v1-v2)
  print(v1*v2)
  print(v1/v2)