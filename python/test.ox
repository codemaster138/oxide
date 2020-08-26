var x = 7

func test(b, foo, bar, baz) {
    x = b ** 2
    x = x + 1
    return b + 2
}

print("x before operation:", x)
print("result:\ ", test(5))
print("x after operation:", x)
var name = input("type your name: ")
print("hi", name)