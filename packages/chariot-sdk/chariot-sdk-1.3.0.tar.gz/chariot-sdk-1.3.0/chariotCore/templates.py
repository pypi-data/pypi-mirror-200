
#   不要在此文件使用任何缩进格式化功能！
#   不要在此文件使用任何缩进格式化功能！
#   不要在此文件使用任何缩进格式化功能！

model_header = """
from pydantic import BaseModel
from typing import *

# 可自行修改增加校验精准度

"""

model_template = """
class {{ className }}(BaseModel):
    {% if args %}{% for argName, argType in args %}
    {{ argName }}: {{ argType }}
    {% endfor %}{% else %}
    ...
    {% endif %}"""

action_template = """
from SDK.subassembly import Actions
from SDK.base import *

from .models import {{ connModel }}, {{ inputModel }}, {{ outputModel }}



class {{ className }}(Actions):

    def __init__(self):
        #   初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.connModel = {{ connModel }}


    def connection(self, data={}):
        #   write your code
        {% if connectionKeys %}{% for key in connectionKeys %}
        {{ key }} = data.get("{{ key }}"){% endfor %}{% else %}
        ...    
        {% endif %}
    
    def run(self, params={}):
        #   write your code
        #   可调用 popEmpty() 去除载荷中的空参数
        #   使用 setLocalCache()、getLocalCache() 管理本地缓存
        {% if inputKeys %}{% for key in inputKeys %}
        {{ key }} = params.get("{{ key }}"){% endfor %}{% else %}
        ...
        {% endif %}
"""

triggers_template = """
from SDK.subassembly import Triggers
from SDK.base import *

from .models import {{ connModel }}, {{ inputModel }}, {{ outputModel }}



class {{ className }}(Triggers):

    def __init__(self):
        #   初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.connModel = {{ connModel }}


    def connection(self, data={}):
        #   write your code
        {% if connectionKeys %}{% for key in connectionKeys %}
        {{ key }} = data.get("{{ key }}"){% endfor %}{% else %}
        ...    
        {% endif %}

    def run(self, params={}):
        #   write your code
        #   可调用 popEmpty() 去除载荷中的空参数
        #   使用 self.setCache() 设置在线缓存
        #   使用 setLocalCache()、getLocalCache() 管理本地缓存
        #   返回必须使用 self.send({})
        {% if inputKeys %}{% for key in inputKeys %}
        {{ key }} = params.get("{{ key }}"){% endfor %}{% else %}
        ...
        {% endif %}
"""


alarm_receivers_template = """
from SDK.subassembly import AlarmReceivers
from SDK.base import *

from .models import {{ connModel }}, {{ inputModel }}, {{ outputModel }}



class {{ className }}(AlarmReceivers):

    def __init__(self):
        #   初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.connModel = {{ connModel }}


    def connection(self, data={}):
        #   write your code
        {% if connectionKeys %}{% for key in connectionKeys %}
        {{ key }} = data.get("{{ key }}"){% endfor %}{% else %}
        ...    
        {% endif %}

    def run(self, params={}):
        #   write your code
        #   可调用 popEmpty() 去除载荷中的空参数
        #   返回必须使用 self.send({})
        #   使用 self.setCache() 设置在线缓存
        #   使用 setLocalCache()、getLocalCache() 管理本地缓存
        {% if inputKeys %}{% for key in inputKeys %}
        {{ key }} = params.get("{{ key }}"){% endfor %}{% else %}
        ...
        {% endif %}

"""


indicator_receivers_template = """
from SDK.subassembly import IndicatorReceivers
from SDK.base import *

from .models import {{ connModel }}, {{ inputModel }}, {{ outputModel }}



class {{ className }}(IndicatorReceivers):

    def __init__(self):
        #   初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.connModel = {{ connModel }}


    def connection(self, data={}):
        #   write your code
        {% if connectionKeys %}{% for key in connectionKeys %}
        {{ key }} = data.get("{{ key }}"){% endfor %}{% else %}
        ...    
        {% endif %}

    def run(self, params={}):
        #   write your code
        #   可调用 popEmpty() 去除载荷中的空参数
        #   使用 self.setCache() 设置在线缓存
        #   使用 setLocalCache()、getLocalCache() 管理本地缓存
        #   返回必须使用 self.send({})
        {% if inputKeys %}{% for key in inputKeys %}
        {{ key }} = params.get("{{ key }}"){% endfor %}{% else %}
        ...
        {% endif %}

"""

