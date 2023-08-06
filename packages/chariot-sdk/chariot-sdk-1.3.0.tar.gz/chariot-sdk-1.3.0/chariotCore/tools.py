import yaml
import os
import logging
import shutil
import jinja2
import json
from chariotCore.templates import *
from copy import deepcopy
import configparser
import tarfile

####
#
#   此文件用于存放task.py中所使用的各种方法
#
####

#   需要添加新的预设类型时，请修改typesDict
types_dict = {
    "string": "str",
    "bytes": "str",
    "boolean": "bool",
    "float": "float",
    "date": "str",
    "object": "dict",
    "password": "str",
    "integer": "int",
    "file": "dict",
    "any": "Any"
}

module_dict = {
    "actions": "动作",
    "triggers": "触发器",
    "indicator_receivers": "情报接收器",
    "alarm_receivers": "告警接收器",
    "asset_receivers": "资产接收器"
}

logging.basicConfig(level=logging.DEBUG, format="")


def log(level="debug", msg=""):
    """
    #   设置不同级别的log输出
    参数说明：
    level:str,    #   log等级，levels = debug, info, attention, warning, error, critical
    msg:str,    #   log信息
    """

    msg = str(msg)

    #   输出带颜色log需要执行一次os.system("")
    os.system("")

    if level == "debug":
        logging.debug("\033[32m" + f"{level.upper()} | {msg}" + "\033[0m")

    elif level == "info":
        logging.info(f"{level.upper()} | {msg}")

    elif level == "attention":
        logging.info("\033[94m" + f"{level.upper()} | {msg}" + "\033[0m")

    elif level == "warning":
        logging.warning(
            "\033[93m\n====================== 警 告 ======================\n\n" +
            f"{level.upper()} | {msg}" +
            "\n\n===================================================\n\033[0m")

    elif level == "error":
        logging.error(
            "\033[91m\n====================== 错 误 ======================\n\n" +
            f"{level.upper()} | {msg}" +
            "\n\n===================================================\n\033[0m")

    elif level == "critical":
        logging.critical(
            "\033[91m\n=================== 严 重 错 误 ===================\n\n" +
            f"{level.upper()} | {msg}" +
            "\n\n===================================================\n\033[0m")


def pathCheck(path: str) -> str:
    """
    #   路径检测和文件类型检测
    参数说明：
    path:str,    #   插件定义文件绝对路径

    #   检测不通过时抛出异常
    """

    #   路径检测
    if not os.path.exists(path):
        raise Exception(f"文件路径错误，请检查路径是否正确：\n{path}")

    #   文件类型检测
    if any(path.endswith(end) for end in ["yml", "yaml"]):
        return "yaml"
    elif path.endswith("json"):
        return "json"
    else:
        raise Exception(f"文件类型错误，请检查是否为yaml或json文件：\n{path}")


def readGenerateFile(work_path: str, file_path: str) -> dict:
    """
    #   插件定义文件读取
    参数说明：
    work_path:str,      #   当前工作区绝对路径
    file_path:str,      #   插件定义文件相对路径

    #   以dict形式返回插件定义文件中的数据
    #   读取失败时抛出异常
    """

    #   获取插件定义文件的绝对路径
    file_path = os.path.join(work_path, file_path)

    log("info", "读取插件属性文件中......")

    #   路径检测和文件类型检测
    file_type = pathCheck(file_path)

    if file_type == "yaml":
        #   打开yaml文件
        try:
            file_readbytes = open(file_path, "rb")
            file_bytes = file_readbytes.read()
            file_readbytes.close()

            file_read = open(file_path, "r", encoding="utf-8")
            yaml_original = file_read.read()
            file_read.close()

        except UnicodeDecodeError:
            raise Exception("编码格式错误\n请将yaml文件转成utf-8编码格式")

        except Exception as error:
            raise Exception(f"yaml文件打开失败，错误未知：\n{error}")

        #   yaml数据读取
        data = yaml.load(yaml_original, Loader=yaml.FullLoader)

    elif file_type == "json":
        #   打开json文件
        try:
            file_readbytes = open(file_path, "rb")
            file_bytes = file_readbytes.read()
            file_readbytes.close()

            file_read = open(file_path, "r", encoding="utf-8")
            #   json数据读取
            data = json.load(file_read)
            file_read.close()

        except UnicodeDecodeError:
            raise Exception("编码格式错误\n请将json文件转成utf-8编码格式")

        except Exception as error:
            raise Exception(f"json文件打开失败，错误未知：\n{error}")

    else:
        raise Exception(f"未知的文件类型：{file_type}")

    #   换行格式检测
    if file_bytes.find(b"\r") != -1:
        log("warning", (r"检测到插件定义文件中存在'\r'换行符" + "\n请尽量使用LF换行格式，以防不可知的错误"))

    #   插件必要元数据检测
    log("debug", "检验插件元数据中")
    DataCheck(data)
    log("debug", "插件元数据检验通过")

    log("info", f"插件定义文件读取完成")

    return data


