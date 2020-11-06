from network import Client


if __name__ == '__main__':
    c = Client()
    print(c.requestServer((0, [0, 0, 0])))
