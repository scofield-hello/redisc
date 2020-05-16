# redisc
redis配置文件生成工具

## 使用帮助
```
pipenv run python redisc.py -h

usage: redisc [-h] [-daemonize] [-dir DIR]
              [-dbfilenamePrefix DBFILENAMEPREFIX] [-requirepass REQUIREPASS]
              [-masterauth MASTERAUTH] [-loglevel LOGLEVEL]
              [-masterip MASTERIP] [-masterport MASTERPORT] [-quorum QUORUM]
              [-output OUTPUT] [-downAfterMilliseconds DOWNAFTERMILLISECONDS]
              [-failoverTimeout FAILOVERTIMEOUT]
              server bind port

positional arguments:
  server                配置类型 master|slave|sentinel
  bind                  绑定IP地址
  port                  绑定服务端口

optional arguments:
  -h, --help            show this help message and exit
  -daemonize            是否已守护进程运行, 默认为True
  -dir DIR              数据文件目录 默认./
  -dbfilenamePrefix DBFILENAMEPREFIX
                        数据文件名, 默认dump
  -requirepass REQUIREPASS
                        当前redis密码, 默认为空
  -masterauth MASTERAUTH
                        master 密码
  -loglevel LOGLEVEL    日志级别 debug|verbose|notice|warning 默认notice
  -masterip MASTERIP    master ip
  -masterport MASTERPORT
                        master 端口
  -quorum QUORUM        quorum 比重, 默认为2
  -output OUTPUT        输出目录, 默认./output
  -downAfterMilliseconds DOWNAFTERMILLISECONDS
                        down-after-milliseconds
  -failoverTimeout FAILOVERTIMEOUT 
                        failover-timeout
```

## 生成master配置
```
pipenv run python redisc.py master 192.168.0.1 6379 -dir=/usr/redis/ -requirepass=123456 -dbfilenamePrefix=dump -loglevel=debug
```

## 生成slave配置
```
pipenv run python redisc.py slave 192.168.0.2 6380 -dir=/usr/redis/ -requirepass=123456 -dbfilenamePrefix=dump -loglevel=debug -masterip=192.168.0.1 -masterport=6379 -masterauth=123456
```

## 生成sentinel配置
```
pipenv run python redisc.py sentinel 192.168.0.3 26379 -dir=/usr/redis/ -masterip=192.168.0.1 -masterport=6379 -masterauth=123456 -quorum=2 -downAfterMilliseconds=10000 -failoverTimeout=15000
```