def DataCheck(data: dict):
    """
    #   插件元数据验证
    参数说明：
    data:dict,     #   插件定义数据

    #   缺失必要参数时抛出异常
    """
    error = ""

    if not data.get("plugin_spec_version"):
        error += "plugin_spec_version\n"
    if not data.get("name"):
        error += "name\n"
    if not data.get("title"):
        error += "title\n"
    if not data.get("version"):
        error += "version\n"
    if not data.get("vendor"):
        error += "vendor\n"

    if error:
        error = error[:-1]
        error = "插件定义文件中缺失必要参数：\n" + error
        raise Exception(error)

    name = data.get("name")
    if not name.islower():
        raise Exception(f"插件ID（name）应为全小写：\n{name}")

    if name.find(" ") != -1:
        raise Exception(f'插件ID（name）不能带有空格（" "）\n请用下划线（"_"）代替')


def generateBaseFile(work_path: str):
    """
    #   根据res文件夹的结构生成基础文件
    参数说明：
    work_path:str,    #   当前工作区绝对路径

    #   文件生成失败时抛出异常
    """

    log("info", "生成基础文件中")

    #   获取res文件夹
    res_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "res")
    #   获取res下每个文件名
    files = os.listdir(res_dir)

    #   移除python缓存文件
    try:
        files.remove("__pycache__")
    except:
        pass

    #   逐个遍历生成
    for file_name in files:

        #   跳过范例文件生成
        if any(file_name.endswith(end) for end in ["yml", "yaml", "json"]):
            continue

        try:
            #   基础文件
            res = os.path.join(res_dir, file_name)
            #   生成位置
            file_path = os.path.join(work_path, file_name)

            #   若文件存在则跳过生成
            if os.path.exists(file_path):
                log("attention", rf"\{file_name} 已存在，跳过生成")
                continue
            elif os.path.isdir(res):
                shutil.copytree(res, file_path)
            else:
                shutil.copy2(res, file_path)

            log("info", rf"\{file_name} 生成完成")

        except Exception as error:
            raise Exception(rf"\{file_name} 生成失败，错误未知：" + f"\n{error}")

    log("info", "基础文件生成完成")


def generateTypesModel(types: dict) -> str:
    """
    #   根据插件定义文件中types参数生成自定义类型的校验内容
    参数说明：
    types:dict,    #   插件定义文件中types参数

    返回需要在models.py文件中写入的所有自定义类型的验证内容
    """
    log("info", "生成 自定义类型（types）校验数据中")

    #   所有自定义类型的校验内容
    types_model = ""

    #   获取类名和类的构成参数
    for type_name, type_params in types.items():
        log("info", f"生成 {type_name} 类型校验数据中")

        type_data = {
            #   类名采用全大写
            "className": type_name.upper(),
            #   对类的构成参数进行重构
            "args": argsSetupData(type_name, type_params)
        }
        #   渲染model字符串
        types_model += renderStrTemplate(type_data, model_template)

        log("info", f"{type_name} 类型校验数据生成完成")

    log("info", "自定义类型（types）校验数据生成完成")

    return types_model


def generateConnectionModel(connection_params: dict) -> str:
    """
    #   根据插件定义文件中connection参数生成连接器的入参校验内容
    参数说明：
    connection_params:dict,    #   插件定义文件中connection的载荷

    返回需要在models.py文件中写入的连接器的入参校验内容
    """

    log("info", "生成 连接器（connection）校验数据中")

    connection_data = {
        #   类名采用全大写
        "className": "CONNECTION",
        #   对连接器的参数进行重构
        "args": argsSetupData("connection", connection_params)
    }

    #   渲染model字符串
    connection_model = renderStrTemplate(connection_data, model_template)

    log("info", "连接器（connection）校验数据生成完成")

    return connection_model


def generateModule(data, module, types_model, connection_model, connection_keys):
    """
    #   生成组件
    参数说明：
    data:dict,  #   插件定义数据
    module:str, #   组件
    types_model:str,    #   自定义类型校验数据
    connection_model:str,   #   连接器校验数据
    connection_keys:list of str,    #   连接器参数列表
    """
    module_data = data.get(module)

    if not module_data:
        log("attention", f"未检测到{module_dict[module]}，跳过{module_dict[module]}的生成")
        return []

    #   生成校验数据和校验文件
    generateModel(module, module_data, types_model, connection_model)

    modules_list = generateModuleFile(os.getcwd(), module, module_data, connection_keys)

    return modules_list


def generateModel(module, module_data, types_model, connection_model):
    """
    #   生成校验数据和校验文件
    参数说明：
    module:str, #   组件
    module_data:str,    #   组件数据
    types_model:str,    #   自定义类型校验数据
    connection_model:str,   #   连接器校验数据
    """

    module_model = generateModelData(module, module_data)

    models_dict = {
        "actions": model_header + types_model + connection_model + module_model,
        "triggers": model_header + types_model + connection_model + module_model,
        "alarm_receivers": model_header + alarm_receivers_model_types +
                           types_model + connection_model + module_model,
        "indicator_receivers": model_header + indicator_receivers_model_types +
                               types_model + connection_model + module_model,
        "asset_receivers": model_header + asset_receivers_model_types +
                           types_model + connection_model + module_model
    }

    generateModelFile(os.getcwd(), module, models_dict[module])