asset_receivers_template = """
from SDK.subassembly import AssetReceivers
from SDK.base import *

from .models import {{ connModel }}, {{ inputModel }},{{ outputModel }}



class {{ className }}(AssetReceivers):

    def __init__(self):
        #   初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.connModel = {{ connModel }}


    def connection(self, data={}):
        #   write your code
        {% if connectionKeys %}{% for key in connectionKeys %}
        {{ key }} = data.get("{{ key }}"){% endfor %}{% else %}
        ...    
        {% endif %}

    def run(self, params={}):
        #   write your code
        #   可调用 popEmpty() 去除载荷中的空参数
        #   返回必须使用 self.send({})
        #   使用 self.setCache() 设置在线缓存
        #   使用 setLocalCache()、getLocalCache() 管理本地缓存
        {% if inputKeys %}{% for key in inputKeys %}
        {{ key }} = params.get("{{ key }}"){% endfor %}{% else %}
        ...
        {% endif %}


"""


action_rest_template = """
from SDK.subassembly import Actions
from SDK.base import *

import requests

from .models import {{ connModel }}, {{ inputModel }},{{ outputModel }}

import requests
import base64
import tempfile

class {{ actionsName }}(Actions):

    def __init__(self):
        #   初始化
        super().__init__()
        self.name = "{{ name }}"
        self.inputModel = {{ inputModel }}
        self.outputModel = {{ outputModel }}
        self.connModel = {{ connModel }}

    def connection(self, data={}):
        #   write your code
        {% for key in connection_url_params_keys %}
        self.{{ key[0] }} = data.get("{{ key[0] }}"){% endfor %}
        {% for key in connection_headers_keys %}
        self.{{ key[0] }} = data.get("{{ key[0] }}"){% endfor %}
        {% for key in connection_params_keys %}
        self.{{ key[0] }} = data.get("{{ key[0] }}"){% endfor %}
        {% for key in connection_body_keys %}
        self.{{ key[0] }} = data.get("{{ key[0] }}"){% endfor %}
        {% for key in connection_files_keys %}
        self.{{ key[0] }} = data.get("{{ key[0] }}"){% endfor %}
        {% if connection_ssl_verify %}
        self.{{ connection_ssl_verify[0] }} = data.get("{{ connection_ssl_verify[0] }}"){% endif %}
        ...

    
    def run(self, params={}):
        #   write your code
        #   可调用 popEmpty() 去除载荷中的空参数
        #   使用 setLocalCache() 设置本地缓存
        {% for key in run_url_params_keys %}
        self.{{ key[0] }} = params.get("{{ key[0] }}"){% endfor %}
        {% for key in run_headers_keys %}
        self.{{ key[0] }} = params.get("{{ key[0] }}"){% endfor %}
        {% for key in run_params_keys %}
        self.{{ key[0] }} = params.get("{{ key[0] }}"){% endfor %}
        {% for key in run_body_keys %}
        self.{{ key[0] }} = params.get("{{ key[0] }}"){% endfor %}
        {% for key in run_files_keys %}
        self.{{ key[0] }} = params.get("{{ key[0] }}"){% endfor %}
        {% if run_ssl_verify %}
        self.{{ run_ssl_verify[0] }} = data.get("{{ run_ssl_verify[0] }}"){% endif %}

        self.url = f"{{ url }}"

        _params = {}
        {% if run_params_keys %}{% for key in run_params_keys %}
        if self.{{ key[0] }}:
            _params["{{ key[1] }}"] = self.{{ key[0] }}
            {% endfor %}{% endif %}  
        {% if connection_params_keys %}{% for key in connection_params_keys %}
        if self.{{ key[0] }}:
            _params["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}

        headers = {}
        {% if run_headers_keys %}{% for key in run_headers_keys %}
        if self.{{ key[0] }}:
            headers["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}
        {% if connection_headers_keys %}{% for key in connection_headers_keys %}
        if self.{{ key[0] }}:
            headers["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}

        {% if body_type == None %}
        payload = {}
        {% endif %}

        {% if body_type == "JSON" %}
        payload = {}
        {% if run_body_keys %}{% for key in run_body_keys %}
        if self.{{ key[0] }}:
            payload["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}
        {% if connection_body_keys %}{% for key in connection_body_keys %}
        if self.{{ key[0] }}:
            payload["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}
        payload = json.dumps(payload)
        {% endif %}

        {% if body_type == "x-www-form-urlencoded" %}
        payload = ""
        {% if run_body_keys %}{% for key in run_body_keys %}
        if self.{{ key[0] }}:
            payload += f"{{ key[1] }}={self.{{ key[0] }}}&"
        {% endfor %}{% endif %}
        {% if connection_body_keys %}{% for key in connection_body_keys %}
        if self.{{ key[0] }}:
            payload += f"{{ key[1] }}={self.{{ key[0] }}}&"
        {% endfor %}{% endif %}
        if len(payload) > 1:
            payload = payload[:-1]
        {% endif %}

        {% if body_type == "form-data" %}
        payload = {}
        {% if run_body_keys %}{% for key in run_body_keys %}
        if self.{{ key[0] }}:
            payload["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}
        {% if connection_body_keys %}{% for key in connection_body_keys %}
        if self.{{ key[0] }}:
            payload["{{ key[1] }}"] = self.{{ key[0] }}
        {% endfor %}{% endif %}
        {% endif %}

        files = []
        {% if run_files_keys %}{% for key in run_files_keys %}
        if self.{{ key[0] }}:
            file_bytes = base64.b64decode(self.{{ key[0] }}.get("content",""))
            {{ key[0] }}_tempfile = tempfile.TemporaryFile()
            {{ key[0] }}_tempfile.write(file_bytes)
            {{ key[0] }}_tempfile.seek(0)
            if file_bytes:
                files.append(("{{ key[1] }}",(self.{{ key[0] }}.get("filename",""),{{ key[0] }}_tempfile)))
        {% endfor %}{% endif %}
        {% if connection_files_keys %}{% for key in connection_files_keys %}
        if self.{{ key[0] }}:
            file_bytes = base64.b64decode(self.{{ key[0] }}.get("content",""))
            {{ key[0] }}_tempfile = tempfile.TemporaryFile()
            {{ key[0] }}_tempfile.write(file_bytes)
            {{ key[0] }}_tempfile.seek(0)
            if file_bytes:
                files.append(("{{ key[1] }}",(self.{{ key[0] }}.get("filename",""),{{ key[0] }}_tempfile)))
        {% endfor %}{% endif %}

        try: 
            response = requests.request("{{ method }}", self.url, headers=headers, data=payload, {% if run_ssl_verify %}verify=self.{{ run_ssl_verify[0] }}, {% endif %}{% if connection_ssl_verify %}verify=self.{{ connection_ssl_verify[0] }}, {% endif %}params=_params, files=files)
        except Exception as error:
            raise Exception(f"请求失败 - {error}")

        {% if run_files_keys %}{% for key in run_files_keys %}{{ key[0] }}_tempfile.close()
        {% endfor %}{% endif %}
        {% if connection_files_keys %}{% for key in run_files_keys %}{{ key[0] }}_tempfile.close()
        {% endfor %}{% endif %}

        try:
            #   尝试获取返回数据
            response_data = response.json()
        except:
            response_data = {}

        return {
            "code" : response.status_code,
            "response_data" : response_data,
            "response_text" : response.text
        }
"""


