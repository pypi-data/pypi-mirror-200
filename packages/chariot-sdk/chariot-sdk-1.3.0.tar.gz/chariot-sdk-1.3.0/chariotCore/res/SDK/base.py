import json
from json import JSONDecodeError
import os
import logging
import time
import tempfile
import yaml
import tarfile
from pydantic import ValidationError
import traceback
import sys
import shutil
import threading
import configparser
from pydantic import BaseModel
import requests
import copy

from . import models

####
#
#   集成SDK中各种需要用上的方法
#   全局变量前面请加下划线，这些变量应该只被base.py内方法调用
#
####

#   Debug
_debug = False

#   默认转发线程数量限制
_threads_limit = 5
_sem = threading.Semaphore(_threads_limit)

#   默认最大日志占用内存
_max_log_size = 2

#   默认日志大小单位（KB,MB,GB）
_max_log_size_unit = "MB"

#   默认清理多少日志（0.00~1.00）
_log_clear_size = 0.5

#   日志数据
_log_data = ""

#   日志输出结构调整
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s\n  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def log(level="debug", msg=""):
    """
    #   设置不同级别的log输出
    #   attention等级和info同等，只是通过不同显示的颜色提醒一下开发者或用户
    参数说明：
    level:str,    #   log等级，levels = debug, info, attention, warning, error, critical
    msg:str,    #   log信息
    """
    global _log_data
    global _max_log_size
    global _max_log_size_unit
    global _log_clear_size
    global _debug

    clearLog(_max_log_size, _max_log_size_unit, _log_clear_size)

    msg = str(msg)

    #   输出带颜色log需要执行一次os.system("")
    os.system("")

    #   日志记录等级方法
    logging_func = {
        "debug": logging.debug,
        "info": logging.info,
        "attention": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical
    }

    logging_color = {
        #   绿色
        "debug": ("\033[32m", "\033[0m"),
        #   白色
        "info": ("", ""),
        #   蓝色
        "attention": ("\033[94m", "\033[0m"),
        #   黄色
        "warning": ("\033[93m", "\033[0m"),
        #   红色
        "error": ("\033[91m", "\033[0m"),
        #   红色
        "critical": ("\033[91m", "\033[0m")
    }

    logging_func[level](logging_color[level][0] + msg + logging_color[level][1])

    #   时间戳
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #   Debug模式下全记录
    if _debug:
        _log_data += f"[{log_time}] {level.upper()}\n  {msg}\n"
    #   非Debug则记录info等级以上日志
    else:
        _log_data += f"[{log_time}] {level.upper()}\n  {msg}\n" if level != "debug" else ""


def clearLog(size: int = _max_log_size, unit: str = _max_log_size_unit, clear_size: float = _log_clear_size):
    """
    #   清理日志
    #   由于不同字符占用大小不一样，所以当非全清理时，日志只以日志字符串长度为基准进行清理
    参数说明：
    size:int,   #   log大小限制，日志内存占用达到设定大小时才会触发日志清理
    unit:str,   #   大小单位，大小单位错误时，默认为MB
    clear_size:float,   #   清理百分之多少日志(0.00~1.00)
    
    """
    global _log_data

    if clear_size >= 1:
        _log_data = ""
        return

    else:
        unit_dict = {
            "KB": 1024,
            "MB": 1048576,
            "GB": 1073741824
        }

        log_bytes = sys.getsizeof(_log_data)
        #   没有单位就默认按MB算
        if log_bytes / unit_dict.get(unit, 1048576) > size:
            _log_data = _log_data[int(len(_log_data) * clear_size):]
            return
        else:
            return


