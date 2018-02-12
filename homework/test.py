def func():
    prefix = "Good Morning"
    def func2(name):
        print(prefix, name)
    return func2
f = func()
f("henry")
f("tom")
print(dir(f))
print(f.__closure__)
print(type(f.__closure__[0]))
print(f.__closure__[0].cell_contents)
