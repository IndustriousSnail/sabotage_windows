import os

if __name__ == '__main__':
    try:
        pid = str(os.getpid()) + "\n"
        f = open('pid.txt', 'a+')
        f.write(pid)
        f.close()
        while True:
            a = 1 + 1
    except KeyboardInterrupt:
        exit(1)