actions_test_template = """
{
  "version": "v3",
  "type": "action",
  "body": {
    "action": "{{ name }}",
    "meta": {},
    "connection": {{ connectionKeys }},
    "dispatcher": null,
    "input": {{ inputKeys }},
    "config": {
      "log": {
        "max_log_size": 2,
        "max_log_size_unit": "MB",
        "log_clear_size": 0.5,
        "debug": false
      },
      "thread": {
        "threads_limit": 5
      }
    }
  }
}
"""

triggers_test_template = """
{
  "version": "v3",
  "type": "trigger",
  "body": {
    "trigger": "{{ name }}",
    "meta": {},
    "connection": {{ connectionKeys }},
    "dispatcher": {
      "url": "http://127.0.0.1:10001/transpond",
      "cache_url": ""
    },
    "input": {{ inputKeys }},
    "enable_web": false,
    "config": {
      "log": {
        "max_log_size": 2,
        "max_log_size_unit": "MB",
        "log_clear_size": 0.5,
        "debug": false
      },
      "thread": {
        "threads_limit": 5
      }
    }
  }
}
"""

alarm_receivers_test_template = """
{
  "version": "v3",
  "type": "alarm_receiver",
  "body": {
    "alarm": "{{ name }}",
    "meta": {},
    "connection": {{ connectionKeys }},
    "dispatcher": {
      "url": "http://127.0.0.1:10001/transpond",
      "cache_url": ""
    },
    "input": {{ inputKeys }},
    "enable_web": false,
    "config": {
      "log": {
        "max_log_size": 2,
        "max_log_size_unit": "MB",
        "log_clear_size": 0.5,
        "debug": false
      },
      "thread": {
        "threads_limit": 5
      }
    }
  }
}
"""

