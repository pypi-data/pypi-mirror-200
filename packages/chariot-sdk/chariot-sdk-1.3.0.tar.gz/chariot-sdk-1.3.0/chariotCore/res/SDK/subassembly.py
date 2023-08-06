from .base import *

import traceback
import requests
import threading


class Actions(object):

    def __init__(self):

        self._output = {
            "version": "v1",
            "type": "action",
            "body": {}
        }

        #   name 按规范应小写且用下划线隔开单词
        self.name = ""

        #   入参 校验类
        self.inputModel = None

        #   出参 校验类
        self.outputModel = None

        #   连接器 校验类
        self.connModel = None

    def connection(self, data: dict):

        ...

    def run(self, params: dict) -> dict:

        ...

    def _test(self, connection_data):
        """
        #   运行连接器
        参数说明：
        conection_data:dict,    #   连接数据

        此过程用方法单独写出来方便测试连接器部分
        """

        log("debug", f"获取连接器数据：\n  {connection_data}")

        try:
            #   校验入参数据
            log("info", "校验连接器数据")
            connection_data = checkModel(connection_data, self.connModel)

            log("info", "运行连接器中")
            self.connection(connection_data)
            log("info", "连接器运行正常")
            log("info", "构建连接器运行信息")
            output = self._buildOutput({}, True)
            return output

        except Exception as error:
            #   收集错误信息
            log("error", f"连接器发生异常，错误原因：\n  {error}")

            error_trace = traceback.format_exc()
            log("error", f"详细错误信息：\n{error_trace}")

            log("info", "构建连接器错误信息")
            output = self._buildOutput({}, False, error_trace)
            return output

    def _run(self, input_data: dict, connection_data: dict, config_data: dict = None):
        """
        #   运行全流程
        参数说明：
        input_data:dict,    #   入参数据
        conection_data:dict,    #   连接数据
        config_data:dict,   #   配置数据
        """
        log("info", "插件运行中")

        if config_data:
            log("info", "检查到有配置信息")
            loadConfig(config_data)
        else:
            log("info", "未传入配置信息，使用默认配置")
            loadConfig()

        #   运行connection
        output = self._test(connection_data)

        #   连接器异常时直接返回错误输出
        if output["body"]["status"] == "False":
            return output

        #   运行run
        try:

            log("debug", f"获取功能数据：\n  {input_data}")

            #   校验功能数据
            log("info", "校验功能入参数据")
            input_data = checkModel(input_data, self.inputModel)

            log("info", "执行功能中")

            output_data = self.run(input_data)

            log("info", "功能执行完成")

            log("info", "校验功能出参数据")
            output_data = checkModel(output_data, self.outputModel)

            #   构建output
            log("info", "构建输出数据")
            output = self._buildOutput(output_data, True)

        except Exception as error:
            #   收集错误信息
            log("error", f"功能执行异常，错误原因：\n  {error}")

            error_trace = traceback.format_exc()
            log("error", f"详细错误信息：\n{error_trace}")

            #   构建错误输出的output
            log("info", "构建错误返回信息")
            output = self._buildOutput({}, False, error_trace)

        return output

    def _buildOutput(self, output_data: dict = {}, status: bool = True, error_trace: str = ""):
        """
        #   构建出参信息，包括日志信息
        参数说明：
        output_data:dict,   #   输出信息
        status:bool,    #   run执行状态，执行成功为True，不成功为False
        error_trace:str,  #   详细的错误信息，用于给开发人员看
        """
        from .base import _log_data

        output = self._output

        output["body"]["output"] = output_data
        #   千乘引擎接受的是str类型的状态
        output["body"]["status"] = str(status)
        #   为了减少重复信息，日志先暂时省略
        output["body"]["log"] = "......"
        output["body"]["error_trace"] = error_trace

        print("  " + str(output))

        output["body"]["log"] = _log_data

        return output


