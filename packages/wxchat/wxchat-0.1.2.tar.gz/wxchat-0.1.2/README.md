# 快速开始
前置条件：
* Python >= 3.6
* 安装微信[3.6.0.18版本](https://pan.baidu.com/s/1OFVmmmbrHTAqZUAE71tvyA?pwd=qka8)。
* 下载[version.dll](https://github.com/q757571446/WeixinClient-Python/blob/master/version.dll), 放入微信安装目录
## 安装
```
pip install wxchat
```

## 使用
1. 服务端: 启动微信，弹出控制台，显示以下消息，则服务端已启动
```
服务已启动, 端口号1: 10086, 端口号2: 10010
```
2. 客户端: 编写代码，调用微信相关功能

```
from wxchat import WeixinClient, MsgType
if __name__ == '__main__':
    client = WeixinClient()
    profile = client.login()
    print("登录用户: ", profile)

    client.send_text("filehelper", "hello world!")

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
本项目仅为学习交流之用，服务端源码请入群获取，入群请添加微信haiyiqiang
