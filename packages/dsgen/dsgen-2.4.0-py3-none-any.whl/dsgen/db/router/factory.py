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
# dsgen.db.router.factory

from dsgen.schema.parser import NamespaceParameterParser
from .prototype import ProtoType


class RouterFactory(object):

    def __init__(self):
        super().__init__()
        self._public_member = dict()
        #
        self.parser = NamespaceParameterParser()
        self.load_preset()

    def load_preset(self):
        return self

    def get_ns_params(self, x):
        '''
        :param x: (string)
        '''
        return self.parser.do(x)

    def get_concrete_cls(self, x):
        '''
        :param x: (string)
        '''
        ns_params = self.get_ns_params(x)

        BASE = ProtoType
        try:
            assert getattr(self, 'use_namespace', False), 'skip'
            BASE = import_string(ns_params['namespace'])
        except:
            pass

        class _stub(BASE):
            route_app_labels = { ns_params['params']['app'], }
            db_alias = ns_params['params']['alias']
            pass
        return _stub

    def get_member(self, name):
        '''
        :param name: (string)
        '''
        member = None

        if name in self.get_public_member():
            member = self._public_member[ name ]
        elif self.get_ns_params(name)['namespace'] is not None:
            member = self.get_concrete_cls(name)
        else:
            if getattr(self, 'use_exc', False):
                raise AttributeError(name)
        return member

    def get_public_member(self):
        return self._public_member.keys()


_factory = RouterFactory()
__dir__ = _factory.get_public_member
__getattr__ = _factory.get_member

#---eof---#
