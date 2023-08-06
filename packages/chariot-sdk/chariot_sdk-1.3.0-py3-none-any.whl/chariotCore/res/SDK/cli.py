from .chariot import *

import sys
import json


####
#
#   写在前面
#   SDK内功能的开发应秉承以下原则：
#   1.  SDK在运行时出现问题应当及时抛出异常从而终止整个流程运行，以避免在出现错误情况下执行业务功能造成严重后果
#   2.  运行业务功能需要使用异常捕获，从而让业务功能不影响SDK对业务功能的错误信息收集和转发
#
####

def client(plugin):
    """
    #   此方法用于作为起始，根据命令跳转到各个功能
    参数说明：
    plugin:PLUGIN,      #   插件集合类（该类位于生成的插件后的根目录下main.py文件内）

    """
    log("info", "正在启动插件")

    #   获取命令
    log("info", "获取执行参数：\n  {}".format(sys.argv))

    #   加载配置文件
    loadConfig()

    #   初始化一个插件类对象，此类位于生成插件后的插件根目录下的main.py里
    #   该对象在初始化后会存储所有功能的类，方便调用
    plugin_object = plugin()

    if sys.argv.count("run"):
        data = getData()
        log("info", "执行 run 命令")
        run(data, plugin_object)

    elif sys.argv.count("http"):
        #   默认工作进程
        workers = 4

        try:
            workers = int(sys.argv[2])
        except:
            pass

        log("info", "执行 http 命令")

        http(workers)

    elif sys.argv.count("test"):
        data = getData()
        log("info", "执行 test 命令")
        test(data, plugin_object)

    else:
        log("error", "未知的命令，输入-h以获取帮助")
        return


def getData() -> dict:
    """
    #   此方法用于获取需要的运行数据
    #   在千乘系统中，可能并不会传入json数据文件，而是会直接传入json数据或字典数据，此时输入cmd指令长度不足（输入数据不计长度）
    #   所以使用sys.stdin.read()读取可能存在的数据
    """
    if len(sys.argv) >= 3:
        testfile_path = sys.argv[2]
        data = loadTestData(testfile_path)
    else:
        data = sys.stdin.read()
        if type(data) != dict and data:
            data = json.loads(data)
    if data:
        log("debug", "获取执行载荷：\n  {}".format(data))
        return data
    else:
        log("error", "未检测到必要的运行数据")
        return {}
