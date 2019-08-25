def test(a,b,c):
    if a != 0:
        print("a")
    if b != 0:
        print("b")
    if c != 0:
        print("c")
    if a != 0 and b != 0:
        print("ab")
        if c == 0:
            return "abc"


print(test(1,2,0))