indicator_receivers_test_template = """
{
  "version": "v3",
  "type": "indicator_receiver",
  "body": {
    "receiver": "{{ name }}",
    "meta": {},
    "connection": {{ connectionKeys }},
    "dispatcher": {
      "url": "http://127.0.0.1:10001/transpond",
      "cache_url": ""
    },
    "input": {{ inputKeys }},
    "enable_web": false,
    "config": {
      "log": {
        "max_log_size": 2,
        "max_log_size_unit": "MB",
        "log_clear_size": 0.5,
        "debug": false
      },
      "thread": {
        "threads_limit": 5
      }
    }
  }
}
"""

asset_receivers_test_template = """
{
  "version": "v3",
  "type": "asset_receiver",
  "body": {
    "asset": "{{ name }}",
    "meta": {},
    "connection": {{ connectionKeys }},
    "dispatcher": {
      "url": "http://127.0.0.1:10001/transpond",
      "cache_url": ""
    },
    "input": {{ inputKeys }},
    "enable_web": false,
    "config": {
      "log": {
        "max_log_size": 2,
        "max_log_size_unit": "MB",
        "log_clear_size": 0.5,
        "debug": false
      },
      "thread": {
        "threads_limit": 5
      }
    }
  }
}
"""

main_template = """#!/usr/bin/env python

from SDK.cli import client
{% if actions %}
import actions{% endif %}
{% if triggers %}
import triggers{% endif %}
{% if indicator_receivers %}
import indicator_receivers{% endif %}
{% if alarm_receivers %}
import alarm_receivers{% endif %}
{% if asset_receivers %}
import asset_receivers{% endif %}

# 整个程序入口

class {{ pluginName }}(object):

    def __init__(self):

        self.connection = {}
        self.actions = {}
        self.triggers = {}
        self.indicator_receivers = {}
        self.alarm_receivers = {} 
        self.asset_receivers = {}
        
        {% for actionClass in actions %}
        self.add_actions(actions.{{ actionClass }}())
        {% endfor %}

        {% for triggerClass in triggers %}
        self.add_triggers(triggers.{{ triggerClass }}())
        {% endfor %}

        {% for indicatorReceiverClass in indicator_receivers %}
        self.add_indicator_receivers(indicator_receivers.{{ indicatorReceiverClass }}())
        {% endfor %}
        
        {% for alarmReceiverClass in alarm_receivers %}
        self.add_alarm_receivers(alarm_receivers.{{ alarmReceiverClass }}())
        {% endfor %}
        
        {% for assetReceiversClass in asset_receivers %}
        self.add_asset_receivers(asset_receivers.{{ assetReceiversClass }}())
        {% endfor %}
        
    def add_connection(self, connect):
        self.connection[connect.name] = connect

    def add_actions(self, action):
        self.actions[action.name] = action

    def add_triggers(self, trigger):
        self.triggers[trigger.name] = trigger

    def add_indicator_receivers(self, indicator_receiver):
        self.indicator_receivers[indicator_receiver.name] = indicator_receiver
    
    def add_alarm_receivers(self, alarm_receiver):
        self.alarm_receivers[alarm_receiver.name] = alarm_receiver
        
    def add_asset_receivers(self, asset_receiver):
        self.asset_receivers[asset_receiver.name] = asset_receiver

def main():

    client({{ pluginName }})


if __name__ == '__main__':
    main()
    
"""

