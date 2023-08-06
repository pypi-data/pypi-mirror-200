# Copyright 2022 Ksyun Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys


class Serializer(object):
    def serialize(self, allow_none=False, allow_no_public=False, first_letter_upper=False):
        d = vars(self)
        ret = {}
        for k in d:
            if not allow_no_public and k.startswith('_'):
                continue

            if isinstance(d[k], Serializer):
                r = d[k].serialize(allow_none, allow_no_public)
            elif isinstance(d[k], list):
                r = list()
                for tem in d[k]:
                    if isinstance(tem, Serializer):
                        r.append(tem.serialize(allow_none, allow_no_public))
                    else:
                        r.append(
                            tem.encode("UTF-8") if isinstance(tem, type(u"")) and sys.version_info[0] == 2 else tem)
            else:
                r = d[k].encode("UTF-8") if isinstance(d[k], type(u"")) and sys.version_info[0] == 2 else d[k]
            if allow_none or r is not None:
                key = k[0].upper() + k[1:] if first_letter_upper else k
                ret[key] = r
        return ret

    def deserialize(self, data, obj):
        d = CommonObject(data).__dict__
        obj.__dict__.update(d)


class CommonObject(Serializer):
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.__dict__[key] = CommonObject(value)
            elif isinstance(value, list) or isinstance(value, tuple):
                ll = []
                for itm in value:
                    if isinstance(itm, dict):
                        ll.append(CommonObject(itm))
                    else:
                        ll.append(itm)
                self.__dict__[key] = ll
            else:
                self.__dict__[key] = value


class AbstractModel(Serializer):
    """Base class for all models."""

    def _deserialize(self, params):
        return None

    def to_json_string(self, *args, **kwargs):
        """Serialize obj to a JSON formatted str, ensure_ascii is False by default"""
        if "ensure_ascii" not in kwargs:
            kwargs["ensure_ascii"] = False
        return json.dumps(self.serialize(allow_none=True), *args, **kwargs)

    def from_json_string(self, jsonStr):
        """Deserialize a JSON formatted str to a Python object"""
        params = json.loads(jsonStr)
        self._deserialize(params)

    def __repr__(self):
        return "%s" % self.to_json_string()