def loadConfig(config_data: dict = {}):
    """
    #   读取配置
    参数说明：
    config_data:dict,   #   配置信息

    没有传入数据或读取失败时将使用默认配置
    """

    global _max_log_size
    global _max_log_size_unit
    global _log_clear_size
    global _sem
    global _debug

    try:
        #   一般在通过web调用时会有config_data，目前千乘尚未支持
        if config_data:
            _max_log_size = config_data.get("log", {}).get("max_log_size", 2)

            _max_log_size_unit = config_data.get("log", {}).get("max_log_size_unit", "MB")

            _log_clear_size = config_data.get("log", {}).get("log_clear_size", 0.5)

            #   当检测到需要Debug时，将日志模式调成Debug输出等级
            if config_data.get("log", {}).get("debug", False):
                logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s\n  %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S", force=True)
                _debug = True
            #   当不需要Debug时，调回去
            else:
                logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s\n  %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S", force=True)
                _debug = False

            _threads_limit = config_data.get("thread", {}).get("threads_limit", 5)
            _sem = threading.Semaphore(_threads_limit)

        #   没受到配置信息就用本地配置文件
        else:
            work_path = os.getcwd()

            config_path = os.path.join(work_path, "config.ini")

            config_data = configparser.ConfigParser()

            config_data.read(config_path, encoding="utf-8")

            _max_log_size = config_data.getint("log", "max_log_size", fallback=2)

            _max_log_size_unit = config_data.get("log", "max_log_size_unit", fallback="MB")

            _log_clear_size = config_data.getfloat("log", "log_clear_size", fallback=0.5)

            if config_data.getboolean("log", "debug", fallback=False):
                logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s\n  %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S", force=True)
                _debug = True
            else:
                logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s\n  %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S", force=True)
                _debug = False

            _threads_limit = config_data.getint("thread", "threads_limit", fallback=5)
            _sem = threading.Semaphore(_threads_limit)

    except Exception as error:
        log("warning", f"SDK配置文件读取失败，将使用默认配置\n  {error}")

        #   Debug
        _debug = False

        #   默认转发线程数量限制
        _threads_limit = 5
        _sem = threading.Semaphore(_threads_limit)

        #   默认最大日志占用内存
        _max_log_size = 2

        #   默认日志大小单位（KB,MB,GB）
        _max_log_size_unit = "MB"

        #   默认清理多少日志（0.00~1.00）
        _log_clear_size = 0.5


def loadTestData(path: str) -> dict:
    """
    #   读取test文件夹下json文件内的数据
    参数说明：
    path:str,   #   json文件路径

    返回dict形式的数据
    读取失败时抛出异常
    """
    try:

        if not os.path.exists(path):
            raise Exception(f"路径错误：\n{path}")

        with open(path, "r", encoding="utf-8") as file:

            data = json.load(file)
            #   校验数据格式
            checkModel(data, models.PLUGIN_TEST_MODEL)

        return data

    except JSONDecodeError:
        raise Exception("json数据文件格式转换错误，请检查json文件的格式")

    except Exception as error:
        raise Exception(f"数据文件 {os.path.basename(path)} 读取失败，原因如下：\n{error}")


def checkModel(data: dict, model) -> dict:
    """
    #   根据models.py内的校验数据校验data内的参数是否符合要求，并尽可能返回规范化的数据
    参数说明：
    data:dict,  #   数据
    model,      #   校验数据

    注意：数据校验很重要

    pydantic库会尝试去规范化进入的数据，即转换原来的数据至规定的格式
    如，123 -> 123.0 （输入为int，规定为float）， False -> "False" （输入为boolean，规定为str）

    校验失败时抛出异常
    """
    try:
        log("info", f"根据 {model.__name__} 校验数据中")

        data = model(**data).json()

        log("info", "校验完成")

        return json.loads(data)

    #   pydantic 会在它正在验证的数据中发现错误时引发 ValidationError
    except ValidationError as errors:
        #   当有多个参数验证不通过时，会有多个错误
        errors = json.loads(errors.json())
        error_log = "数据参数验证不通过"
        for error in errors:
            error_log += f"\n错误参数：{error['loc']}\n错误原因：{error['msg']}"
        raise Exception(error_log)


def transpondData(data: dict, needCheck: bool = True, outputModel: BaseModel = None, dispatcher_url: str = ""):
    """
    #   转发数据
    参数说明：
    data:dict,  #   需要转发的信息
    needCheck:bool, #   是否需要对转发的信息进行出参验证
    outputModel:BaseModel,  #   出参验证model
    dispatcher_url:str,     #   转发的URL
    """
    global _sem
    with _sem:
        if needCheck:
            data = checkModel(data, outputModel)

        log("info", "转发数据中：\n  {}".format(data))

        response = requests.post(dispatcher_url, json=data, verify=False)

        log("info", f"发送完成，状态码：{response.status_code}\n  返回信息：{response.text}")

        return response


def save_update_pack(update_pack: bytes):
    """
    #   将上传的更新包保存到插件根目录的update文件夹下
    参数说明：
    update_pack:bytes,  #   更新包
    """

    work_path = os.getcwd()

    update_packs_dir = os.path.join(work_path, "update")

    if not os.path.exists(update_packs_dir):
        os.mkdir(update_packs_dir)

    temp_pack_path = os.path.join(update_packs_dir, f"{int(time.time())}.tar.gz")

    with open(temp_pack_path, "wb") as file:
        file.write(update_pack)


