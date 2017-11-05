"""
Provides the class Complex() to mimic the built-in complex class.
"""

class Complex():
    "Complex(real,[imag]) -> a complex number"

    def __init__(self,r=0,i=0):
        self.real = r
        self.imag = i

    def __abs__(self):
        "abs(self)"
        return (self.real**2 +self.imag**2)**0.5

    def __add__(self,value):
        "Return self+value."
        if hasattr(value,'imag'):
            return Complex(self.real+value.real,self.imag+value.imag)
        else:
            return Complex(self.real+value,self.imag)

    def __mul__(s,v):
        "Return s*v."
        if hasattr(v,'imag'):
            x = s.real * v.real - s.imag * v.imag
            y = s.real * v.imag + v.real * s.imag
            return Complex(x,y)
        else:
            return Complex(v*s.real,v*s.imag)

    def __rmul__(s,v):
        "Return s*v"
        if hasattr(v,'imag'):
            x = s.real * v.real - s.imag * v.imag
            y = s.real * v.imag + v.real * s.imag
            return Complex(x,y)
        else:
            return Complex(v*s.real,v*s.imag)

    def __radd__(self,value):
        "Return self+value"
        if hasattr(value,'imag'):
            return Complex(self.real+value.real,self.imag+value.imag)
        else:
            return Complex(self.real+value,self.imag)            

    def conjugate(self):
        return Complex(self.real,-self.imag)

    def __str__(self):
        if self.real==0:
            return "{}j".format(self.imag)
        else:
            sign="-" if self.imag<0 else "+"
            return "({}{}{}j)".format(self.real,sign,abs(self.imag))

    def __repr__(self):
        return str(self)

    def __pow__(self,value):
        "Return self ** value"
        raise NotImplementedError('not done yet')



def main():
    for x,y in [(0,0),(1,0),(0,1),(3,4),(1,-2),(7.8,-6.2)]:
        print('\nTesting ({},{})'.format(x,y))

        g = Complex() # ours
        h = complex() # builtin

        print(g,h)
        print(abs(g),abs(h))
        print(g.conjugate(),h.conjugate())
        print(g.real,h.real)
        print(g.imag,h.imag)

        w,y = h+1 , g+1
        print(w,y)
        w,y = 1+g , 1+h

        w,y = g * Complex(2,3), h * complex(2,3)
        print(w,y)

        w,y = g * 4, h * 4
        print(w,y) 


        w,y = 4 * g, 4 * h
        print(w,y)    

        w,y = g * g, h * h
        print(w,y)
        print(type(w),type(y))

        w,y = h * g, g * h
        print(w,y)
        print(type(w),type(y)) 


        w,y = 4j + g, 4j + h
        print(w,y)    


if __name__ == '__main__':
    main()