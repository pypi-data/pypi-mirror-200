#!/usr/bin/env python3
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
# dsgen.__dsq_main__ -- console script `dsq`

import argparse
import importlib
import json
import os
import sys


class DSQuery(object):
    CONST_ENV_NAME = 'DJANGO_SETTINGS_MODULE'

    CONST_DESCR = ''

    DEFAULT_DS = 'app.settings'

    def __init__(self):
        super(DSQuery, self).__init__()
        self.parser = argparse.ArgumentParser(
            description=self.CONST_DESCR
        )
        self.append_arguments(self.parser)

    def append_arguments(self, obj):
        '''
        :param obj: (`ArgumentParser`)
        '''
        obj.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            help='turn on debug output'
        )
        obj.add_argument(
            '--json',
            dest='json',
            action='store_true',
            help='output JSON format'
        )
        obj.add_argument(
            'name',
            type=str,
            help='the field name'
        )
        return self

    def process_args(self, args):
        '''
        :param args: (list of string)
        '''
        self.option = self.parser.parse_args(args)
        return self

    def get_ds_module(self):
        self.target = os.getenv(
            self.CONST_ENV_NAME,
            self.DEFAULT_DS
        )
        try:
            self.ds_mod = importlib.import_module(
                self.target
            )
        except ModuleNotFoundError as e:
            msg = "fail to load the module '{s}'.".format(
                s=self.target
            )
            raise ValueError(msg)
        return self

    def extract_value(self, name):
        '''
        :param name: (string)

        :return: (object)
        '''
        return getattr(self.ds_mod, name)

    def output_format(self, value):
        '''
        :param value: (object)

        :return: JSON stream or raw input value (object)
        '''
        if self.option.json:
            formatted = json.dumps(value)
        else:
            formatted = value
        return formatted

    def run(self, args):
        '''
        :param args: (list of string)
        '''
        ret = 0
        try:
            self.process_args(args)
            self.get_ds_module()
            val = self.extract_value(self.option.name)
            final_val = self.output_format(val)
            print(final_val)
        except Exception as e:
            if self.option.debug:
                print(e, file=sys.stderr)
            ret = 2
        return ret


def main():
    app = DSQuery()
    return app.run(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(main())

#---eof---#