def generateModelData(module: str, module_data: dict) -> str:
    """
    #   根据插件定义文件中各个组件的参数生成组件的入参和出参校验数据
    参数说明：
    module:str,     #   组件，module = actions, triggers, indicator_receivers, alarm_receivers, asset_receivers
    module_data:dict,    #   插件定义文件中组件的参数

    返回需要在models.py文件中写入的动作的入参和出参校验数据
    """

    log("info", f"生成 {module_dict[module]}（{module}）校验数据中")

    model = ""

    for module_key, key_params in module_data.items():
        log("info", f"生成 {module_key} 校验数据中")

        #   获取输入与输出载荷
        input_params = key_params.get("input")
        output_params = key_params.get("output")

        input_class_name = module_key.upper() + "_INPUT"
        output_class_name = module_key.upper() + "_OUTPUT"

        log("info", f"生成 {module_key}: input 校验数据中")
        input_data = {
            #   类名采用全大写
            "className": input_class_name,
            #   对输入的参数进行重构
            "args": argsSetupData("input", input_params)
        }
        log("info", f"{module_key}: input 校验数据生成完成")

        log("info", f"生成 {module_key}: output 校验数据中")
        output_data = {
            "module": module,
            "className": output_class_name,
            "args": argsSetupData("output", output_params)
        }
        log("info", f"{module_key}: output 校验数据生成完成")

        model += renderStrTemplate(input_data, model_template)

        #   告警接收器、情报接收器和资产接收器的出参校验数据在转发信息时使用，所以校验数据特殊
        model_template_dict = {
            "alarm_receivers": alarm_receivers_model_template,
            "indicator_receivers": indicator_receivers_model_template,
            "asset_receivers": asset_receivers_model_template
        }

        model += renderStrTemplate(output_data, model_template_dict.get(module, model_template))

        log("info", f"{module_key} 校验数据生成完成")

    log("info", f"{module_dict[module]}（{module}）校验数据生成完成")

    return model