init_template = """
import sys
from importlib import reload
{% if module == "actions" %}
from .models import *
reload(models)
{% endif %}
{% for name, className in init_list %}
from .{{ name }} import {{ className }}
{% endfor %}

def modules_dict():

    reload(sys.modules[__name__])
    {% if module == "actions" %}{% for name, className in init_list %}reload({{ name }})
    {% endfor %}{% endif %}
    return {
        {% for name, className in init_list %}"{{ name }}": {{ className }},
        {% endfor %}
    }
"""



help_template = """
# {{ name }}

## About
{{ name }}

## 版本信息
- {{ version }}

## Connection

{% if connection %}


{% for field_name, field_data in connection.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|

{%- endfor %}


{% endif %}


## Actions

{% if actions %}

{% for action, actionData in actions.items() %}

### {{ action }}

---

{% for action_name,action_data in actionData.items() %}

{% if action_name == 'input' %}
#### Input

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if action_name == 'output' %}
#### Output

{% for field_name, field_data in action_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Triggers

---

{% if triggers %}


{% for trigger, triggerData in triggers.items() %}

### {{ trigger }}

---

{% for trigger_name,trigger_data in triggerData.items() %}

{% if trigger_name == 'input' %}
#### Input

{% for field_name, field_data in trigger_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if trigger_name == 'output' %}
#### Output

{% for field_name, field_data in trigger_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Alarm Receivers

---

{% if alarm_receivers %}


{% for alarm_receiver, alarm_receiverData in alarm_receivers.items() %}

### {{ alarm_receiver }}


---

{% for alarm_receiver_name,alarm_receiver_data in alarm_receiverData.items() %}

{% if alarm_receiver_name == 'input' %}
#### Input

{% for field_name, field_data in alarm_receiver_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if alarm_receiver_name == 'output' %}
#### Output

{% for field_name, field_data in alarm_receiver_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Indicator Receivers

---

{% if indicator_receivers %}


{% for indicator_receiver, indicator_receiverData in indicator_receivers.items() %}

### {{ indicator_receiver }}

---

{% for indicator_receiver_name,indicator_receiver_data in indicator_receiverData.items() %}

{% if indicator_receiver_name == 'input' %}
#### Input

{% for field_name, field_data in indicator_receiver_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if indicator_receiver_name == 'output' %}
#### Output

{% for field_name, field_data in indicator_receiver_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Asset Receivers

---

{% if asset_receivers %}


{% for asset_receiver, asset_receiverData in asset_receivers.items() %}

### {{ asset_receiver }}

---

{% for asset_receiver_name,asset_receiver_data in asset_receiverData.items() %}

{% if asset_receiver_name == 'input' %}
#### Input

{% for field_name, field_data in asset_receiver_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}

{% endif %}


{% if asset_receiver_name == 'output' %}
#### Output

{% for field_name, field_data in asset_receiver_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|


{%- endfor %}


{% endif %}



{% endfor %}

{% endfor %}

{% endif %}



## Types

{% if types %}

{% for type_name, type_data in types.items() %}

### {{ type_name }}

{% for field_name, field_data in type_data.items() -%}

{% if loop.index == 1 -%}
|Name|Type|Required|Description|Default|Enum|
|----|----|--------|-----------|-------|----|
{%- endif %}
|{%- if field_data.title -%}
{{ field_data.title['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.type }}|{{ field_data.required }}|{%- if field_data.description -%}
{{ field_data.description['zh-CN'] }}
{%- else -%}
None
{%- endif -%}|{{ field_data.default|default('None') }}|{{ field_data.enum|default('None') }}|

{%- endfor %}

{% endfor %}

{% endif %}
"""

