def foo(a):
    a.update({'a': 1})
    print(a)

a = {}
foo(a)
print(a)