from fastapi import FastAPI, File, Request
from fastapi.responses import JSONResponse
import uvicorn
import typing
import multiprocessing
from . import VERSION
from .models import *
from .base import *
from importlib import reload

####
#
#   插件的Rest API服务
#   全局变量前面请加下划线，这些变量应该只被web.py内方法调用
#   **预计在将来某一个版本中被另外一种方法替代** (这行划去)
#   计划总赶不上变化不是吗
#
####

_rest_server = FastAPI(title="千乘插件API接口", version=VERSION, description="")


@_rest_server.post("/actions/{action_name}", tags=["动作"])
async def actions(action_name, plugin_stdin: typing.Optional[ACTION_TEST_MODEL]):
    """
    #   动作接口
    """
    clearLog(clear_size=1)

    #   在生成插件之后有actions就能成功import了
    try:
        import actions
        #   先初始化并释放一次动作类，以清空缓存
        actions.modules_dict()[action_name]()
        #   清空完再reload
        reload(actions)
    except:
        pass

    action = load_module(action_name, "action")

    if not action:
        log("error", f"无法找到功能：{action_name}")
        content = {
            "msg": f"无法找到功能：{action_name}"
        }
        return JSONResponse(content=content, status_code=404)

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, models.PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    #   获取input
    input_data = data_body.get("input")
    connection_data = data_body.get("connection")

    #   执行 run 相关操作
    output = action._run(input_data, connection_data, data_body.get("config"))

    if output["body"]["status"] != "True":
        return JSONResponse(content=output, status_code=500)
    else:
        return output


@_rest_server.post("/actions/{action_name}/test", tags=["动作"])
async def actions_test(action_name: str, plugin_stdin: typing.Optional[ACTION_TEST_MODEL]):
    """
    #   动作连接器测试接口
    """
    return rest_test("action", action_name, plugin_stdin)


def load_module(func_name, module):
    """
    #   尝试重载各个组件
    参数说明
    func_name:str,      #   方法名
    module:str,         #   组件

    如果无法找到方法或组件则返回None
    """

    if module == "action":
        #   在生成插件之后有actions就能成功import了
        try:
            import actions
            #   先初始化并释放一次功能类，以清空缓存
            actions.modules_dict()[func_name]()
            #   清空完再reload
            reload(actions)
            return actions.modules_dict()[func_name]()
        except:
            pass

    elif module == "trigger":
        #   通过接口创建的接收器进程会重新加载文件，所以无需reload和清缓存
        try:
            import triggers
            return triggers.modules_dict()[func_name]()
        except:
            pass

    elif module == "alarm_receiver":
        try:
            import alarm_receivers
            return alarm_receivers.modules_dict()[func_name]()
        except:
            pass

    elif module == "indicator_receiver":
        try:
            import indicator_receivers
            return indicator_receivers.modules_dict()[func_name]()
        except:
            pass

    elif module == "asset_receiver":
        try:
            import asset_receivers
            return asset_receivers.modules_dict()[func_name]()
        except:
            pass

    return None


def rest_test(module, func_name, plugin_stdin):
    """
    #   通用接收器的连接器测试方法
    参数说明：
    module:str,         #   组件，module = action,trigger,alarm_receiver,indicator_receiver,asset_receiver
    func_name:str,  #   方法名称
    plugin_stdin:str,   #   接口传入数据

    因为测试连接器流程一样
    所有使用一个通用方法进行维护
    """

    clearLog(clear_size=1)

    func = load_module(func_name, module)

    if not func:
        log("error", f"未找到功能：{func_name}")
        content = {
            "msg": "未找到功能：{func_name}"
        }
        return JSONResponse(content=content, status_code=404)

    #   取出body
    data = plugin_stdin.dict()
    data_body = data.get("body")

    connection_data = data_body.get("connection")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")
        loadConfig()

    output = func._test(connection_data)

    if output["body"]["status"] != "True":
        return JSONResponse(content=output, status_code=500)
    else:
        return output


