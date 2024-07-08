

l = ["b'", '14']

l[0] = l[0].replace("b'", "")

if not l[0]:
    del l[0]
    
print(l)