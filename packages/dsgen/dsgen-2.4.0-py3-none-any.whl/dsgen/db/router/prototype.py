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
# dsgen.db.router.prototype


class ProtoType(object):
    route_app_labels = {
        '<dsgen>',
    }
    db_alias = 'image'

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db_alias
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db_alias
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migration(self, db, app_label, model_name=None, **hints):
        db_is_matched = (db == self.db_alias)
        if app_label in self.route_app_labels:
            return db_is_matched
        else:
            return not(db_is_matched)
        return None

#---eof---#
