from lexer import generate

def shell():
    while True:
        text = input('oxide> ')
        if text == '.exit':
            break
        tokens = generate('<stdin>', text)
        if tokens[1]:
            print(tokens[1])
            continue
        print(tokens[0])

if __name__ == "__main__":
    shell()