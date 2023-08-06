from typing import List
from pydantic import BaseModel


#   插件定义文件结构，用于自动生成插件
class PLUGIN_CONSTRUCTION(BaseModel):
    plugin_spec_version: str = "v2"
    name: str
    version: str
    hot_update: bool = True
    auto_generate: bool = True
    title: dict
    description: dict = None
    vendor: str = "chariot"
    tags: List[str] = None
    connection: dict = None
    actions: dict


#   执行数据验证类，用于传入插件数据的验证
class PLUGIN_TEST_MODEL(BaseModel):
    version: str
    type: str
    body: dict


class DISPATCHER(BaseModel):
    url: str = "http://127.0.0.1:10001/transpond"
    cache_url: str = ""


class BODY_MODEL(BaseModel):
    meta: dict = {}
    connection: dict = {}
    dispatcher: DISPATCHER = None
    input: dict = {}
    enable_web: bool = False
    config: dict = {}


class ACTION_TEST_BODY_MODEL(BODY_MODEL):
    action: str


class TRIGGER_TEST_BODY_MODEL(BODY_MODEL):
    trigger: str
    dispatcher: DISPATCHER


class ALARM_RECEIVER_TEST_BODY_MODEL(BODY_MODEL):
    alarm: str
    dispatcher: DISPATCHER


class INDICATOR_RECEIVER_TEST_BODY_MODEL(BODY_MODEL):
    receiver: str
    dispatcher: DISPATCHER


class ASSET_RECEIVER_TEST_BODY_MODEL(BODY_MODEL):
    asset: str
    dispatcher: DISPATCHER


class ACTION_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "action"
    body: ACTION_TEST_BODY_MODEL


class TRIGGER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "trigger"
    body: TRIGGER_TEST_BODY_MODEL


class ALARM_RECEIVER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "alarm_receiver"
    body: ALARM_RECEIVER_TEST_BODY_MODEL


class INDICATOR_RECEIVER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "indicator_receiver"
    body: INDICATOR_RECEIVER_TEST_BODY_MODEL


class ASSET_RECEIVER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "asset_receiver"
    body: ASSET_RECEIVER_TEST_BODY_MODEL
