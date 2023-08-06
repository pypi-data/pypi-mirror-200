# 快速开始
前置条件：
* Python >= 3.6
* 安装微信[3.6.0.18版本](https://pan.baidu.com/s/1OFVmmmbrHTAqZUAE71tvyA?pwd=qka8)。
* 下载[version.dll](https://github.com/q757571446/wxchatdll/blob/master/version.dll), 放入微信安装目录，如果需要源代码编译请查看[wxchatdll](https://github.com/q757571446/wxchatdll)仓库
## 安装
```
pip install wxchat
```

## 使用
1. 启动微信，弹出控制台，显示以下消息，则服务端已启动
```
服务已启动, 端口号1: 10086, 端口号2: 10010
```
2. 编写客户端代码，调用微信相关功能

```
    client = WeixinClient()
    profile = client.login()
    print("登录用户: ", profile)

    @client.message()
    def all_msg(message):
        print("all_msg", message)

    client.run_forever(debug=True)
```

## 其他
服务端默认端口号为10086和10010，如果需要指定端口号运行，请启动微信时添加参数，例如:
```
WeChat.exe -port1 123456 -port2 654321
```
客户端和服务端如果不在同一台机器上，请指定ip地址和端口号，例如:
```
client = WeixinClient("192.168.0.109", 123456, 654321)
```


## 示例
1. [接收消息](https://github.com/q757571446/WeixinClient-Python/blob/master/examples/receive_message.py)
2. [发送消息](https://github.com/q757571446/WeixinClient-Python/blob/master/examples/send_message.py)
3. [获取联系人](https://github.com/q757571446/WeixinClient-Python/blob/master/examples/contact.py)
4. [获取群成员](https://github.com/q757571446/WeixinClient-Python/blob/master/examples/chatroom.py)

# 声明
本项目仅为学习交流之用，如有问题请加入QQ群: 620013287, 或点击链接加入[微信逆向交流群](https://jq.qq.com/?_wv=1027&k=3dSGCt0z)，请不要用于商业、违法途径，本人不对此源码造成的违法负责。