def hotUpdate(command: str, data: dict = {}):
    """
    #   热更新运行代码
    参数说明：
    command:str,    #   命令：run, http, test
    data:dict,      #   执行载荷

    当有更新包时自动执行更新，没有更新包时跳过更新

    """
    work_path = os.getcwd()

    update_packs_dir = os.path.join(work_path, "update")

    if not os.path.exists(update_packs_dir):
        log("info", "未检测到热更新包，跳过更新环节")
        return False

    else:
        update_packs = os.listdir(update_packs_dir)

    if not update_packs:
        log("info", "未检测到热更新包，跳过更新环节")
        return False

    elif len(update_packs) == 1:
        log("info", "检测到热更新包，执行更新环节")
        update_pack_path = os.path.join(update_packs_dir, update_packs[0])

    elif len(update_packs) > 1:
        log("info", "检测到多个更新包，使用最新传入的更新包执行更新")
        update_pack_path = os.path.join(update_packs_dir, findLatestUpdate(update_packs_dir, update_packs))

    else:
        log("info", "未检测到热更新包，跳过更新环节")
        return False

    try:

        log("info", "创建临时文件夹")

        with tempfile.TemporaryDirectory() as temp_dir:

            log("info", "解压更新包至临时文件夹")
            tar = tarfile.open(update_pack_path, "r:*")

            tar.extractall(temp_dir)

            log("info", "检查版本信息中......")
            if not checkUpdateVersion(os.path.join(temp_dir, "plugin.spec.yaml")):
                return False

            temp_files = os.listdir(temp_dir)

            log("info", "正在覆盖文件")
            for temp_file_name in temp_files:

                resource = os.path.join(temp_dir, temp_file_name)

                #   生成位置
                file_path = os.path.join(os.getcwd(), temp_file_name)

                #   复制
                if os.path.isdir(resource):
                    shutil.copytree(resource, file_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(resource, file_path)

            log("info", "更新完成！")

    except Exception as error:
        error_trace = traceback.format_exc()
        log("error", "热更新执行失败，失败原因：\n  {}\n  详细信息：\n{}".format(error, error_trace))
        log("attention", "将在5秒后重启服务")
        time.sleep(5)
        return False

    return True


def findLatestUpdate(update_packs_dir: str, update_packs: list):
    """
    #   寻找最新传入的更新包
    参数说明：
    update_packs_dir:str,      #   更新包文件夹
    update_packs:list,          #   多个更新包

    返回创建时间最新的文件
    """

    def getCreateTime(update_pack):
        return os.path.getctime(os.path.join(update_packs_dir, update_pack))

    update_packs.sort(key=getCreateTime)

    return update_packs[-1]


def checkUpdateVersion(yaml_path):
    """
    #   检查更新版本
    参数说明：
    yaml_path:str,  #   更新包的yaml暂存文件的绝对路径
    """
    try:
        file_read = open(yaml_path, "r", encoding="utf-8")
        yaml_original = file_read.read()
        file_read.close()
    except UnicodeDecodeError:
        raise Exception("更新包内yaml文件编码格式错误\n  请将yaml文件转成utf-8编码格式")

    except Exception as error:
        raise Exception(f"yaml文件打开失败，错误未知：\n  {error}")

    #   yaml数据读取
    yaml_data = yaml.load(yaml_original, Loader=yaml.FullLoader)

    #   获取更新包版本
    version_pack = yaml_data.get("version", "")

    try:
        file_read = open(os.path.join(os.getcwd(), "plugin.spec.yaml"), "r", encoding="utf-8")
        yaml_original = file_read.read()
        file_read.close()
    except UnicodeDecodeError:
        raise Exception("更新包内yaml文件编码格式错误\n  请将yaml文件转成utf-8编码格式")

    except Exception as error:
        raise Exception(f"yaml文件打开失败，错误未知：\n  {error}")

    #   yaml数据读取
    yaml_data = yaml.load(yaml_original, Loader=yaml.FullLoader)

    #   获取更新包版本
    version_now = yaml_data.get("version", "")

    #   比较版本信息
    if not compareVersion(version_pack, version_now):
        return False

    log("info", "插件更新 {} --> {}".format(version_now, version_pack))

    return True


def compareVersion(version_pack: str, version_now: str):
    """
    #   比较版本号
    参数说明：
    version_pack:str,   #   更新包版本
    version_now:str,    #   目前版本
    """

    if version_pack == version_now:
        log("info", "版本号相同，将执行覆盖更新")
        return True

    version_pack = version_pack.split(".")
    version_now = version_now.split(".")

    if len(version_pack) != 3 or len(version_now) != 3:
        log("error", "版本号格式不正确，请检查版本号设置，并重新传入新的更新包")
        return False

    try:

        if int(version_pack[0]) == int(version_now[0]) \
                and int(version_pack[1]) == int(version_now[1]) \
                and int(version_pack[2]) > int(version_now[2]):
            return True

        if int(version_pack[0]) > int(version_now[0]) or (
                int(version_pack[0]) == int(version_now[0]) and int(version_pack[1]) > int(version_now[1])):
            log("error", "大版本更新请重新安装插件")
            return False

    except:
        log("error", "版本号格式不正确，请检查版本号设置，并重新传入新的更新包")
        return False

    log("error", "更新包版本低于目前插件版本，已放弃更新")
    return False


def setLocalCache(data: dict = {}, cache_name: str = ""):
    """
    #   创建本地临时缓存
    参数说明：
    data:dict,      #   需要缓存的数据
    cache_name:str, #   缓存文件的名称

    创建失败时抛出异常
    """
    log("info", "缓存数据中")
    #   工作区目录
    work_path = os.getcwd()
    #   sdk缓存文件夹目录
    sdkcache_dir_path = os.path.join(work_path, "__sdkcache__")

    try:
        #   创建缓存文件夹
        if not os.path.exists(sdkcache_dir_path):
            os.mkdir(sdkcache_dir_path)
        #   缓存数据位于插件根目录下__sdkcache__文件夹内
        with open(os.path.join(sdkcache_dir_path, f"{cache_name}.chariot.sdkc"), "wb") as cache_file:
            cache_file.write(json.dumps(data).encode())
    except Exception as error:
        error_trace = traceback.format_exc()
        raise Exception("缓存数据失败，失败原因：\n  {}\n  详细信息：\n{}".format(error, error_trace))

    log("info", "缓存完成")


def getLocalCache(cache_name: str = "") -> dict:
    """
    #   获取本地缓存

    获取成功返回dict形式数据，失败时抛出异常
    """

    log("info", "获取缓存数据中")
    #   工作区目录
    work_path = os.getcwd()
    #   sdk缓存文件夹目录
    sdkcache_dir_path = os.path.join(work_path, "__sdkcache__")

    try:
        #   缓存数据位于插件根目录下__sdkcache__文件夹内
        with open(os.path.join(sdkcache_dir_path, f"{cache_name}.chariot.sdkc"), "rb") as cache_file:
            cache = json.loads(cache_file.read().decode())
    except Exception as error:
        error_trace = traceback.format_exc()
        raise Exception("获取缓存数据失败，失败原因：\n  {}\n  详细信息：\n{}".format(error, error_trace))

    log("info", "获取缓存数据成功：\n  {}".format(cache))

    return cache


def clearUpdateFile():
    """
    #   清理更新文件以释放空间

    """
    log("attention", "正在清理更新文件以释放空间")

    update_packs_dir = os.path.join(os.getcwd(), "update")

    if os.path.exists(update_packs_dir):
        for update_pack in os.listdir(update_packs_dir):
            os.remove(os.path.join(update_packs_dir, update_pack))

    log("info", "清理完成")


def popEmpty(params):
    """
    #   采用深度遍历算法剔除载荷中的所有空参数，注意是所有！！！
    #   空参数包括："",{},None,[]
    参数说明：
    params:dict/list,   #   需要剔除空参数的字典或列表

    返回剔除完毕的字典或列表
    """
    p_temp = copy.deepcopy(params)
    if type(params) == dict:
        for k in params:
            if type(params[k]) in [dict, list]:
                temp = popEmpty(p_temp[k])
                if temp in ["", None, {}, []]:
                    p_temp.pop(k)
                else:
                    p_temp[k] = temp
            elif params[k] in ["", None, {}, []]:
                p_temp.pop(k)
        return p_temp
    if type(p_temp) == list:
        p_temp_len = len(p_temp)
        for k in range(p_temp_len):
            if type(p_temp[k]) in [dict, list]:
                temp = popEmpty(p_temp[k])
                if temp in ["", None, {}, []]:
                    p_temp.remove(p_temp[k])
                    return popEmpty(p_temp)
                else:
                    p_temp[k] = temp
            elif p_temp[k] in ["", {}, None, []]:
                p_temp.remove(p_temp[k])
                return popEmpty(p_temp)
        return p_temp
    return p_temp
