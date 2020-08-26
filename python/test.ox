var x = 7

func test(b) {
    x = b ** 2
    x = x + 1
    return b + 2
}

print(x)
print(test(5))
print(x)