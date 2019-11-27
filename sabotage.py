import getopt
import os
import sys
import threading
import time
import psutil
import socket

cpu_status = []
memory_status = []
disk_status = []


class MockCpu(threading.Thread):
    min_cpu = 50
    max_cpu = 60

    def avg(self, cpu_list):
        return sum(cpu_list) / len(cpu_list)

    def run(self):
        f = open("pid.txt", "w+")
        f.write("")
        f.close()
        while True:
            cpu_list = psutil.cpu_percent(interval=1, percpu=True)  # 获取cpu利用率
            cpu_avg = self.avg(cpu_list)  # 计算cpu平均利用率
            cpu_status.clear()
            cpu_status.append("当前所有核CPU利用率为：" + str(cpu_list))
            cpu_status.append("平均CPU利用率为：" + str(cpu_avg))

            f = open("pid.txt", "r")
            thread_list = f.readlines()
            f.close()

            if cpu_avg < self.min_cpu:
                # 启动一个死循环
                os.popen("python while.py")
            elif len(thread_list) > 0 and cpu_avg > self.max_cpu:
                # 关闭一个死循环
                pid = thread_list[0].strip()
                os.system("taskkill /PID %s /F > log.txt" % pid)
                thread_list.remove(thread_list[0])
                f = open("pid.txt", "w")
                f.writelines(thread_list)
                f.close()

            time.sleep(1)


class MockMemory(threading.Thread):
    min_memory = 60
    max_memory = 70
    memory_list = []

    def run(self):
        while True:
            virtual_memory = psutil.virtual_memory()
            used_memory = virtual_memory.used / 1024 / 1024 / 1024
            free_memory = virtual_memory.free / 1024 / 1024 / 1024
            memory_percent = virtual_memory.percent
            memory_info = "内存使用：%0.2fG，使用率%0.1f%%，剩余内存：%0.2fG" % (used_memory, memory_percent, free_memory)
            memory_status.clear()
            memory_status.append(memory_info)
            if memory_percent < self.min_memory:
                self.memory_list.append([0 for i in range(1024 * 1024 * 300)])
            elif memory_percent > self.max_memory:
                self.memory_list.pop()

            time.sleep(0.5)


# todo
def mockNetwork():
    # net_send = (psutil.net_io_counters().bytes_sent) / 1024 / 1024
    # print(net_send)
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect(("172.18.63.113", port))
    s.send(bytes(1024 * 1024 * 50))
    while len(s.recv(1024)) <= 0:
        break
    s.close()


class MockDiskOutput(threading.Thread):
    write_speed = 50

    def run(self):
        while True:
            f = open('temp.txt', 'a+')
            for i in range(1000):
                f.write('0' * 1024 * self.write_speed)
                time.sleep(0.001)
                if int(time.time()) % 10 == 0:
                    f.truncate()  # 每10s清空一次文件
            f.close()


def mockDiskInput():
    # 先准备一个G的数据
    # f = open('readTemp0.txt', 'w')
    # f.write('0' * 1024 * 1024 * 1024)
    # f.close()
    #
    # f = open('readTemp1.txt', 'w')
    # f.write('0' * 1024 * 1024 * 1024)
    # f.close()

    read_speed = 10  # 10M
    index = 1
    while True:
        f = open('readTemp%s.txt' % index, 'r')
        for i in range(1000):
            data = f.read(1024 * read_speed)
            print(len(data))
            time.sleep(0.001)
            if len(data) <= 0:
                index = (index + 1) % 2
                break
        f.close()


class GetDiskStatus(threading.Thread):

    def run(self):
        tmp_disk_info = psutil.disk_io_counters()
        old_write_bytes = tmp_disk_info.write_bytes
        old_read_bytes = tmp_disk_info.read_bytes
        while True:
            disk_io_info = psutil.disk_io_counters()
            diff_write_bytes = disk_io_info.write_bytes - old_write_bytes
            diff_read_bytes = disk_io_info.read_bytes - old_read_bytes
            disk_status.clear()
            if diff_write_bytes < 1024:
                disk_status.append("当前磁盘写入速度：%s B/s" % diff_write_bytes)
            elif 1024 <= diff_write_bytes <= 1024 * 1024:
                disk_status.append("当前磁盘写入速度：%s KB/s" % (diff_write_bytes / 1024))
            else:
                disk_status.append("当前磁盘写入速度：%s MB/s" % (diff_write_bytes / 1024 / 1024))

            if diff_read_bytes < 1024:
                disk_status.append("当前磁盘读取速度：%s B/s" % diff_read_bytes)
            elif 1024 <= diff_read_bytes <= 1024 * 1024:
                disk_status.append("当前磁盘读取速度：%s KB/s" % (diff_read_bytes / 1024))
            else:
                disk_status.append("当前磁盘读取速度：%s MB/s" % (diff_read_bytes / 1024 / 1024))

            old_write_bytes = disk_io_info.write_bytes
            old_read_bytes = disk_io_info.read_bytes
            time.sleep(1)


def printHelp():
    tip = """
Usage: python sabotage.py [-c min-max] [-m min-max] [-o writeSpeed]

  -h Output this help and exit.
  -c Simulate CPU utilization.You have to give the minimum range and the maximum range. 
     Use the minus symbol(-) between two numbers.
  -m Simulate memory utilization.You have to give the minimum range and the maximum range. 
     Use the minus symbol(-) between two numbers.
  -o Simulate disk write speed. The unit is M. The actual write speed will be less than 
     the given value.How much less depends on the write speed of the disk.
     
Examples:
  python sabotage.py -c 50-60 -m 60-70 -o 50
  python sabotage.py -m 60-70 -o 50
  python sabotage.py -c 50-60
"""
    print(tip)
    exit(1)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-h-c:-m:-o:-i")
    except getopt.GetoptError as e:
        printHelp()

    try:
        for opt_name, opt_value in opts:
            if opt_name == '-h':
                printHelp()
            if opt_name == '-c':
                min_cpu, max_cpu = str(opt_value).split("-")
                mockCpu = MockCpu()
                mockCpu.min_cpu = int(min_cpu)
                mockCpu.max_cpu = int(max_cpu)
                mockCpu.start()
            if opt_name == '-m':
                min_memory, max_memory = str(opt_value).split("-")
                mockMemory = MockMemory()
                mockMemory.min_memory = int(min_memory)
                mockMemory.max_memory = int(max_memory)
                mockMemory.start()
            if opt_name == '-o':
                mockDisOutput = MockDiskOutput()
                mockDisOutput.write_speed = int(opt_value)
                mockDisOutput.start()
            if opt_name in ('-o', '-i'):
                GetDiskStatus().start()
    except:
        printHelp()

    try:
        while True:
            os.system("cls")
            for item in cpu_status:
                print(item)
            for item in memory_status:
                print(item)
            for item in disk_status:
                print(item)
            time.sleep(1)
    except KeyboardInterrupt:
        os.system("taskkill /im python.exe /f")