indicator_receivers_model_types = """
class Indicator(BaseModel):
    uid: str
    type: str
    value: str
    source: str
    reputation: str
    threat_score: int
    rawed: str
    tagsed: Optional[str] = None
    status: Optional[bool] = None
    notes: Optional[str] = None
    casesed: Optional[str] = None
    created_at: str
    updated_at: str


class IndicatorDomain(BaseModel):
    uid: str
    indicator_uid: str
    primary_domain: Optional[str] = None
    admin_name: Optional[str] = None
    organization: Optional[str] = None
    admin_email: Optional[str] = None
    admin_phone: Optional[str] = None
    admin_address: Optional[str] = None
    register_at: Optional[str] = None
    renew_at: Optional[str] = None
    name_provider: Optional[str] = None
    name_servers: Optional[str] = None


class IndicatorUrl(BaseModel):
    uid: str
    indicator_uid: str
    hash: Optional[str] = None
    host: Optional[str] = None


class IndicatorIp(BaseModel):
    uid: str
    indicator_uid: str
    hostname: Optional[str] = None
    geo_country: Optional[str] = None
    geo_location: Optional[str] = None
    open_ports: Optional[str] = None


class IndicatorHash(BaseModel):
    uid: str
    indicator_uid: str
    sha256: Optional[str] = None
    sha1: Optional[str] = None
    md5: Optional[str] = None


class IndicatorEmail(BaseModel):
    uid: str
    indicator_uid: str
    primary_domain: Optional[str] = None


class IndicatorFile(BaseModel):
    uid: str
    indicator_uid: str
    filename: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[str] = None
    sha256: Optional[str] = None
    sha1: Optional[str] = None
    md5: Optional[str] = None


class IndicatorHost(BaseModel):
    uid: str
    indicator_uid: str
    ip: Optional[str] = None
    mac: Optional[str] = None
    bios: Optional[str] = None
    memory: Optional[str] = None
    processors: Optional[str] = None
    os: Optional[str] = None


class IndicatorAccount(BaseModel):
    uid: str
    indicator_uid: str
    username: Optional[str] = None
    email: Optional[str] = None
    account_type: Optional[str] = None
    role: Optional[str] = None
    domain: Optional[str] = None
    organization: Optional[str] = None
"""

indicator_receivers_model_template = """
class {{ className }}(BaseModel):

    indicator: Indicator
    indicator_sub: Union[IndicatorDomain, IndicatorUrl, IndicatorIp, IndicatorHash, IndicatorEmail, IndicatorFile, IndicatorHost, IndicatorAccount, None]

"""

alarm_receivers_model_types = """
class Alarm(BaseModel):
    uid: str
    name: str
    alarm_ip: str
    alarm_type: str
    sip: str
    tip: str
    source: str
    type: str
    reputation: str
    status: Optional[bool] = True
    raw: str
    created_at: str
    updated_at: str
    
"""

alarm_receivers_model_template = """
class {{ className }}(BaseModel):

    alarm: Alarm
    
"""

asset_receivers_model_types = """
class Asset(BaseModel):
    servicer: str = ""
    device_type: str = ""
    device_id: str = ""
    name: str = ""
    public_ipv4: str = ""
    inner_ipv4: str = ""
    location: str = ""
    department: str = ""
    description: str = ""
    mac: str = ""
    model: str = ""
    os: str = ""
    cpu: str = ""
    ram: str = ""
    kernel_version: str = ""
    port: str = ""
    disk: str = ""
    software: str = ""
    tag: Optional[List[str]] = []
    raw: str = ""
    created_at: str
    updated_at: str
"""

