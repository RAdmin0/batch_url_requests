
import requests
import sys

# 屏蔽https的warning警告
import logging
logging.captureWarnings(True)


def url_request(url_file):
    f1 = open("http_connection.csv","a+",encoding="utf8")
    f2 = open("http_not_connection.csv","a+",encoding="utf8")
    count = 0
    count_conn = 0
    count_not_conn = 0
    
    schema = ["https://","http://"]
    
    # 第一个参数为要扫描得url列表
    with open(url_file,"r",encoding="utf8") as f:
        for url in f:
            count = count + 1
            print(f"第 {count} 个url")
            
            # 若该域名已有schema，不对其进行测试，跳出循环
            if url.strip().startswith("https://") or url.strip().startswith("http://"):
                f1.write(url)
                f1.flush()
                break
            
            for sche in schema:
                new_url = sche + url.strip()
                try:
                    rep = requests.get(new_url,timeout=10,verify=False)
                    f1.write(new_url+",")
                    f1.write(rep.status_code + "\n")
                    f1.flush()
                    count_conn = count_conn + 1
                    # 保证对同一个域名只请求一次
                    break
                except Exception as e:
                    count_not_conn = count_not_conn + 1
                    print(new_url+"无法连接")
                    f2.write(new_url)
                    f2.flush()
            print(f"可连接url数量：{count_conn}")
            print(f"无法连接url数量：{count_not_conn}")
            print('-'*50)
                
    f1.close()
    f2.close()

if __name__ == "__main__":
    try:
        url_request(sys.argv[1])
    except Exception as e:
        print("使用方法：python batch_url_requests.py url列表文件")
