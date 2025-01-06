#!/usr/bin/env python3
import urllib.request
import threading
import ipaddress

# 定义MOD子网的起始和结束IP地址
subnet_start = ""
subnet_end = ""

# 定义要扫描的端口列表
ports = [6600, 5050, 5005, 8086, 8088, 8888, 9080, 8000, 9026, 3952, 9000, 9999, 5555]

# 定义成功IP的文件
successful_ips_file = "successful_zb.txt"

# 定义最大线程数
max_threads = 10

# 检查IP和端口的连通性
def check_ip_port(ip, port):
    url = f"http://{ip}:{port}/udp/230.1.2.131:11111"
    try:
        response = urllib.request.urlopen(url, timeout=0.3)
        if response.getcode() == 200:
            server_header = response.headers.get('Server')
            if server_header and 'udpxy' in server_header:
                print(f"访问 {ip}:{port} 成功，Server: udpxy")
                with open(successful_ips_file, 'a', encoding='utf-8') as f:
                    f.write(f"{ip}:{port}\n")
    except Exception as e:
        print(f"访问 {ip}:{port} 失败: {e}")

# 清空文件内容
open(successful_ips_file, 'w').close()

# 转换起始和结束IP地址为IPv4Address对象
start_ip = ipaddress.IPv4Address(subnet_start)
end_ip = ipaddress.IPv4Address(subnet_end)

# 创建并启动线程来检查每个IP地址和端口
threads = []
for ip in range(int(start_ip), int(end_ip)+1):
    ip_address = str(ipaddress.IPv4Address(ip))
    for port in ports:
        if len(threads) >= max_threads:
            # 如果当前活动线程数已达到最大值，则等待线程完成
            for thread in threads:
                thread.join()
            threads = []  # 清空线程列表
        thread = threading.Thread(target=check_ip_port, args=(ip_address, port))
        thread.start()
        threads.append(thread)

# 等待剩余线程完成
for thread in threads:
    thread.join()