# Windows环境下，增加CPU、内存、磁盘IO、网络IO负担

- 可以故意提高CPU利用率，导致机器变慢
- 可以故意提高内存占用率，导致机器可用内存变少
- 可以故意疯狂读写文件，导致磁盘IO变累

# 依赖安装

    pip install psutil

# 使用方法

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
      
# 举例

让cpu利用率达到50%至60%左右，内存占用率达到60%至70左右，磁盘当前写入速度达到50M/s

    python sabotage.py -c 50-60 -m 60-70 -o 50
    
让内存占用率达到60%至70左右，磁盘当前写入速度达到50M/s

    python sabotage.py -m 60-70 -o 50    
    
让cpu利用率达到50%至60%左右

    python sabotage.py -c 50-60
    

# TODO

- [ ] 磁盘读取占用
- [ ] 网络IO占用