# UnifiCloud Gateway Ultra用のポートのIPアドレスが吹き飛ぶバグ?の対処療法スクリプト

## 中身
1. ip linkコマンドによるIFのIPアドレス確認  
2. IPv4が設定されていなければ、pingによるインターネット疎通確認  
3. インターネット疎通がいずれのサーバとも取れなければIFを再起動

## 設定
### インタフェース指定 
interface変数に任意のインタフェース名を指定。
UCG Ultraの場合、eth4がWANポートであるためeth4を指定している

### pingサーバ
seversリストに追記

## 常時起動
/etc/systemd/system/wanportForceUp.serviceに以下を書く
ExecStartは適宜変更
~~~
[Unit]
Description=Keep WAN Port Up
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/myscript/wanportForceUp.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
~~~
~~~
systemctl daemon-reload
~~~
~~~
systemctl enable wanportForceUp
~~~
~~~
systemctl start wanportForceUp
~~~
systemctl status wanportForceUp
~~~
