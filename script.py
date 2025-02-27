import os
import time
import subprocess
import re

def ping(host,count=3,timeout=2,interval=1):
    try:
        result = subprocess.run(
                ["ping","-c",str(count),"-i",str(interval),"-W",str(timeout),host],
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        print(host)
        print(e)
        return False

def checkIntIp(ifname="eth4"):
    print("checkInterfaceIP")
    print("InterfaceName : ",ifname)
    try:
        result = subprocess.run(["ip", "address", "show", ifname], capture_output=True, text=True, check=True)
        # 正規表現でIPアドレスを抽出 (IPv4のみ)
        match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)/\d+", result.stdout)
        if match:
            ipaddr = match.group(1)
            print("IpAddress : ",ipaddr)
            return ipaddr  # IPアドレス部分を返す
        else:
            print("IpAddress : None")
            return None  # IPアドレスが見つからない場合
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

def restart_interface(interface="eth4"):
    print("インターフェースを再起動",interface)
    # リンクをダウンしてアップ
    subprocess.run(["ip","link","set",interface,"down"])
    time.sleep(1)
    subprocess.run(["ip","link","set",interface,"up"])

    # ファイルにリンク再接続回数を記録 ファイルの数をインクリメント
    log_filepath = "/var/log/myscript/interface_restart_count.log"
    log_dir = os.path.dirname(log_filepath)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir,exist_ok=True)
    if not os.path.exists(log_filepath):
        with open(log_filepath, "w") as log_file:
            log_file.write("0")  # 初期を書き込む

    with open(log_filepath,"r") as log_file:
        content = int(log_file.read().strip())
        content += 1
    with open(log_filepath,"w") as log_file:
        log_file.write(str(content))
    print("合計ポート再起動数",content)
    time.sleep(10)

def main():
    # 設定値
    servers = ["1.1.1.1","8.8.8.8","google.com"]
    interface = "eth4"

    while True:
        if checkIntIp(interface) == None:
            failure_count = 0 # 疎通ができないserver数
            print("はじめからチェック")
            for server in servers:
                if ping(server):
                    break
                # 以下pingが通らなかった場合
                failure_count += 1
                time.sleep(1)
                print("疎通不可",server,failure_count)
                if failure_count < len(servers) :
                    print(failure_count,len(servers))
                    continue
                # 以下全serverと疎通が取れなかった場合
                restart_interface(interface = interface)
                print("インターネット疎通不可")
                break
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()
