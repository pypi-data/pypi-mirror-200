from .base import *
from .web import runserver


####
#
#   这里的方法主要是给开发时测试用的
#   但事实上，老版本千乘在创建触发器、告警接收器、情报接收器也会通过这里创建
#
####


def run(data: dict, plugin_object):
    """
    #   运行功能的整个流程
    参数说明：
    data:dict,      #   运行功能时的必要的数据
    plugin_object:PLUGIN,      #   插件集合对象（类位于生成的插件后的根目录下main.py文件内）

    """

    log("info", "尝试获取数据中的 body")

    #   必要的参数位于data内的body下
    data_body = data.get("body")
    if not data_body:
        log("error", "body 为空")
        return

    log("info", "检测需要运行的组件")

    modules_list = ["action", "trigger", "alarm", "receiver", "asset"]

    #   检查json数据是使用在哪个组件上的
    for module in modules_list:
        if data_body.get(module):
            runModule(data_body[module], data_body, plugin_object, module)
            return

    log("info", "未检测到需要运行的组件")


def runModule(func_name: str, data: dict, plugin_object, module):
    """
    #   运行功能
    参数说明：
    func_name:str,  #   功能名称（功能ID）
    data:dict,      #   运行功能时的必要的数据
    plugin_object:PLUGIN,      #   插件集合对象（类位于生成的插件后的根目录下main.py文件内）
    module:str,     #   组件，module = actions,

    出现异常时，会将异常信息放入log，但不会抛出异常
    """

    module_dict = {
        "action": "动作",
        "trigger": "触发器",
        "alarm": "告警接收器",
        "receiver": "情报接收器",
        "asset": "资产接收器"
    }

    log("info", f"运行{module_dict[module]}（{module}）中")

    plugin_object_dict = {
        "action": plugin_object.actions,
        "trigger": plugin_object.triggers,
        "alarm": plugin_object.alarm_receivers,
        "receiver": plugin_object.indicator_receivers,
        "asset": plugin_object.asset_receivers
    }

    func = plugin_object_dict[module][func_name]

    #   获取连接器数据
    connection_data = data.get("connection")
    #   获取入参
    input_data = data.get("input")

    if module == "action":
        func._run(input_data, connection_data)
    else:
        #   数据转发URL
        dispatcher_url = data.get("dispatcher").get("url")
        #   缓存服务URL
        cache_url = data.get("dispatcher").get("cache_url")
        func._run(input_data, connection_data, dispatcher_url, cache_url)

    log("info", f"{module_dict[module]}（{module}）运行结束")


def test(data: dict, plugin_object):
    """
    #   只运行连接器部分
    参数说明：
    data:dict,      #   运行功能时的必要的json数据
    plugin_object:PLUGIN,      #   插件集合对象（类位于生成的插件后的根目录下main.py文件内）
    """
    #   必要的参数位于data内的body下
    data_body = data.get("body", {})
    connection_data = data_body.get("connection")

    module_dict = {
        "action": "动作",
        "trigger": "触发器",
        "alarm": "告警接收器",
        "receiver": "情报接收器",
        "asset": "资产接收器"
    }

    plugin_object_dict = {
        "action": plugin_object.actions,
        "trigger": plugin_object.triggers,
        "alarm": plugin_object.alarm_receivers,
        "receiver": plugin_object.indicator_receivers,
        "asx set": plugin_object.asset_receivers
    }

    #   检查json数据是使用在哪个组件上的
    modules_list = ["action", "trigger", "alarm", "receiver", "asset"]

    #   检查json数据是使用在哪个组件上的
    for module in modules_list:
        if data_body.get(module):
            func_name = data_body[module]
            func = plugin_object_dict[module][func_name]
            func._test(connection_data)
            log("info", f"{module_dict[module]}（{module}）连接器运行结束")
            return

    log("info", "未检测到需要运行的组件")


def http(workers=4):
    """
    #   启动rest服务接口
    参数说明：
    workers:int,    #   工作进程数量
    """
    runserver(workers)