class Triggers(object):

    def __init__(self):

        self._output = {
            "version": "v1",
            "type": "trigger",
            "body": {}
        }

        #   name 按规范应小写且用下划线隔开单词
        self.name = ""

        #   缓存服务URL
        self.cache_url = ""

        #   发送到
        self.dispatcher_url = ""

        #   入参 校验类
        self.inputModel = None

        #   出参 校验类
        self.outputModel = None

        #   连接器 校验类
        self.connModel = None

    def connection(self, data: dict):

        ...

    def run(self, params):

        ...

    def _test(self, connection_data):
        """
        #   运行连接器
        参数说明：
        conection_data:dict,    #   连接数据
        """

        log("debug", f"获取连接器数据：\n  {connection_data}")

        try:
            #   校验入参数据
            log("info", "校验连接器数据")
            connection_data = checkModel(connection_data, self.connModel)

            log("info", "运行连接器中")
            self.connection(connection_data)
            log("info", "连接器运作正常")
            log("info", "构建连接器运行信息")
            output = self._buildOutput({}, True)
            return output

        except Exception as error:
            #   收集错误信息
            log("error", f"连接器异常，错误原因：\n  {error}")

            error_trace = traceback.format_exc()
            log("error", f"详细错误信息：\n{error_trace}")

            log("info", "构建连接器错误信息")
            output = self._buildOutput({}, False, error_trace)
            return output

    def _run(self, input_data, connection_data, dispatcher_url, cache_url, config_data: dict = None):
        """
        #   运行全流程
        参数说明：
        input_data:dict,    #   入参数据
        conection_data:dict,    #   连接数据
        dispatcher_url:str,     #   数据转发URL
        cache_url:str,          #   缓存服务URL
        config_data:dict,   #   配置数据
        """
        log("info", "插件运行中")

        self.dispatcher_url = dispatcher_url

        self.cache_url = cache_url

        if config_data:
            log("info", "检查到有配置信息")
            loadConfig(config_data)
        else:
            log("info", "未传入配置信息，使用默认配置")
            loadConfig()

        #   运行connection
        output = self._test(connection_data)

        #   连接器异常时直接返回错误输出
        if output["body"]["status"] == "False":
            return output

        #   运行run
        try:

            log("debug", f"获取功能数据：\n  {input_data}")

            #   校验入参数据
            log("info", "校验入参数据")
            input_data = checkModel(input_data, self.inputModel)

            log("info", "执行功能中")

            #   正常情况下，触发器、情报接收器、告警接收器都是处于轮询状态，不会主动跳出
            self.run(input_data)

            log("info", "功能执行完成")

        except Exception as error:
            #   收集错误信息
            log("error", f"功能执行异常，错误原因：\n  {error}")

            error_trace = traceback.format_exc()
            log("error", f"详细错误信息：\n{error_trace}")

            #   构建错误输出的output
            log("info", "构建错误返回信息")
            output = self._buildOutput({}, False, error_trace)

        else:
            output = self._buildOutput({}, True)

        return output

    def send(self, data: dict = {}, needCheck: bool = True):
        """
        #   转发信息
        参数说明：
        data:dict,  #   需要转发的信息
        needCheck:bool, #   是否需要对转发的信息进行出参验证
        """
        #   创建转发线程
        thread1 = threading.Thread(target=transpondData, args=(data, needCheck, self.outputModel, self.dispatcher_url))
        thread1.start()

    def setCache(self, data: dict = {}):
        """
        #   设置千乘-插件缓存
        参数说明：
        data:dict,  #   需要缓存的数据

        设置缓存失败时抛出异常
        """
        log("info", "缓存数据中......")

        cache = {
            "method": "set",
            "data": json.dumps(data)
        }

        try:
            response = requests.post(self.cache_url, json=cache, verify=False)
        except:
            raise Exception("向缓存服务器请求失败")

        if response.status_code == 201:
            log("info", f"缓存成功，状态码：{response.status_code}\n  返回信息：{response.text}")
            return

        elif response.status_code == 413:
            raise Exception(f"缓存失败，请求内容过大( >3 MB )，缓存失败，状态码：{response.status_code}\n")

        else:
            raise Exception(f"缓存失败，状态码：{response.status_code}\n  返回信息：{response.text}")

    def getCache(self) -> dict:
        """
        #   获取千乘-插件缓存

        获取缓存异常时抛出异常
        """
        log("info", "获取缓存数据中.....")

        method = {
            "method": "get"
        }

        try:
            response = requests.post(self.cache_url, json=method, verify=False)
        except:
            raise Exception("向缓存服务器请求失败")

        if response.status_code == 200:
            log("info", f"获取缓存成功，状态码：{response.status_code}\n  返回信息：{response.text}")
            cache = json.loads(response.json().get("data"))
            return cache

        elif response.status_code == 413:
            raise Exception(f"获取缓存失败，请求内容过大( >3 MB )，获取缓存失败，状态码：{response.status_code}\n")

        else:
            raise Exception(f"获取缓存失败，状态码：{response.status_code}\n  返回信息：{response.text}")

    def _buildOutput(self, output_data: dict = {}, status: bool = True, error_trace: str = ""):
        """
        #   构建出参信息，包括日志信息
        参数说明：
        output_data:dict,   #   输出信息
        status:bool,    #   run执行状态，执行成功为True，不成功为False
        error_trace:str,  #   详细的错误信息，用于给开发人员追踪错误
        """

        from .base import _log_data

        output = self._output
        output["body"]["output"] = output_data

        output["body"]["status"] = str(status)
        #   为了减少重复信息，日志先暂时省略
        output["body"]["log"] = "......"
        output["body"]["error_trace"] = error_trace

        print("  " + str(output))

        output["body"]["log"] = _log_data

        return output


class IndicatorReceivers(Triggers):
    """
    #   情报接收器目前实现原理上和触发器没有区别
    """

    def __init__(self):
        super().__init__()
        self._output["type"] = "indicator_receiver"


class AlarmReceivers(Triggers):
    """
    #   告警接收器目前实现原理上和触发器没有区别
    """

    def __init__(self):
        super().__init__()
        self._output["type"] = "alarm_receiver"


class AssetReceivers(Triggers):
    """
    #   资产接收器目前实现原理和触发器没有区别
    """

    def __init__(self):
        super().__init__()
        self._output["type"] = "asset_receiver"
