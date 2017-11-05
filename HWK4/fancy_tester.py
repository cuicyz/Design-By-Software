from model_complex import Complex

def test_complex_type_class(f):
    "try out features of complex classes."
    c = f(3,4)
    d = 4 + 3j
    e = 2 + 5j
    print("c d e",c,d,e)
    print("imag c",c.imag)
    print("real c",c.real)
    print("c*d",c*d)
    print("abs(c)",abs(c))
    print("c+d",c+d)
    print("c*e*d",c*e*d)


if __name__ == '__main__':
    test_complex_type_class(complex)
    test_complex_type_class(Complex)