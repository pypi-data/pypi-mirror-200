<div align="center">

# ともたけ よしの bot
*******************
_🌱 This project is based on the [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) and [fnbot](https://github.com/mrhblfx/fnbot) development of QQ entertainment robot 🌱_

</div>

# Quick Start

## for Windows
- 安装`python>=3.8`
- 下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- 修改生成的'config.yml'
<details>
<summary>Example of config.yml</summary>

```yml
account: # 账号相关
  uin: 123456789 # QQ账号
  password: '' # 密码为空时使用扫码登录
```
and
```yml
# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器

  - http: # HTTP 通信设置
      address: 127.0.0.1:9900 # HTTP监听地址
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      #- url: ''                # 地址
      #  secret: ''             # 密钥
      #  max-retries: 3         # 最大重试，0 时禁用
      #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
        - url: http://127.0.0.1:9901/ # 地址
          secret: ''                  # 密钥
          max-retries: 10             # 最大重试，0 时禁用
          retries-interval: 1000      # 重试时间，单位毫秒，0 时立即
```

</details>

+ 在终端运行
```powershell
git clone https://github.com/mrhblfx/fnbot
```

+ 修改`pybot.toml`
<details>
<summary>Example of pybot.toml</summary>

```toml
host = "127.0.0.1"
port = 9900
post = 9901
bot_qq = 123456789 # QQ account
group_list = [123456,1234567] # The group chat where QQbot is located
```

</details>

+ `python bot.py`

## for Linux
```bash
```

## unfinished to be continued

## ......
