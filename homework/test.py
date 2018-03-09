class G(object):
    def show(self):
        print("I am G")

class F(G):
    def show(self):
        print("I am F")

class E(G):
    def show(self):
        print("I am E")

class D(G):
    def show(self):
        print("I am D")

class C(F):
    def show(self):
        print("I am C")

class B(E):
    def show(self):
        print("I am B")

class A(B, C ,D):
    pass

print(A.mro())