def receivers(module, receiver_name, plugin_stdin):
    """
    #   通用接收器方法
    参数说明：
    module:str,         #   组件，module = trigger,alarm_receiver,indicator_receiver,asset_receiver
    receiver_name:str,  #   接收器名称
    plugin_stdin:str,   #   接口传入数据

    因为触发器、告警接收器、情报接收器、资产接收器代码重复率极高（或者可以说一模一样的），
    因此使用一个通用方法进行维护
    """

    clearLog(clear_size=1)

    receiver = load_module(receiver_name, module)

    module_dict = {
        "trigger": "触发器",
        "indicator_receiver": "情报接收器",
        "alarm_receiver": "告警接收器",
        "asset_receiver": "资产接收器"
    }

    data = plugin_stdin.dict()

    try:
        #   判断是否存在接收器类型
        if data.get("type") not in module_dict.keys():
            log("error", f"不支持的接收器类模块类型（type）：{data.get('type')}")
            content = {
                "msg": f"不支持的接收器类模块类型（type）：{data.get('type')}",
                "tips": f"目前仅支持{list(module_dict.keys())}"
            }
            return JSONResponse(content=content, status_code=400)

        #   判断是否存在该接收器
        if not receiver:
            log("error", f"不存在的功能：{receiver_name}")
            content = {
                "msg": f"不存在的功能：{receiver_name}"
            }
            return JSONResponse(content=content, status_code=400)

        #   data中的body部分
        data_body = data.get("body")
        #   run输入参数
        input_data = data_body.get("input")
        #   连接器参数
        connection_data = data_body.get("connection")
        #   转发地址
        dispatcher_url = data_body.get("dispatcher").get("url")
        #   缓存地址
        cache_url = data_body.get("dispatcher").get("cache_url")
        #   进程创建
        process = multiprocessing.Process(target=receiver._run,
                                          args=(input_data, connection_data, dispatcher_url, cache_url,
                                                data_body.get("config")))
        #   启动进程
        process.start()

        from .base import _log_data

        content = {
            "version": "v1",
            "type": data["type"],
            "body": {
                "status": "True",
                "log": _log_data,
                "error_trace": "",
                "msg": f"{module_dict[data['type']]}已创建完成"
            }
        }

        return JSONResponse(content=content, status_code=201)

    except Exception as error:

        from .base import _log_data

        log("error", f"{error}")

        content = {
            "version": "v1",
            "type": data["type"],
            "body": {
                "status": "False",
                "log": _log_data,
                "error_trace": traceback.format_exc(),
                "msg": f"{module_dict[data['type']]}创建失败"
            }
        }

        return JSONResponse(content=content, status_code=500)


@_rest_server.post("/triggers/{trigger_name}", tags=["触发器"])
async def triggers(trigger_name: str, plugin_stdin: typing.Optional[TRIGGER_TEST_MODEL]):
    """
    #   触发器接口
    """
    return receivers("trigger", trigger_name, plugin_stdin)


@_rest_server.post("/triggers/{trigger_name}/test", tags=["触发器"])
async def trigger_test(trigger_name: str, plugin_stdin: typing.Optional[TRIGGER_TEST_MODEL]):
    """
    #   触发器连接器测试接口
    """
    return rest_test("trigger", trigger_name, plugin_stdin)


@_rest_server.post("/alarm_receivers/{alarm_receiver_name}", tags=["告警接收器"])
async def alarm_receivers(alarm_receiver_name: str, plugin_stdin: typing.Optional[ALARM_RECEIVER_TEST_MODEL]):
    """
    #   告警接收器接口
    """
    return receivers("alarm_receiver", alarm_receiver_name, plugin_stdin)


@_rest_server.post("/alarm_receivers/{alarm_receiver_name}/test", tags=["告警接收器"])
async def alarm_receivers_test(alarm_receiver_name: str,
                               plugin_stdin: typing.Optional[ALARM_RECEIVER_TEST_MODEL]):
    """
    #   告警接收器连接器测试接口
    """
    return rest_test("alarm_receiver", alarm_receiver_name, plugin_stdin)


@_rest_server.post("/indicator_receivers/{indicator_receiver_name}", tags=["情报接收器"])
async def indicator_receivers(indicator_receiver_name: str,
                              plugin_stdin: typing.Optional[INDICATOR_RECEIVER_TEST_MODEL]):
    """
    #   情报接收器接口
    """
    return receivers("indicator_receiver", indicator_receiver_name, plugin_stdin)


