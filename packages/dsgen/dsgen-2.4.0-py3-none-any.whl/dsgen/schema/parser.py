# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Xingeng Chen
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
# dsgen.schema.parser

from .base import SpaceDelimited, SemicolonDelimited


class SchemaParser(object):
    def __init__(self):
        super().__init__()
        #
        self.load_preset()

    def load_preset(self):
        return self


class NamespaceParameterParser(SchemaParser):

    def load_preset(self):
        self.delimiter_hub = dict()

        self.delimiter_hub[ SpaceDelimited.SPACE ] = SpaceDelimited
        self.delimiter_hub[ SemicolonDelimited.SEMICOLON ] = SemicolonDelimited

        return self

    def do(self, x):
        '''
        :param x: (string)
        '''
        rval = {
            'namespace': None,
            'params': dict(),
        }

        stub = None
        for spacer in self.delimiter_hub.keys():
            if spacer in x:
                stub = self.delimiter_hub[ spacer ]
                break

        if stub is not None:
            actor = stub()
            actor.argument_delimiter = actor.COLON
            token = actor.get_tokens(x)
            rval['namespace'] = token[0]

            for arg in token[1:]:
                kv = actor.split_key_value(arg)
                rval['params'][ kv[0] ] = kv[1]

        return rval

#---eof---#