asset_receivers_model_template = """
class {{ className }}(BaseModel):

    asset: Asset
    
"""

testserver_head_template = r"""
from fastapi import FastAPI,HTTPException
import uvicorn
import typing
import json
from SDK.base import * 

description = \
'''
  欢迎使用 1.2.8 版本SDK提供的全新测试系统。\n
  相较于之前的版本的 REST 测试接口，这个版本提供了更加详细的功能细分以及测试数据输入指引。\n
  现在再也不会几个接口测试一大堆功能，一大堆参数还不知道怎么填了。\n
  
  Enjoy it!  -- Matthews_K

'''
test_server = FastAPI(title="Chariot-Plugin Test Server", version="1.2.8", description=description)

"""

testserver_tail_template = """
def runserver():
    os.system("")
    log("attention","在浏览器内输入 http://127.0.0.1:1453/docs 以进行接口测试")
    log("attention","在浏览器内输入 http://127.0.0.1:1453/redoc 以查看帮助文档")
    uvicorn.run(test_server,host="127.0.0.1", port=1453)


if __name__ == '__main__':

    runserver()
"""

testserver_actions_template = """
@test_server.post("/actions/{{ name }}",response_model={{ class_name }}().outputModel,tags=["动作"])
def action_{{ name }}(connection_data:{{ class_name }}().connModel=None,
                      input_data:{{ class_name }}().inputModel=None):
    
    clearLog()

    connection_data = connection_data.dict()

    input_data = input_data.dict()

    output = {{ class_name }}()._run(input_data,connection_data)

    if output["body"].get("error_trace"):
        raise HTTPException(500,detail=output["body"]["error_trace"])
    else:
        output_data = output["body"]["output"]

    return output_data

"""

testserver_triggers_template = """
@test_server.post("/triggers/{{ name }}",response_model={{ class_name }}().outputModel,tags=["触发器"])
def trigger_{{ name }}(dispatcher_url:str="http://127.0.0.1:8000/send",
                       connection_data:{{ class_name }}().connModel=None,
                       input_data:{{ class_name }}().inputModel=None):
    
    clearLog()

    connection_data = connection_data.dict()

    input_data = input_data.dict()

    output = {{ class_name }}()._run(input_data,connection_data,dispatcher_url)

    if output["body"].get("error_trace"):
        raise HTTPException(500,detail=output["body"]["error_trace"])
    else:
        output_data = output["body"]["output"]

    return output_data

"""

testserver_alarm_receivers_template = """
@test_server.post("/alarm_receivers/{{ name }}",response_model={{ class_name }}().outputModel,tags=["告警接收器"])
def alarm_receiver_{{ name }}(dispatcher_url:str="http://127.0.0.1:8000/send",
                              connection_data:{{ class_name }}().connModel=None,
                              input_data:{{ class_name }}().inputModel=None):
    
    clearLog()

    connection_data = connection_data.dict()

    input_data = input_data.dict()

    output = {{ class_name }}()._run(input_data,connection_data,dispatcher_url)

    if output["body"].get("error_trace"):
        raise HTTPException(500,detail=output["body"]["error_trace"])
    else:
        output_data = output["body"]["output"]

    return output_data

"""

testserver_indicator_receivers_template = """
@test_server.post("/indicator_receivers/{{ name }}",response_model={{ class_name }}().outputModel,tags=["情报接收器"])
def indicator_receiver_{{ name }}(dispatcher_url:str="http://127.0.0.1:8000/send",
                              connection_data:{{ class_name }}().connModel=None,
                              input_data:{{ class_name }}().inputModel=None):
    
    clearLog()

    connection_data = connection_data.dict()

    input_data = input_data.dict()

    output = {{ class_name }}()._run(input_data,connection_data,dispatcher_url)

    if output["body"].get("error_trace"):
        raise HTTPException(500,detail=output["body"]["error_trace"])
    else:
        output_data = output["body"]["output"]

    return output_data

"""


