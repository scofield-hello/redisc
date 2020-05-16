import os
import sys
import argparse
from jinja2 import Template

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="redisc")
    parser.add_argument("server",
                        action="store",
                        help="配置类型 master|slave|sentinel")
    parser.add_argument("bind", action="store", help="绑定IP地址")
    parser.add_argument("port", action="store", type=int, help="绑定服务端口")
    parser.add_argument("-daemonize",
                        dest="daemonize",
                        action="store_true",
                        default=True,
                        help="是否已守护进程运行, 默认为True")
    parser.add_argument("-dir",
                        dest="dir",
                        action="store",
                        default="./",
                        help="数据文件目录 默认./")
    parser.add_argument("-dbfilenamePrefix",
                        dest="dbfilenamePrefix",
                        action="store",
                        default="dump",
                        help="数据文件名, 默认dump")
    parser.add_argument("-requirepass",
                        dest="requirepass",
                        action="store",
                        help="当前redis密码, 默认为空")
    parser.add_argument("-masterauth",
                        dest="masterauth",
                        action="store",
                        help="master 密码")
    parser.add_argument("-loglevel",
                        dest="loglevel",
                        action="store",
                        default="notice",
                        help="日志级别 debug|verbose|notice|warning 默认notice")
    parser.add_argument("-masterip",
                        dest="masterip",
                        action="store",
                        default="127.0.0.1",
                        help="master ip")
    parser.add_argument("-masterport",
                        dest="masterport",
                        action="store",
                        type=int,
                        default=6379,
                        help="master 端口")
    parser.add_argument("-output",
                        dest="output",
                        action="store",
                        default="./output",
                        help="输出目录, 默认./output")

    parser.add_argument("-downAfterMilliseconds",
                        dest="downAfterMilliseconds",
                        action="store",
                        type=int,
                        default=10000,
                        help="down-after-milliseconds")
    parser.add_argument("-failoverTimeout",
                        dest="failoverTimeout",
                        action="store",
                        type=int,
                        default=15000,
                        help="failover-timeout")

    parsed_args = parser.parse_args(sys.argv[1:])
    bind = parsed_args.bind
    port = parsed_args.port
    directory = parsed_args.dir
    server = parsed_args.server
    daemonize = parsed_args.daemonize
    dbfilename_prefix = parsed_args.dbfilenamePrefix
    requirepass = parsed_args.requirepass
    loglevel = parsed_args.loglevel
    masterip = parsed_args.masterip
    masterport = parsed_args.masterport
    masterauth = parsed_args.masterauth
    down_after_milliseconds = parsed_args.downAfterMilliseconds
    failover_timeout = parsed_args.failoverTimeout
    output = parsed_args.output
    if not os.path.exists(output):
        os.makedirs(output)
    if server not in ["master", "slave", "sentinel"]:
        raise "请指定生成配置类型 master|slave|sentinel"
    filename = None
    render_text = None
    template_str = None
    startup_cmd = None
    connect_cmd = None
    template_filename = "./templates/redis.conf" if server in [
        "master", "slave"
    ] else "./templates/sentinel.conf"
    with open(file=template_filename, mode="r", encoding="utf-8") as f:
        template_str = f.read()
    template = Template(template_str)
    if server == "master":
        render_text = template.render(bind=bind,
                                      port=port,
                                      dir=directory,
                                      daemonize=daemonize,
                                      dbfilenamePrefix=dbfilename_prefix,
                                      requirepass=requirepass,
                                      loglevel=loglevel)
        filename = os.path.join(output, "redis_%s.conf" % port)
        startup_cmd = "src/redis-server redis_%s.conf" % port
        connect_cmd = "src/redis-cli -h %s -p %s -a %s" % (bind, port,
                                                           requirepass)
    elif server == "slave":
        render_text = template.render(bind=bind,
                                      port=port,
                                      dir=directory,
                                      daemonize=daemonize,
                                      dbfilenamePrefix=dbfilename_prefix,
                                      requirepass=requirepass,
                                      masterip=masterip,
                                      masterport=masterport,
                                      masterauth=masterauth,
                                      loglevel=loglevel)
        filename = os.path.join(output, "redis_%s.conf" % port)
        startup_cmd = "src/redis-server redis_%s.conf" % port
        connect_cmd = "src/redis-cli -h %s -p %s -a %s" % (bind, port,
                                                           requirepass)
    elif server == "sentinel":
        render_text = template.render(
            bind=bind,
            port=port,
            dir=directory,
            daemonize=daemonize,
            dbfilenamePrefix=dbfilename_prefix,
            requirepass=requirepass,
            masterip=masterip,
            masterport=masterport,
            masterauth=masterauth,
            downAfterMilliseconds=down_after_milliseconds,
            failoverTimeout=failover_timeout,
            loglevel=loglevel)
        filename = os.path.join(output, "sentinel_%s.conf" % port)
        startup_cmd = "src/redis-server sentinel_%s.conf --sentinel" % port
        connect_cmd = "src/redis-cli -h %s -p %s" % (bind, port)
    with open(file=filename, mode="w", encoding="utf-8") as f:
        f.write(render_text)
    print("配置文件已生成:\n%s" % filename)
    print("请使用以下命令启动:\n%s" % startup_cmd)
    print("检查服务进程:\nps -ef|grep redis")
    print("启动客户端测试:\n%s" % connect_cmd)