@_rest_server.post("/indicator_receivers/{indicator_receiver_name}/test", tags=["情报接收器"])
async def indicator_receivers_test(indicator_receiver_name: str,
                                   plugin_stdin: typing.Optional[INDICATOR_RECEIVER_TEST_MODEL]):
    """
    #   情报接收器连接器测试接口
    """
    return rest_test("indicator_receiver", indicator_receiver_name, plugin_stdin)


@_rest_server.post("/asset_receivers/{asset_receiver_name}", tags=["资产接收器"])
async def asset_receivers(asset_receiver_name: str,
                          plugin_stdin: typing.Optional[ASSET_RECEIVER_TEST_MODEL]):
    return receivers("asset_receiver", asset_receiver_name, plugin_stdin)


@_rest_server.post("/asset_receivers/{asset_receiver_name}/test", tags=["资产接收器"])
async def asset_receivers_test(asset_receiver_name: str,
                               plugin_stdin: typing.Optional[ASSET_RECEIVER_TEST_MODEL]):
    return rest_test("asset_receiver", asset_receiver_name, plugin_stdin)


@_rest_server.post("/update_plugin", tags=["插件热更新"])
async def update_plugin(update_pack: bytes = File()):
    """
    #   上传更新包
    """
    try:
        save_update_pack(update_pack)
        update_result = hotUpdate("http")
        clearUpdateFile()
        if update_result:
            return {
                "msg": "更新完成"
            }
        else:
            return {
                "msg": "更新失败"
            }
    except Exception as error:
        clearUpdateFile()
        content = {
            "msg": f"更新失败 - {error}"
        }
        return JSONResponse(content=content, status_code=500)


@_rest_server.post("/generate_plugin", tags=["插件生成器"])
async def generate_plugin(plugin_construction: models.PLUGIN_CONSTRUCTION):
    """
    #   自动生成插件接口
    #   此接口暂时不可用
    TODO 修复自动生成插件功能在多进程下的运行
    """
    return {
        "msg": "接口暂时停用"
    }

    # clearLog(clear_size=1)
    #
    # data = plugin_construction.dict()
    #
    # #   将特殊定义文件放到缓存下，等待SDK调用
    # setLocalCache(data, "plugin_construction")
    #
    # os.system("chariot-plugin -ag {}".format(os.path.join("__sdkcache__", "plugin_construction.chariot-128.sdkc")))

@_rest_server.get("/sdk_version", tags=["插件信息"])
async def sdk_version():
    """
    #   获取SDK版本
    """
    return {
        "sdk_version": VERSION
    }


@_rest_server.get("/plugin_data", tags=["插件信息"])
async def get_plugin_data():
    """
    #   获取插件定义数据接口
    """

    json_data_path = os.path.join(os.getcwd(), "plugin.spec.json")

    yaml_data_path = os.path.join(os.getcwd(), "plugin.spec.yaml")

    if os.path.exists(json_data_path):
        plugin_data = json.load(open(json_data_path, "r"))
        return plugin_data

    elif os.path.exists(yaml_data_path):
        with open(yaml_data_path, "r", encoding="utf-8") as file:
            plugin_data = yaml.load(file.read(), Loader=yaml.FullLoader)
        return plugin_data

    else:
        log("error", "插件定义数据不存在")
        content = {
            "error": "插件定义数据不存在"
        }
        return JSONResponse(content=content, status_code=404)


@_rest_server.post("/transpond", tags=["转发数据接收"])
async def receive_transponded(request: Request):
    """
    #   测试用接口，用于接收转发的数据
    """
    try:
        data = await request.body()
        log("info", f"获得转发数据：\n {data.decode()}")
        resp_data = {
            "msg": "接收成功",
            "error": ""
        }
        return JSONResponse(content=resp_data)
    except Exception as error:
        resp_data = {
            "msg": "接收失败",
            "error": str(error)
        }
        return JSONResponse(content=resp_data, status_code=500)


def runserver(workers=4):
    """
    #   启动api服务
    参数说明：
    workers:int,    #   工作进程数量
    """
    os.system("")
    log("attention", "在浏览器内输入 http://127.0.0.1:10001/docs 以进行接口测试")
    uvicorn.run("SDK.web:_rest_server", host="0.0.0.0", port=10001, workers=workers)