def generateModelFile(work_path: str, model_module: str, model_data: str):
    """
    #   根据目录及校验数据生成校验文件models.py
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    model_module:str,     #   校验的组件，model_module = actions, triggers, indicator_receivers, alarm_receivers
    model_data:str,     #   校验数据

    文件生成失败时抛出异常
    """

    log("info", rf"生成 {model_module}\models.py 校验文件中")

    try:
        #   生成校验对象的文件夹
        path = os.path.join(work_path, model_module)
        if not os.path.exists(path):
            os.mkdir(path)

        #   生成校验文件
        file_path = os.path.join(path, "models.py")
        #   覆盖原有文件
        with open(file_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(model_data)

    except Exception as error:
        raise Exception(rf"{model_module} 的校验文件（models.py）生成失败，错误未知：" + f"\n{error}")

    log("info", rf"{model_module}\models.py 校验文件生成完成")


def generateModuleFile(work_path: str, module: str, module_data: dict, connection_keys: list) -> list:
    """
    #   生成所有组件的文件
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    module:str,     #   组件，module = actions, triggers, indicator_receivers, alarm_receivers
    module_data:dict,    #   组件的参数
    connection_keys:list of str,    #   连接器参数列表

    返回功能列表 key_list，用于生成入口文件 main.py
    文件生成失败时抛出异常
    """

    #   用于记录要在初始化文件（__init__.py）中写入的功能导入（import）
    init_list = []

    #   组件文件夹路径
    module_path = os.path.join(work_path, module)

    log("info", f"生成 {module_dict[module]}（{module}）所有功能中")

    #   遍历组件内每一个功能和功能的参数
    for func_id, params in module_data.items():
        try:

            log("info", rf"生成 {module}\{func_id}.py 文件中")

            #   生成功能数据
            func, func_data, init = generateModuleData(func_id, params, module, connection_keys)

            init_list.append(init)

            #   生成功能文件
            generateFuncFile(module, func_id, func)

        except Exception as error:
            raise Exception(rf"{module}\{func_id}.py 生成失败，原因未知：" + f"\n{error}")

        module_test_template_dict = {
            "actions": actions_test_template,
            "triggers": triggers_test_template,
            "alarm_receivers": alarm_receivers_test_template,
            "indicator_receivers": indicator_receivers_test_template,
            "asset_receivers": asset_receivers_test_template
        }

        #   生成测试用的json文件
        generateTestFile(func_data, module_test_template_dict[module])

    #   生成插件功能初始化文件
    generateInitFile(module, module_path, init_list)

    log("info", f"{module_dict[module]}（{module}）所有功能生成完成")

    #   功能类名称列表 func_class_name_list，用于生成入口文件 main.py
    func_class_name_list = [func[1] for func in init_list]

    return func_class_name_list


def generateFuncFile(module, func_id, func):
    """
    #   生成功能文件
    module:str,     #   组件，module = actions, triggers, indicator_receivers, alarm_receivers, asset_receivers
    func_id:str,    #   功能的id
    func:str,       #   功能的数据
    """

    module_path = os.path.join(os.getcwd(), module)

    func_path = os.path.join(module_path, f"{func_id}.py")

    if os.path.exists(func_path):
        log("attention", rf"{module}\{func_id}.py 已存在，已跳过生成")
    else:
        with open(func_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(func)
        log("info", rf"{module}\{func_id}.py 生成完成")


def generateModuleData(func_id, params, module, connection_keys) -> (str, dict, list):
    """
    #   生成组件内功能数据
    参数说明：
    func_id:str,   #   功能的id
    params:dict,    #   功能的参数，包括title、input等，重点是input
    module:str,     #   组件，module = actions, triggers, indicator_receivers, alarm_receivers, asset_receivers
    connection_keys:list of str,    #   连接器参数列表
    """

    init = None

    class_name_dict = {
        "actions": "_ACTION",
        "triggers": "_TRIGGER",
        "alarm_receivers": "_ALARM_RECEIVER",
        "indicator_receivers": "_INDICATOR_RECEIVER",
        "asset_receivers": "_ASSET_RECEIVER"
    }

    module_template_dict = {
        "actions": action_template,
        "triggers": triggers_template,
        "alarm_receivers": alarm_receivers_template,
        "indicator_receivers": indicator_receivers_template,
        "asset_receivers": asset_receivers_template
    }

    class_name = func_id.upper() + class_name_dict[module]

    #   用于记录要在初始化文件（__init__.py）中写入的功能导入（import）
    #   同时用于生成入口文件 main.py
    init = (func_id, class_name)

    #   这里收集input的key是为了自动生成获取数据的功能
    if params.get("input"):
        input_keys = list(params["input"].keys())
    else:
        input_keys = []

    func_data = {
        "name": func_id,
        "inputModel": func_id.upper() + "_INPUT",
        "outputModel": func_id.upper() + "_OUTPUT",
        "connModel": "CONNECTION",
        "connectionKeys": connection_keys,
        "inputKeys": input_keys,
        "className": class_name
    }

    func = renderStrTemplate(func_data, module_template_dict[module])

    return func, func_data, init


def autoGenerateDataTrans(data: dict) -> dict:
    """
    #   将用于自动生成插件的插件特殊定义数据重新整理为一般的插件定义数据
    #   特殊定义文件相较于一般的插件定义文件在每个功能上的input参数下都对各个需要输入的数据进行了分类
    #   这一举措是为了确定输入的数据属于构成一次请求中的哪一部分
    参数说明：
    data:dict,      #   特殊定义文件的数据
    """

    log("info", "转换插件定义文件中")

    #   深拷贝一份数据用于操作
    new_data = deepcopy(data)

    #   用于统一化变量名称，以防出现变量名在python中不可用
    value_id = 0

    #   转换连接器
    connection_data = data.get("connection", {})
    new_data["connection"] = {}
    for value_type in connection_data:
        for value in connection_data[value_type]:
            #   构建新的统一参数名和旧参数名的映射
            connection_data[value_type][value]["@origin"] = value
            #   把参数属于哪一类也塞进去
            connection_data[value_type][value]["@type"] = value_type
            new_data["connection"][f"value_{value_id}"] = connection_data[value_type][value]
            value_id += 1

    #   用于重新计数
    value_temp = value_id

    #   转换动作
    actions_data = data.get("actions")

    #   遍历动作的每一个功能
    for func in actions_data:
        new_data["actions"][func]["input"] = {}

        #   有时候GET请求啥参数也没有
        if not actions_data[func].get("input"):
            continue

        #   遍历功能的input部分每一个参数分类
        for value_type in actions_data[func]["input"]:
            #   遍历每一个参数分类下的参数
            for value in actions_data[func]["input"][value_type]:
                #   构建新的统一参数名和旧参数名的映射
                actions_data[func]["input"][value_type][value]["@origin"] = value
                #   把参数属于哪一类也塞进去
                actions_data[func]["input"][value_type][value]["@type"] = value_type
                new_data["actions"][func]["input"][f"value_{value_id}"] = actions_data[func]["input"][value_type][value]
                value_id += 1

        value_id = value_temp

    return new_data


def autoGeneratePluginSpecFile(data: dict):
    """
    #   从特殊定义文件中自动生成一般插件定义文件
    #   一个插件总得有个定义文件不是吗？
    参数说明：
    data:dict,      #   特殊定义文件的数据
    """
    with open("plugin.spec.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def autoGenerateActionsFile(work_path: str, module_data: dict) -> list:
    """
    #   生成请求API专用的动作运行文件
    #   大部分API接口只需要构造简单的Requests就能直接调用，因此可以高度模板化，减少开发时间
    #   与“生成所有功能的运行文件”方法不同的是，高度模板化带来的是更多详细参数的需求，其他方面则无太大区别
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    module_data:dict,    #   组件的参数
    """

    #   用于记录要在初始化文件（__init__.py）中写入的功能导入（import）
    init_list = []

    #   功能列表 key_list，用于生成入口文件 main.py
    key_list = []

    #   组件文件夹路径
    key_path = os.path.join(work_path, "actions")

    #   获取连接器数据
    connection_url_params_keys = []
    connection_headers_keys = []
    connection_params_keys = []
    connection_body_keys = []
    connection_files_keys = []
    connection_ssl_verify = ()
    for value, value_params in module_data.get("connection", {}).items():
        if value_params["@type"] == "url_params":
            connection_url_params_keys.append((value, value_params["@origin"]))
        elif value_params["@type"] == "headers":
            connection_headers_keys.append((value, value_params["@origin"]))
        elif value_params["@type"] == "params":
            connection_params_keys.append((value, value_params["@origin"]))
        elif value_params["@type"] == "body":
            connection_body_keys.append((value, value_params["@origin"]))
        elif value_params["@type"] == "files":
            connection_files_keys.append((value, value_params["@origin"]))
        elif value_params["@type"] == "ssl_verify":
            connection_ssl_verify = (value, value_params["@origin"])

    #   遍历组件内每一个功能和功能的参数
    for module_key, params in module_data.get("actions", {}).items():
        try:

            log("info", rf"生成 actions\{module_key}.py 文件中")

            #   存储用于渲染功能文件内容的数据
            key_data = {}

            #   功能类名采用全大写
            key_class_name = module_key.upper() + "_ACTION"
            key_data["actionsName"] = key_class_name

            init_list.append([module_key, key_class_name])

            #   设定渲染模板
            key_template = action_rest_template
            key_test_template = actions_test_template

            #   功能列表，用于生成入口文件 main.py
            key_list.append(key_class_name)

            #   设置input, output类名
            input_class_name = module_key.upper() + "_INPUT"
            output_class_name = module_key.upper() + "_OUTPUT"

            #   获取动作数据
            run_url_params_keys = []
            run_headers_keys = []
            run_params_keys = []
            run_body_keys = []
            run_files_keys = []
            run_ssl_verify = ()

            for value in params["input"]:
                if params["input"][value]["@type"] == "url_params":
                    run_url_params_keys.append((value, params["input"][value]["@origin"]))
                elif params["input"][value]["@type"] == "headers":
                    run_headers_keys.append((value, params["input"][value]["@origin"]))
                elif params["input"][value]["@type"] == "params":
                    run_params_keys.append((value, params["input"][value]["@origin"]))
                elif params["input"][value]["@type"] == "body":
                    run_body_keys.append((value, params["input"][value]["@origin"]))
                elif params["input"][value]["@type"] == "files":
                    run_files_keys.append((value, params["input"][value]["@origin"]))
                elif params["input"][value]["@type"] == "ssl_verify":
                    run_ssl_verify = (value, params["input"][value]["@origin"])

            #   获取请求方式
            method = params["method"]
            #   获取URL
            url = params["url"]
            #   对URL中的参数进行整理
            for url_param in connection_url_params_keys:
                url = str(url).replace("{" + f"{url_param[1]}" + "}", "{self." + url_param[0] + "}")
            for url_param in run_url_params_keys:
                url = str(url).replace("{" + url_param[1] + "}", "{self." + url_param[0] + "}")

            #   获取请求体类型
            body_type = params.get("body_type", None)

            key_data.update({
                "name": module_key,
                "inputModel": input_class_name,
                "outputModel": output_class_name,
                "connModel": "CONNECTION",
                "method": method,
                "url": url,
                "body_type": body_type,
                "connection_url_params_keys": connection_url_params_keys,
                "connection_headers_keys": connection_headers_keys,
                "connection_params_keys": connection_params_keys,
                "connection_body_keys": connection_body_keys,
                "connection_files_keys": connection_files_keys,
                "connection_ssl_verify": connection_ssl_verify,
                "run_url_params_keys": run_url_params_keys,
                "run_headers_keys": run_headers_keys,
                "run_params_keys": run_params_keys,
                "run_body_keys": run_body_keys,
                "run_files_keys": run_files_keys,
                "run_ssl_verify": run_ssl_verify
            })

            #   渲染组件内不同功能文件内容
            key = renderStrTemplate(key_data, key_template)

            file_path = os.path.join(key_path, f"{module_key}.py")

            with open(file_path, "w", encoding="utf-8", newline="\n") as file:
                file.write(key)

            log("info", rf"actions\{module_key}.py 生成完成")

        except Exception as error:
            raise Exception(rf"actions\{module_key}.py 生成失败，原因未知：" + f"\n{error}")

        #   生成测试用的json文件
        generateTestFile(key_data, key_test_template)

    generateInitFile("actions", key_path, init_list)

    log("info", f"{module_dict['actions']}（actions）所有功能生成完成")

    return key_list


def generateTestFile(func_data, func_test_template):
    """
    #   生成测试用的json文件
    参数说明：
    func_data:dict,     #   功能的各项参数
    key_test_template:str,  #   需要渲染的测试文件模板
    生成失败时抛出异常
    """

    module_key = func_data.get("name")

    if not module_key:
        raise Exception("功能名称缺少")

    log("info", rf"生成 tests\{module_key}.json 测试文件中")

    try:

        connection_params_dict = {}
        for key in func_data.get("connectionKeys", []):
            connection_params_dict[key] = None

        func_data["connectionKeys"] = json.dumps(connection_params_dict)

        input_params_dict = {}
        for key in func_data.get("inputKeys", []):
            input_params_dict[key] = None

        func_data["inputKeys"] = json.dumps(input_params_dict)

        #   渲染测试文件内容
        test = renderStrTemplate(func_data, func_test_template)

        tests_path = os.path.join(os.getcwd(), "tests")
        file_path = os.path.join(tests_path, f"{module_key}.json")
        #   当测试文件存在时不写入，以防覆盖原本的测试数据
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8", newline="\n") as file:
                file.write(test)

        else:
            log("attention", rf"tests\{module_key}.json 测试文件已存在，已跳过生成")

        log("info", rf"tests\{module_key}.json 测试文件生成完成")

    except Exception as error:
        raise Exception(f"{module_key}.json 动作测试文件生成失败，原因未知：" + f"\n{error}")


def generateInitFile(module, key_path, init_list):
    """
    #   生成插件功能初始化文件
    module:str,     #   组件
    key_path:str,   #   生成位置
    init_list:list, #   功能导入列表
    """
    try:
        log("info", rf"生成 初始化文件 {module}\__init__.py 中")
        file_path = os.path.join(key_path, "__init__.py")
        template_data = {
            "init_list": init_list,
            "module": module
        }
        init = renderStrTemplate(template_data, init_template)
        with open(file_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(init)
        log("info", rf"初始化文件 {module}\__init__.py 生成完成")
    except Exception as error:
        raise Exception(rf"初始化文件 {module}\__init__.py 生成失败，原因未知：" + f"\n{error}")


def updateModuleFile(work_path: str):
    """
    #   对1.2.6版本sdk做的actions, triggers, alarm_receivers, indicator_receivers进行兼容性改动，主要改动为规范化类名
    #   对1.2.7版本所使用的去除空参数功能进行修正
    #   对旧requirements.txt添加python-multipart库
    #   对1.3.0版本之前的Dockerfile进行修正

    参数说明：
    work_path:str,    #   当前工作区绝对路径

    **该方法预计在将来某一个版本中会被删除**

    改动失败时抛出异常
    """
    modules = ["action", "trigger", "alarm_receiver", "indicator_receiver"]

    try:

        #   遍历每一个模块
        for module in modules:
            path = os.path.join(work_path, module + "s")

            if os.path.exists(path):
                files = os.listdir(path)

                #   遍历每一个文件
                for file in files:

                    #   排除可能存在的缓存文件
                    if file.endswith(".py") and file != "models.py":
                        file_path = os.path.join(path, file)

                        with open(file_path, "r", encoding="utf-8") as f:
                            data = f.read()

                            #   旧文件一般类名命名方式都是 f"{功能名}{模块名}S"，如
                            #   "EXAMPLEACTIONS"，模块名不够清晰，因此需要规范
                            #   新文件类命名方式则采用 f"{功能名}_{模块名}"，如 "EXAMPLE_ACTION"

                            if data.find(module.upper() + "S") != -1 and data.find("_" + module.upper()) == -1:
                                log("attention", rf"检测到旧版本的功能文件 \{module}\{file}，执行兼容性更新")

                                data = data.replace(module.upper() + "S", "_" + module.upper())
                                data = data.replace("INPUT", "_INPUT")
                                data = data.replace("OUTPUT", "_OUTPUT")
                                data = data.replace(" Core\r\n", " *\r\n")  # CRLF
                                data = data.replace(" Core\n", " *\n")  # LF
                                data = data.replace("# 初始化\r\n",
                                                    "# 初始化\r\n        super().__init__()\r\n")  # CRLF
                                data = data.replace("# 初始化\n",
                                                    "# 初始化\n        super().__init__()\n")  # LF
                                log("attention", "兼容性更新完成")

                            #   1.2.8对清除空参数的方法进行了重写，并且更改为全局可用

                            if data.find("self._popEmpty") != -1:
                                data = data.replace("self._popEmpty", "popEmpty")

                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(data)
            else:
                pass

        requirements_path = os.path.join(work_path, "requirements.txt")
        if os.path.exists(requirements_path):
            with open(requirements_path, "r", encoding="utf-8") as f:
                data = f.read()
            if data.find("python-multipart") == -1:
                with open(requirements_path, "a", encoding="utf-8") as f:
                    f.write("\npython-multipart\n")

        config_path = os.path.join(work_path, "config.ini")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = f.read()
            if "[ignore]" not in data:
                data += "\n[ignore]\n#   打包时忽略的根目录下的文件\n#   以逗号分隔多个文件（文件夹）\nignore = env,venv,tests,.git,.vs,.gitignore,.idea,__sdkcache__,__pycache__,temp_image.tar.gz,temp_plugin.tar.gz"
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(data)

    except Exception as error:
        raise Exception(f"兼容措施执行失败，错误未知：\n{error}")


def generateMainFile(work_path: str, plugin_name: str,
                     modules_list_dict: dict):
    """
    #   生成入口文件
    参数说明：
    work_path:str,      #   当前工作区绝对路径
    plugin_name:str,    #   插件名称
    modules_list_dict:dict,     #   组件的功能列表的字典

    生成失败时抛出异常
    """

    log("info", r"生成入口文件 \main.py 中")

    try:
        main_data = {
            "pluginName": plugin_name.upper() + "_PLUGIN",
        }

        main_data.update(modules_list_dict)

        file_path = os.path.join(work_path, "main.py")

        main_data = renderStrTemplate(main_data, main_template)

        with open(file_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(main_data)

    except Exception as error:
        raise Exception(r"入口文件 \main.py 生成失败，错误未知：" + f"\n{error}")

    log("info", r"入口文件文件 \main.py 生成完成")


def generateHelpFile(yaml_data: dict):
    """
    #   生成帮助文件
    参数说明：
    yaml_data:dict,     #   yaml文件数据

    **此方法生成的文件基本用不上，预计在将来版本删除**

    生成失败时抛出异常
    """

    log("info", r"生成帮助文件 \help.md 中")

    try:
        file_path = os.path.join(os.getcwd(), "help.md")
        help_data = renderStrTemplate(yaml_data, help_template)
        with open(file_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(help_data)

    except Exception as error:
        raise Exception(r"生成帮助文件 \help.md 失败，原因未知：" + f"\n{error}")

    log("info", r"帮助文件 \help.md 生成完成")


def generateUtilFile(work_path: str):
    """
    #   生成通用文件存储的文件夹，在此文件夹下放置各个功能需要共用的方法
    参数说明：
    work_path:str,      #   当前工作区绝对路径

    生成失败时抛出异常
    """

    log("info", r"生成通用文件存储文件夹 \util 中")

    try:
        util_path = os.path.join(work_path, "util")

        if not os.path.exists(util_path):
            os.mkdir(util_path)
        else:
            log("attention", r"\util 文件夹已存在，已跳过生成")

    except Exception as error:
        raise Exception(r"通用文件存储文件夹 \util 失败，原因未知：" + f"\n{error}")

    log("info", r"通用文件存储文件夹 \util 生成完成")


def generateUpdateFile(work_path: str):
    """
    #   生成热更新时源码包的存放文件夹
    参数说明：
    work_path:str,      #   当前工作区绝对路径

    生成失败时抛出异常
    """
    log("info", r"生成热更新源码包存储文件夹 \update 中")

    try:
        update_path = os.path.join(work_path, "update")

        if not os.path.exists(update_path):
            os.mkdir(update_path)
        else:
            log("attention", r"\update 文件夹已存在，已跳过生成")

    except Exception as error:
        raise Exception(r"热更新源码包存储文件夹 \update 失败，原因未知：" + f"\n{error}")

    log("info", r"热更新源码包存储文件夹 \update 生成完成")


def generateTestServerFile(work_path: str,
                           actions_list: list,
                           triggers_list: list,
                           indicator_receivers_list: list,
                           alarm_receivers_list: list):
    """
    **此方法暂时弃用**

    #   生成本地REST测试服务器文件
    参数说明：
    work_path:str,      #   当前工作区绝对路径
    actions_list:list,      #   动作列表
    triggers_list:list,     #   触发器列表
    indicator_receivers_list:list,      #   情报接收器列表
    alarm_receivers_list:list,          #   告警接收器列表

    生成失败时抛出异常
    """

    log("info", r"生成本地REST测试服务器数据文件 \testserver.py 中")

    testserver_file_content = testserver_head_template

    if actions_list:

        testserver_file_content = "\nfrom actions import *" + testserver_file_content

        for action in actions_list:
            action_data = {
                "class_name": action,
                "name": action.replace("_ACTION", "").lower()
            }

            testserver_file_content += renderStrTemplate(action_data, testserver_actions_template)

    if triggers_list:

        testserver_file_content = "\nfrom triggers import *" + testserver_file_content

        for trigger in triggers_list:
            trigger_data = {
                "class_name": trigger,
                "name": trigger.replace("_TRIGGER", "").lower()
            }

            testserver_file_content += renderStrTemplate(trigger_data, testserver_triggers_template)

    if indicator_receivers_list:

        testserver_file_content = "\nfrom indicator_receivers import *" + testserver_file_content

        for indicator_receiver in indicator_receivers_list:
            indicator_receiver_data = {
                "class_name": indicator_receiver,
                "name": indicator_receiver.replace("_INDICATOR_RECEIVER", "").lower()
            }

            testserver_file_content += renderStrTemplate(indicator_receiver_data,
                                                         testserver_indicator_receivers_template)

    if alarm_receivers_list:

        testserver_file_content = "\nfrom alarm_receivers import *" + testserver_file_content

        for alarm_receiver in alarm_receivers_list:
            alarm_receiver_data = {
                "class_name": alarm_receiver,
                "name": alarm_receiver.replace("_ALARM_RECEIVER", "").lower()
            }

            testserver_file_content += renderStrTemplate(alarm_receiver_data, testserver_alarm_receivers_template)

    testserver_file_content += testserver_tail_template

    try:

        testserver_file_path = os.path.join(work_path, "testserver.py")

        with open(testserver_file_path, "w", encoding="utf-8") as file:

            file.write(testserver_file_content)

    except Exception as error:
        raise Exception(rf"本地REST测试服务器数据文件 \testserver.py 生成失败 \n   {error}")

    log("info", r"本地REST测试服务器数据文件 \testserver.py 生成完成")


def argsSetupData(param_name: str, params: dict) -> list:
    """
    #   整理构成参数方便调用
    参数说明：
    param_name:str,     #   集合名称（自定义类名称、输入集合名称、输出集合名称）
    params:dict,    #   构成参数

    将构成参数整理成：
    [['值1', "Literal['枚举值1','枚举值2'] = 默认值"], ['值2', '类型 = 默认值'],['值3','Optional[List[类型]] = 默认值']]

    例如：
    [['value1', 'dict = None'], ['value2', "Literal['123', '321'] = None"]]

    构成参数中的关键数据：
    构成参数的类型（type）   #   在出现枚举集合时，可缺失，其他情况下不可缺失
    是否必填（required）  #   可缺失，缺省为False
    默认值（default）    #   可缺失
    枚举集合（enum）   #   可缺失，缺省为None
    """
    params_list = []

    if params:
        #   从构成参数中提取必要的数据
        for value, value_param in params.items():
            #   构成参数的类型
            value_type = value_param.get("type")

            #   是否必填
            value_required = value_param.get("required", False)

            #   默认值
            value_default = value_param.get("default")

            #   枚举值
            value_enum = value_param.get("enum")

            #   检验构成参数的必要数据是否符合规范
            log("debug", f"检验 {value} 的构成参数中")
            paramsCheck(value_type, value_default, value_enum)
            log("debug", f"{value} 的构成参数检验通过")

            #   根据typesDict将不同类型转换成python中的类型，在默认值和枚举集合存在时附加两者
            value_type = typeTransform(value_type, value_required, value_default, value_enum)

            params_list.append([value, value_type])

    else:
        log("attention", f"{param_name} 为空，已跳过 {param_name} 校验数据生成")

    return params_list


def paramsCheck(value_type: str, value_default, value_enum: list):
    """
    #   检验构成参数的必要数据是否符合规范
    参数说明：
    value_type,     #   参数类型
    value_default:,    #   构成参数的默认值
    value_enum,     #   构成参数的枚举集合

    #   检验不通过时抛出异常
    """
    if not value_type and not value_enum:
        raise Exception(f"类型与枚举集合都为空\n类型（type）与枚举集合（enum）请至少填写一项")

    if value_type and not types_dict.get(value_type):
        if value_type.startswith("[]") and not types_dict.get(value_type[2:]):
            log("attention", f"未知类型的列表组合：{value_type}，如果是自定义类型请忽略此信息")
        elif not value_type.startswith("[]") and not types_dict.get(value_type[2:]):
            log("attention", f"未知的类型：{value_type}，如果是自定义类型请忽略此信息")

    if value_enum and not isinstance(value_enum, list):
        raise Exception("枚举集合（enum）填写不符合规范")

    if value_default and value_enum and value_default not in value_enum:
        raise Exception(f"默认值 {value_default}\n无法在枚举的集合中找到")

    if value_enum == []:
        raise Exception("枚举集合为空集：[]")


def typeTransform(value_type: str, value_required: bool, value_default: None, value_enum: None):
    """
    #   根据typesDict将不同类型转换成python中的类型，在默认值和枚举集合存在时附加两者
    参数说明：
    value_type:str,     #   参数类型
    value_default:Any type,    #   构成参数的默认值
    value_enum:list,     #   构成参数的枚举集合

    默认值在 required = true 且无 default 参数时为空，默认值在 required = false 时且无 default 参数时为None

    例如：
    ['error1', 'dict =  None']
    ['error_code1', "Literal[['123', '321'], ['124', '321']]"]
    ['error2','Optional[List[dict]] = None']
    ['error_code2', 'Optional[List[TEST_TYPE]] = None']
    ['error_code2', "Literal['123','321'] = None"]
    """
    #   存在枚举集合时
    if value_enum:
        argType = f"Literal{value_enum}"

    #   非枚举集合时，尝试从typeDict中获取预设类
    else:
        argType = types_dict.get(value_type)

    #   无法直接获取到预设类
    if not argType:

        #   是否为列表
        if value_type.startswith("[]"):

            #   查看是否为预设类的列表形式
            #   Optional，意为此参数可以为None或已经声明的类型
            if types_dict.get(value_type[2:]):
                #   预设类的列表形式将直接取预设类型的 列表 形式
                argType = f"Optional[List[{types_dict.get(value_type[2:])}]]"
            else:
                #   非预设类的列表形式将取自定义类型的全大写的 列表 形式
                argType = f"Optional[List[{value_type[2:].upper()}]]"

        else:
            #   非预设类直接采用自定义类型的全大写形式
            argType = value_type.upper()

    #   不需要必填且没有默认值时，则默认值给None，这样在运行测试时，非必填的参数能够通过参数校验
    if not value_required and value_default is None:
        argType += " = None"

    #   当存在默认值时，则给默认值
    elif value_default is not None:
        #   注意，当默认值为字符串时，要加 ""
        if isinstance(value_default, str):
            argType += f' = "{value_default}"'
        else:
            argType += f" = {value_default}"

    return argType


def renderStrTemplate(data: dict, template):
    """
    #   根据templates.py内的模板渲染字符串
    参数说明：
    data,     #     需要渲染的数据
    template,    #      渲染的模板
    """
    template = jinja2.Template(template)
    res = template.render(data)

    return res


def loadIgnore():
    """
    #   读取忽略文件配置

    没有传入数据或读取失败时将返回空列表
    """
    log("info", "读取配置文件中")
    work_path = os.getcwd()
    config_path = os.path.join(work_path, "config.ini")
    try:
        if os.path.exists(config_path):
            config_data = configparser.ConfigParser()
            config_data.read(config_path, encoding="utf-8")
            ignore = config_data.get("ignore", "ignore", fallback="")
            ignore = ignore.split(",")
            return ignore
        else:
            log("attention", "未找到配置文件")
            return []
    except Exception as error:
        log("warning", f"读取配置文件失败\n{error}")
        return []


def tarballOnlinePack(pack_name: str = ""):
    """
    参数说明：
    pack_name:str,    #   包名称，不提供则根据插件定义文件自动生成

    返回插件定义文件的数据
    """

    work_path = os.getcwd()

    data = readGenerateFile(work_path, "plugin.spec.yaml")

    #   获取插件定义文件中的元数据
    vendor = data["vendor"]
    name = data["name"]
    version = data["version"]

    #   在线包文件名
    if pack_name:
        tar_name = pack_name
    else:
        tar_name = f"{vendor}-{name}-{version}.tar.gz"

    #   排除可能存在的离线包
    offline_name = f"{vendor}-{name}-{version}-offline.tar.gz"

    tar = tarfile.open(os.path.join(work_path, tar_name), "w:gz", format=tarfile.GNU_FORMAT)

    #   默认排除项
    ignore = ["__sdkcache__", "__pycache__", offline_name, f"{vendor}-{name}-{version}.tar.gz"]

    ignore.extend(loadIgnore())

    #   去重
    ignore = list(set(ignore))

    for file in os.listdir(work_path):
        if file in ignore:
            log("info", f"{file}已忽略")
            continue
        else:
            tar.add(os.path.join(work_path, file), arcname=file)

    tar.close()

    return data
