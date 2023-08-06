# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Xingeng Chen
# Copyright 2016, 2017, 2018 Liang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# dsgen.utils

import json

from .base import DSBase, CeleryHelper
from .message import MSG_FORMAT_ERROR_LOADING_JSON


class DSGenerator(DSBase):
    '''
    instantisilize a sub-class of this, and override module-level reference to instance method
    `__dir__` => `get_config_field_list`
    `__getattr__` => get_config_value`
    '''

    def __init__(self, json_path=None):
        '''
        :param json_path: (string)
        '''
        super(DSGenerator, self).__init__()
        self.site_config = dict()

        if json_path is not None:
            try:
                with open(json_path, 'r') as json_f:
                    self.site_config.update(
                        json.load(json_f)
                    )
            except Exception as e:
                from django.core.exceptions import ImproperlyConfigured
                msg = MSG_FORMAT_ERROR_LOADING_JSON.format(fp=json_path)
                bad_config = ImproperlyConfigured(msg)
                raise bad_config
            self.site_json_path = json_path
        self.collect_apps()

    def get_config_field_list(self):
        attr_fields = [ attr for attr in dir(self) if attr.isupper() ]
        dict_fields = list(self.site_config.keys())
        dict_extra_fields = [ each for each in dict_fields if not(each in attr_fields) ]
        # rvalue;
        all_fields = list()
        all_fields.extend(attr_fields)
        all_fields.extend(dict_extra_fields)
        return all_fields

    def get_config_value(self, name):
        '''
        :param name: (string)
        '''
        if name.startswith('_'):
            value = globals().get(name)
        else:
            value = getattr(
                self,
                name,
                self.site_config.get(name)
            )
        return value


class DSetting(object):
    '''
    base-class for Django app setting

    subclass MUST declare the following attributes:
    - `DEFAULT` (dict)
    - `SETTING_NAME` (string)

    subclass MAY override the following methods:
    - `get_passthrough_fields` (list/tuple)
    '''

    def __init__(self):
        self._default = self.DEFAULT
        self._cache_key = set()
        from django.conf import settings as _ds_conf
        self._ds_conf = _ds_conf

    @property
    def site_conf(self):
        if not hasattr(self, '_site'):
            _conf = getattr(
                self._ds_conf,
                self.SETTING_NAME,
                dict()
            )
            setattr(
                self,
                '_site',
                _conf
            )
        return self._site

    def get_passthrough_fields(self):
        '''
        :return: (list/tuple of string)
        '''
        pass_through_list = list()
        return pass_through_list

    def __getattr__(self, attr):
        '''
        :param attr: (string)
        '''
        if attr in self.get_passthrough_fields():
            return getattr(self._ds_conf, attr)
        if attr not in self._default:
            raise AttributeError("Invalid setting: '%s'" % attr)

        try:
            val = self.site_conf[attr]
        except KeyError:
            val = self._default[attr]

        self._cache_key.add(attr)
        setattr(self, attr, val)
        return val

    def signal_handler_setting_changed(self, *args, **kwargs):
        '''
        stub handler for `django.test.signals.setting_changed`
        '''
        if kwargs['setting'] == self.SETTING_NAME:
            self.reload()
        return None

    def reload(self):
        '''
        flush cached values
        '''
        for item in self._cache_key:
            delattr(self, item)
        self._cache_key.clear()
        if hasattr(self, '_site'):
            delattr(self, '_site')
        return None


class DSCeleryConfig(CeleryHelper):
    '''
    helper class for Celery task schedule and queue definition
    '''

    def convert_queue_definition(self, data):
        '''
        construct Celery queue definition

        ```json
        {
            "name": "demo",
            "exchange": "demo",
            "exchange.type": "direct",
            "routing_key": "task"
        }
        ```

        :param data: plain values from JSON (dict)
        :return: conversion result (dict)
        '''
        from kombu import Exchange, Queue
        exch = Exchange(
            data.get('exchange', data['name']),
            type=data.get('exchange.type', 'fanout'),
        )
        queue = Queue(
            data['name'],
            exch,
            routing_key=data['routing_key'],
        )
        return queue

    def create_schedule(self, data):
        '''
        construct Celery schedule objects

        ```json
        {
            "task-description": {
                "task": "app.tasks.a_simple_task",
                "schedule": timedelta(minutes=30)
            },
            "second-task-description": {
                "task": "app.tasks.another_task",
                "schedule": crontab(minute='3', hour='0,1,2,6,7,8,9,10,11')
            }
        }
        ```

        :param data: plain values from JSON (dict)
        :return: conversion result (dict)
        '''
        from celery.schedules import crontab
        from datetime import timedelta

        val = dict()
        val.update(data)
        for task in val.keys():
            raw_val = val[ task ]['schedule']
            try:
                tokens = raw_val.split('=', 1)
                td_param = {
                    tokens[0]: int(tokens[1]),
                }
                val[ task ]['schedule'] = timedelta(**td_param)
            except AttributeError:
                val[ task ]['schedule'] = crontab(**raw_val)
            except ValueError:
                # currently we just drop the incorrectly defined items;
                pass
            pass  #-end-for-task-in
        return val


#---eof---#
