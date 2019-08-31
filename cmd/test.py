def test(a):
    a = 'b'
    print("test" + a)

def returnStr():
    return "r"

result = returnStr()
test(result)

print(result)
