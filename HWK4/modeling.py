# Copyright 2017 Chuan Xing Zheng czheng78@bu.edu
# U32336445
# HWK4
#!/usr/bin/python


class Polynomial():

    def __init__(self, coeff={}):
        exp = len(coeff) - 1
        result = {}
        for i in coeff:
            if (i != 0):
                result[exp] = i
            exp -= 1
        self.coeff = result

    def exponents(self):
        return self.coeff.keys()

    def __getitem__(self, key):
        try:
            return self.coeff[key]
        except KeyError:
            return 0

    def __setitem__(self, key, new_coeff):
        self.coeff[key] = new_coeff

    def __delitem__(self, key):
        del self.coeff[key]

    def __str__(self):
        x = ""
        for i in reversed(sorted(self.exponents())):
            if (self[i] != 0):
                if len(x) > 0:
                    x = x + " + "
                x = x + str(self[i]) + "x^" + str(i)

        return x

    def __add__(self, B):
        c = Polynomial([])
        for i in list(self.exponents()):
            if i in list(B.exponents()):
                c[i] = B[i] + self[i]
            else:
                c[i] = self[i]
        for j in list(B.exponents()):
            if j in list(self.exponents()):
                c[j] = self[j] + B[j]
            else:
                c[j] = B[j]
        return c

    def __sub__(self, a):
        c = Polynomial([])
        c = self
        for k in a.exponents():
            if k in self.exponents():
                c[k] = self.coeff[k] - a[k]
            else:
                c[k] = -a[k]

        return c

    def __mul__(self, a):
        result = Polynomial([])
        for exp1 in self.exponents():
            for exp2 in a.exponents():
                c = exp1 + exp2
                b = self[exp1] * a[exp2]
                try:
                    result[c] += b
                except KeyError:
                    result[c] = b
        return result

    def __eq__(self, a):
        if len(self.coeff) != len(a.coeff):
            return False
        for i in self.coeff:
            if self[i] != a[i]:
                return False

        return True

    def deriv(self):
        c = Polynomial([])
        for i in list(self.coeff):
            if i == 0:
                pass
            else:
                c[i - 1] = self[i] * i

        return c

    def eval(self, x):
        c = 0.0
        for i in reversed(sorted(self.exponents())):
            c += self[i] * x**i
        return c
